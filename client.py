import asyncio
import os
import shutil
import subprocess
import time
from typing import Any

from agents import Agent, Runner, gen_trace_id, trace, WebSearchTool, SQLiteSession, ItemHelpers
from agents.mcp import MCPServer, MCPServerSse
from agents.model_settings import ModelSettings

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

async def run(mcp_server: MCPServer):
    # session = SQLiteSession("JIRA_session2", "jira_session2.db")
    session = SQLiteSession("TODO_session", "todo_session.db")
    jira_agent = Agent(
        name="Jira Assistant",
        instructions="You're a helpful assistant, help user with his questions. Use the mcp server, only if its needed.",
        mcp_servers=[mcp_server],
        model_settings=ModelSettings(tool_choice="required"),
    )

    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break

        print("=== Run starting ===")
        result = await Runner.run(
            jira_agent,
            user_input,
            session=session
        )

        print(f"Assistant: {result.final_output}")

async def main():
    async with MCPServerSse(
        name="SSE Python Server",
        params={
            "url": "http://localhost:8082/sse",
        },
    ) as server:
        trace_id = gen_trace_id()
        with trace(workflow_name="SSE Example", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n")
            await run(server)


if __name__ == "__main__":
    # Let's make sure the user has uv installed
    if not shutil.which("uv"):
        raise RuntimeError(
            "uv is not installed. Please install it: https://docs.astral.sh/uv/getting-started/installation/"
        )
    asyncio.run(main())