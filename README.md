# 🧠 MCP-Powered HR Assistant (FastAPI + LLM Tool Calling)

## 📌 Overview

This project demonstrates how to build a context-aware AI assistant that interacts with structured enterprise data using the Model Context Protocol (MCP).

Instead of relying only on embeddings and RAG, the assistant dynamically discovers tools, executes database queries, and reasons over live data using an LLM.

The use case is a real-world HR / Employee Analytics system, supporting queries like:

- Who works in a specific location?
- What is an employee’s salary?
- Who reports to whom?
- Follow-up questions using conversational context

## ❓ Why not just RAG?

Traditional RAG systems work well for unstructured text (docs, PDFs, policies), but they struggle with:

- Live databases
- Aggregations (highest salary, averages)
- Filters (location, department)
- Deterministic answers
- Follow-up questions using pronouns (“his”, “that employee”)

MCP solves this by allowing the LLM to call tools instead of guessing.

## 🧩 What is MCP (Model Context Protocol)?

MCP is a protocol, not a library.

It defines:

- How tools are described
- How models discover tools
- How models call tools
- How results are returned and reasoned over

In this project:

- Each FastAPI endpoint = an MCP tool
- `/mcp/tools` = tool discovery
- The LLM decides when and which tool to call

## 🏗️ Architecture

```
User
  ↓
LLM (reasoning + memory)
  ↓ decides tool
MCP Client
  ↓
MCP Server (FastAPI)
  ↓
SQLite Employee Database
  ↓
Structured JSON result
  ↓
LLM formats final answer
```

**Key Design Principles**

- LLM is stateless
- Application provides conversation memory
- Database access is deterministic
- No embeddings for structured data
- No hard-coded intent logic

## 📂 Project Structure

```
mcp-employee-ai/
│
├── init_db.py          # Creates and seeds the employee database
├── mcp_server.py       # MCP tool server (FastAPI)
├── mcp_client.py       # Simple MCP client (tool discovery + execution)
├── llm_app.py          # LLM + MCP orchestration with conversation memory
├── requirements.txt    # Python dependencies
└── README.md
```

## 🧪 Example Capabilities

The assistant can answer:

- “Which location James is working from?”
- “What is his salary?” (context-aware)
- “Who else works in London?”
- “Who reports to EMP-1002?”
- “List employees working in Bangalore”

The assistant:

- Remembers context
- Resolves pronouns
- Chooses tools automatically
- Avoids hallucination

## ⚙️ Setup Instructions (Step by Step)

1️⃣ Create virtual environment (recommended)

```bash
python -m venv venv_for_mcp
source venv_for_mcp/bin/activate
```

2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

3️⃣ Initialize the database

This creates a SQLite database with realistic employee data (Example).

```bash
python init_db.py
```

4️⃣ Start the MCP server

```bash
uvicorn mcp_server:app --port 3333
Or 
uvicorn mcp_server:app --reload --port 3333
```

Verify:

- Open http://127.0.0.1:3333/docs
- You should see MCP tools listed

5️⃣ Run the LLM application

Open a new terminal (same venv):

```bash
python llm_app.py
```

## 📄 Note on `mcp_client.py`

You may notice a file named `mcp_client.py` in this repository.

This file is not required for the main application flow and is not used by `llm_app.py`.

Why it exists:

- It is a standalone MCP client used to:
  - Test MCP tool discovery (`/mcp/tools`)
  - Execute MCP tools directly without involving an LLM
  - Debug database queries and MCP server behavior in isolation

Actual execution flow:

- `llm_app.py` acts as the real MCP client when the LLM is running
- `mcp_client.py` exists purely for learning, debugging, and demonstration purposes

You can safely remove this file if you only want the LLM-driven experience.

Optional one-liner (even shorter)

If you want something ultra-minimal:

`mcp_client.py` is an optional utility to interact with the MCP server without an LLM. The main application (`llm_app.py`) already acts as the MCP client during normal execution.


## 💬 Sample Conversation

Ask a question: Which location James is working from?

→ James is working from the London location.

Ask a question: What is his salary?

→ James's base salary is 2,500,000.

Ask a question: Who else works in London?

→ Emily Clark, Oliver Wilson, Daniel Miller...

## 🧠 Key Learnings from This Project

- MCP is a protocol, not a framework
- LLMs do not have memory — applications must manage it
- Every tool call must be answered (tool_call_id)
- Structured data should be queried, not embedded
- Agent systems require strict orchestration

## 🚀 Why This Project Matters

This project demonstrates:

- Agentic LLM design
- Tool discovery and execution
- Context-aware conversations
- Enterprise-style data access
- Real debugging of protocol-level issues

It goes beyond basic RAG demos and reflects real-world GenAI system design.

## 🔮 Possible Improvements

- Add salary analytics tools (highest / average salary)
- Role-based access (HR vs Manager)
- Redis-backed conversation memory
- Combine MCP + RAG for policy documents
- Add caching for tool calls

## 👤 Author

Built by Ajmal
Sharing learnings around GenAI, MCP, and agentic systems.
