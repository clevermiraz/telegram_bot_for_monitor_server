# Telegram Server Monitor Bot

This is a simple Python script to monitor your server running Docker, Django, and Next.js. It sends alerts to your Telegram account via a Telegram Bot when issues are detected such as:

-   Docker containers not running
-   High CPU or RAM usage
-   Backend (Django) health check failures
-   (Optional) Frontend (Next.js) health check failures

---

## Features

-   Monitors Docker container status
-   Checks CPU and memory usage
-   Checks backend health endpoint status
-   Sends alert messages to your Telegram account via bot

---

## Requirements

-   Python 3.7+
-   Docker running locally (for Docker container checks)
-   Telegram bot token and your Telegram user chat ID
-   Dependencies listed in `requirements.txt` (or install manually)

---

## Setup

1. Clone the repository or copy the script files.

2. Create a `.env` file in the project root with:

    ```env
    TELEGRAM_BOT_TOKEN=your-telegram-bot-token-from-botfather
    TELEGRAM_CHAT_ID=your-telegram-user-chat-id

    ```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the monitoring script:

```bash
python monitor.py
```
