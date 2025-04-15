from dotenv import load_dotenv
import os

load_dotenv()

WEB_API_PORT = 5000
WEB_API_URL = f"http://localhost:{WEB_API_PORT}"
# LLM_API_URL = "http://localhost:8080/api/chat/completions"
# LLM_API_KEY = os.getenv("OPEN_WEBUI_API_KEY")
