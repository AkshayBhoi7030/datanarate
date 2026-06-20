from typing import List, Dict, Any
from pydantic import BaseModel
from app.agents.sql_generator_agent import SQLGeneratorAgent
from app.validators.sql_validator import SQLValidator
from app.executors.safe_sql_executor import SafeSQLExecutor
from app.explainers.insight_generator import InsightGenerator
from app.core.logging import logger


class TestCase(BaseModel):
    question: str
    expected_tables: List[str]


class EvaluationResult(BaseModel):
    question: str
    sql_generated: bool
    sql_valid: bool
    execution_successful: bool
    insight_generated: bool
    error: str = ""


class EvaluationFramework:
    def __init__(self):
        self.test_cases = [
            TestCase(
                question="Show me all users",
                expected_tables=["users"]
            ),
            TestCase(
                question="What's the total revenue?",
                expected_tables=["orders", "products"]
            ),
            TestCase(
                question="List the top 10 customers by purchase amount",
                expected_tables=["customers", "orders"]
            ),
            TestCase(
                question="Show me product sales by category",
                expected_tables=["products", "orders"]
            ),
            TestCase(
                question="What's the average order value?",
                expected_tables=["orders"]
            ),
        ]
        self.sql_agent = SQLGeneratorAgent()
        self.validator = SQLValidator()
        self.executor = SafeSQLExecutor()
        self.insight_gen = InsightGenerator()

    async def run_evaluation(self) -> List[EvaluationResult]:
        results = []
        for test_case in self.test_cases:
            logger.info(f"Evaluating: {test_case.question}")
            result = EvaluationResult(question=test_case.question)
            try:
                # Test 1: SQL Generation
                sql = await self.sql_agent.generate_sql(test_case.question)
                result.sql_generated = len(sql) > 0
                logger.info(f"Generated SQL: {sql}")

                # Test 2: SQL Validation
                self.validator.validate(sql)
                result.sql_valid = True

                # We won't actually execute without sample DB
                # For real evaluation, you'd need a sample database
                result.execution_successful = False
                result.insight_generated = False

            except Exception as e:
                result.error = str(e)
                logger.error(f"Test failed: {e}")
            results.append(result)
        return results

    def print_report(self, results: List[EvaluationResult]):
        total = len(results)
        sql_gen_success = sum(1 for r in results if r.sql_generated)
        sql_val_success = sum(1 for r in results if r.sql_valid)
        exec_success = sum(1 for r in results if r.execution_successful)
        insight_success = sum(1 for r in results if r.insight_generated)

        print("\n" + "=" * 60)
        print("DataNarrate Evaluation Report")
        print("=" * 60)
        print(f"Total test cases: {total}")
        print(f"SQL generation success: {sql_gen_success}/{total} ({sql_gen_success/total*100:.1f}%)")
        print(f"SQL validation success: {sql_val_success}/{total} ({sql_val_success/total*100:.1f}%)")
        print(f"Execution success: {exec_success}/{total} ({exec_success/total*100:.1f}%)")
        print(f"Insight generation success: {insight_success}/{total} ({insight_success/total*100:.1f}%)")
        print("=" * 60)
