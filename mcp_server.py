import uvicorn
import requests
import httpx
from starlette.applications import Starlette
from starlette.routing import Mount
from fastmcp import FastMCP
import json

with open("openapi.json", "r") as f:
        spec = json.load(f)
# BASE_URL = "http://127.0.0.1:8000"

# Fetch your FastAPI OpenAPI schema
#spec = requests.get(SPEC_URL, timeout=5).json()

# Build an MCP server from that spec.
# Pass an AsyncClient so generated tools can call your API.


JIRA_BASE_URL = "https://your-jira-base-url"
EMAIL = "your-email"
API_TOKEN = "your-api-token"

# # Create an async HTTP client with basic auth for all requests
client = httpx.AsyncClient(
base_url=JIRA_BASE_URL,
auth=(EMAIL, API_TOKEN),
headers={"Accept": "application/json"}
)

mcp = FastMCP.from_openapi(
    openapi_spec=spec,
    client=httpx.AsyncClient(base_url=JIRA_BASE_URL),
)

# Expose an SSE endpoint at /sse
#app = Starlette(routes=[Mount("/", app=mcp.sse_app())])

if __name__ == "__main__":
    uvicorn.run(mcp.sse_app(), host="127.0.0.1", port=8082)
