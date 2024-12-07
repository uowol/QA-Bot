import os
from fastapi import FastAPI, Request
from app.slack.bot import slack_event_handler
from app.selenium.scraper import ChatGPTScraper

CHROME_SUBPROCESS_PATH = os.getenv(
    "CHROME_SUBPROCESS_PATH",
    r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chromeCookie"',
)
SUBPROCESS_PORT = os.getenv("SUBPROCESS_PORT", 9222)

app = FastAPI()
scraper = ChatGPTScraper(
    subprocess_path=CHROME_SUBPROCESS_PATH, subprocess_port=SUBPROCESS_PORT
)  # TODO: Linux에서 실행할 수 있도록 수정


@app.post("/slack/events")
async def slack_events(request: Request):
    headers = request.headers
    if headers.get("X-Slack-Retry-Num"):
        return {"status": "ok"}  # 재시도 요청 무시

    event_data = await request.json()

    if (
        "challenge" in event_data
    ):  # Slack sends a challenge event when the server is first connected
        return {"challenge": event_data["challenge"]}

    response = slack_event_handler(event_data, scraper)

    return {
        "status": "ok"
    }  # slack에게 응답을 보내지 않으면 계속해서 같은 이벤트를 받음