from fastapi import APIRouter, BackgroundTasks
from app.agents.sql_generator_agent import SQLGeneratorAgent
from app.executors.safe_sql_executor import SafeSQLExecutor
from app.explainers.insight_generator import InsightGenerator
from app.core.cache import redis_cache
from app.core.responses import APIResponse
from app.schemas.query import QueryRequest, QueryResponse
from app.core.logging import logger
from app.core.exceptions import DataNarrateException, InternalServerErrorException

router = APIRouter(prefix="/query", tags=["query"])


@router.post("", response_model=APIResponse[QueryResponse])
async def query_data(request: QueryRequest, background_tasks: BackgroundTasks):
    question = request.question
    logger.info(f"Starting query processing for: '{question}'")

    # Initialize services
    sql_agent = SQLGeneratorAgent()
    sql_executor = SafeSQLExecutor()
    insight_gen = InsightGenerator()

    # Check cache
    logger.debug("Checking cache...")
    cached_sql = await redis_cache.get_sql(question)
    cached_results = await redis_cache.get_results(question)
    cached_insights = await redis_cache.get_insights(question)

    if cached_sql and cached_results and cached_insights:
        logger.info("Using cached query results")
        return APIResponse(
            data=QueryResponse(
                question=question,
                sql=cached_sql,
                data=cached_results,
                insight=cached_insights
            )
        )

    try:
        logger.debug("Step 1: Generating SQL...")
        # Generate SQL
        sql = await sql_agent.generate_sql(question)

        logger.debug("Step 2: Executing SQL...")
        # Execute SQL
        results = sql_executor.execute(sql)

        logger.debug("Step 3: Generating insights...")
        try:
            # Generate insights (optional)
            insights = await insight_gen.generate_insights(question, results)
        except Exception as e:
            logger.warning(f"Failed to generate insights, using default: {str(e)}", exc_info=True)
            insights = "Insights unavailable. Please ensure Ollama is running for this feature."

        logger.debug("Step 4: Caching results...")
        # Cache results in background
        background_tasks.add_task(redis_cache.set_sql, question, sql)
        background_tasks.add_task(redis_cache.set_results, question, results)
        background_tasks.add_task(redis_cache.set_insights, question, insights)

        logger.info("Query processing completed successfully")
        return APIResponse(
            data=QueryResponse(
                question=question,
                sql=sql,
                data=results,
                insight=insights
            )
        )
    except DataNarrateException:
        raise
    except Exception as e:
        logger.error(f"Query failed: {str(e)}", exc_info=True)
        raise InternalServerErrorException(
            detail=f"Failed to process query. Please ensure Ollama is running locally with phi3:mini model. Error: {str(e)}",
            error_code="QUERY_PROCESSING_FAILED"
        )
