# 📝 MCP Project – Todo List Assistant with JIRA Integration

This project is a **Modular Conversational Platform (MCP)** powered by **FastAPI**, **Starlette**, and **FastMCP**.  
It combines three components:  

1. **main.py** → A FastAPI-based **Todo List API** (task CRUD + move/search).  
2. **mcp_server.py** → An MCP server that wraps APIs and exposes them over SSE.  
3. **client.py** → An interactive CLI client that connects to the MCP server and uses an agent runner.

---

## 🚀 Features
- Manage tasks with sections (`backlog`, `active`, `later`).
- Add, update, delete, move, and search tasks.  
- Interactive CLI assistant (`client.py`) with **Agent + MCP Server** integration.  
- SSE (Server-Sent Events) connection between client and server.  
- Clean architecture with environment-based API key loading.  

---

## 🛠️ Tech Stack
- **Python 3.11+**
- **FastAPI** – REST API for tasks
- **FastMCP** – MCP server wrapper
- **Starlette** – lightweight ASGI framework
- **Uvicorn** – ASGI server
- **httpx** – async HTTP client
- **SQLite** – session persistence
- **dotenv** – for managing API keys in `.env`

---

## 📂 Project Structure
MCP_Project/
│── client.py # CLI agent that interacts with MCP server
│── mcp_server.py # SSE-based MCP server
│── main.py # Todo List API
│── openapi.json # API schema used by MCP server
│── requirements.txt # Dependencies
│── .env # Environment variables (ignored by Git)


## ⚙️ Setup & Installation

1. **Clone the repo**

git clone https://github.com/<your-username>/MCP_Project.git
cd MCP_Project
Create & activate a virtual environment


python -m venv venv
# Windows
venv\Scripts\activate
# Linux / Mac
source venv/bin/activate
Install dependencies


pip install -r requirements.txt
Configure environment variables
Create a .env file in the project root:


OPENAI_API_KEY=your-openai-key
ATLASSIAN_API_TOKEN=your-atlassian-token
EMAIL=your-email
JIRA_BASE_URL=https://your-jira-instance.atlassian.net
▶️ Running the Project
1. Start the Todo List API (FastAPI app)


uvicorn main:app --reload --port 8000
Open http://127.0.0.1:8000/docs for Swagger UI.

2. Start the MCP Server

python mcp_server.py
This will expose SSE on: http://127.0.0.1:8082/sse

3. Run the Client

python client.py
Type messages, and the assistant will process them using the MCP server and Todo API.
Type exit to quit.

📌 Example Usage
Add a Task


POST /tasks/backlog
{
  "title": "Finish project",
  "description": "Write final documentation",
  "status": "todo"
}
Move a Task


POST /tasks/move
{
  "taskId": "1234-abcd",
  "fromSection": "backlog",
  "toSection": "active"
}
Interactive Client


User: Show me all tasks
Assistant: Here are the tasks grouped by section...
🛡️ Security Notes
Secrets like API tokens must not be hardcoded in code.

Store sensitive values in .env (already .gitignored).

Rotate tokens if they were exposed in commits.

