# DataNarrate Demo Scripts

## 5-Minute Demo Script (Recruiter / Quick Pitch)

**[0:00 - 0:30] Opening**
- "Hi, I want to show you DataNarrate - an AI-powered analytics platform I built"
- "It lets anyone ask questions about their data in plain English, no SQL needed"

**[0:30 - 1:30] Demo Dashboard**
- Open DataNarrate dashboard
- "Here's the main interface - clean and intuitive"
- Show key sections: Query Input, Results, Charts, History

**[1:30 - 2:30] Natural Language to SQL**
- Ask a question: "Show me total revenue by category"
- "Watch - the AI generates SQL automatically"
- "Here's the query result, and a chart is generated automatically"

**[2:30 - 3:30] Saved Queries & History**
- Show query history sidebar
- "You can save frequently used queries for later"
- "Let's run this saved query - Monthly Revenue"

**[3:30 - 4:30] Exports**
- "You can export results in multiple formats"
- Show CSV, Excel, PDF export buttons
- Download a PDF report as example

**[4:30 - 5:00] Closing**
- "That's DataNarrate - turning questions into insights in seconds"
- "I built the full stack: FastAPI backend, React frontend, AI pipeline, Docker, CI/CD"
- "Let me know if you'd like a deeper technical dive!"

---

## 10-Minute Demo Script (Technical Interviewer)

**[0:00 - 1:00] Project Overview**
- "DataNarrate is an AI analytics platform - I'll walk you through the product and the tech"
- Highlight: FastAPI, React, Ollama, PostgreSQL, Redis, Docker

**[1:00 - 3:00] Architecture Deep Dive**
- Show architecture diagram
- "Here's the stack: Frontend calls FastAPI, which uses Ollama + RAG for SQL generation"
- "We cache results in Redis for performance"
- "PostgreSQL stores user data, saved queries, history"

**[3:00 - 5:00] AI Pipeline Demo**
- "Let's see how the AI works: User question → Schema Retrieval (RAG) → Prompt → LLM → SQL"
- "Important: We validate all SQL before execution to block DROP/DELETE"
- Show SQL validator test results

**[5:00 - 7:00] Key Features**
- Walk through query interface, results, charts
- Show saved queries, history
- Demonstrate exports: CSV, Excel, PDF

**[7:00 - 9:00] Technical Choices**
- "Why FastAPI? Async, auto-docs, great ecosystem"
- "Why Ollama? Local development, easy to swap to OpenAI/Anthropic"
- "Why Redis? Caching SQL and results for 80% faster responses"

**[9:00 - 10:00] Closing & Questions**
- "That's a quick tour - I'd be happy to dive deeper into any part"
- "What questions do you have about the architecture, code, or challenges?"

---

## Recruiter Demo Flow
1. **Hook**: "Turns natural language into data insights"
2. **Visual**: Show dashboard, charts, clean UI
3. **Social Proof**: Tests, CI/CD, Docker
4. **Impact**: Makes analytics accessible to non-technical users

## Technical Interviewer Demo Flow
1. **Architecture**: Start with system design diagram
2. **Code Deep Dive**: Show specific files (SQL validator, RAG, cache)
3. **Challenges**: Talk about SQL security, AI accuracy, performance
4. **Trade-offs**: Local vs hosted LLM, SQL vs NoSQL, etc.
5. **Testing & CI/CD**: Show test coverage, GitHub Actions
