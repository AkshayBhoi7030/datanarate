from typing import List, Dict, Any, Optional
import json
from app.llm.ollama_service import OllamaService
from app.llm.openrouter_service import OpenRouterService
from app.prompts.sql_prompts import INSIGHT_GENERATION_PROMPT
from app.core.logging import logger


class InsightGenerator:
    def __init__(self):
        self.ollama_service = OllamaService()
        self.openrouter_service = OpenRouterService()

    async def generate_insights(self, question: str, results: List[Dict[str, Any]]):
        logger.info("Generating insights from query results")

        if not results:
            logger.warning("No data found for your query")
            return "### Executive Summary\nNo data found for your query."

        num_rows = len(results)
        columns = list(results[0].keys())
        logger.debug(f"Data: {num_rows} rows, columns: {columns}")

        # First, try to generate structured fallback insights without LLM
        logger.debug("Generating structured fallback insights...")
        structured_fallback = self._generate_structured_fallback(question, results)
        logger.debug("Structured fallback generated successfully")

        try:
            # Try OpenRouter first
            logger.debug("Trying OpenRouter for insights...")
            try:
                results_str = json.dumps(results, indent=2)
                prompt = INSIGHT_GENERATION_PROMPT.format(
                    question=question,
                    results=results_str
                )
                insights = await self.openrouter_service.generate(
                    prompt=prompt,
                    temperature=0.7,
                    max_tokens=1024
                )
                logger.info("Generated insights via OpenRouter successfully")
                return insights
            except Exception as e:
                logger.warning(f"OpenRouter failed, trying Ollama: {e}", exc_info=True)

            # Try Ollama second
            logger.debug("Trying Ollama for insights...")
            try:
                results_str = json.dumps(results, indent=2)
                prompt = INSIGHT_GENERATION_PROMPT.format(
                    question=question,
                    results=results_str
                )
                insights = await self.ollama_service.generate(
                    prompt=prompt,
                    temperature=0.7,
                    max_tokens=1024
                )
                logger.info("Generated insights via Ollama successfully")
                return insights
            except Exception as e:
                logger.warning(f"Ollama failed, using fallback: {e}", exc_info=True)

        except Exception as e:
            logger.warning(f"All LLM services failed, using structured fallback: {e}", exc_info=True)

        return structured_fallback
    
    def _generate_structured_fallback(self, question: str, results: List[Dict[str, Any]]) -> str:
        num_rows = len(results)
        columns = list(results[0].keys())
        
        # Identify numeric columns
        numeric_cols = []
        for col in columns:
            try:
                float(results[0][col])
                numeric_cols.append(col)
            except (ValueError, TypeError):
                continue
        
        insights = []
        
        # Executive Summary
        insights.append("### Executive Summary")
        insights.append(f"Query returned {num_rows} records with columns: {', '.join(columns)}.")
        if numeric_cols:
            insights.append(f"Key numeric metrics available: {', '.join(numeric_cols)}.")
        
        # Key Insights
        insights.append("\n### Key Insights")
        insights.append(f"• Dataset size: {num_rows} records")
        insights.append(f"• Number of columns: {len(columns)}")
        
        # Top Performers (if we have numeric data)
        if numeric_cols and num_rows > 0:
            top_col = numeric_cols[0]
            sorted_results = sorted(
                results,
                key=lambda x: float(x[top_col]) if x[top_col] is not None else 0,
                reverse=True
            )
            top_3 = sorted_results[:3]
            
            insights.append("\n### Top Performers")
            for idx, row in enumerate(top_3, 1):
                label = str(row[columns[0]]) if columns[0] in row else f"Item {idx}"
                value = row[top_col]
                insights.append(f"• {label}: {value}")
            
            # Lowest Performers
            bottom_3 = sorted_results[-3:]
            insights.append("\n### Lowest Performers")
            for idx, row in enumerate(reversed(bottom_3), 1):
                label = str(row[columns[0]]) if columns[0] in row else f"Item {idx}"
                value = row[top_col]
                insights.append(f"• {label}: {value}")
        
        # Recommendations
        insights.append("\n### Recommendations")
        insights.append("• For more detailed insights, connect Ollama or OpenRouter.")
        insights.append("• Use specific questions about trends or comparisons.")
        
        return "\n".join(insights)
