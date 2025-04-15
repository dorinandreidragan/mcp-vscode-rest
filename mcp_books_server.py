import config
from fastapi_mcp import FastApiMCP
from books_server import app
import uvicorn

BASE_URL = config.WEB_API_URL

mcp = FastApiMCP(
    app,
    name="Books Server",
    description="A simple book management server",
    base_url=BASE_URL,
    describe_all_responses=True,
    describe_full_response_schema=True,
)

mcp.mount()

if __name__ == "__main__":
    uvicorn.run(app, port=5000)
