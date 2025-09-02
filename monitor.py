import asyncio
import os

import docker
import psutil
import requests
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

ENVIRONMENT = os.getenv("ENVIRONMENT", "staging")  # default staging

CPU_THRESHOLD = int(os.getenv("CPU_THRESHOLD", 80))
MEM_THRESHOLD = int(os.getenv("MEM_THRESHOLD", 80))

BACKEND_URL = os.getenv("BACKEND_URL")
FRONTEND_URL = os.getenv("FRONTEND_URL")

bot = Bot(token=TELEGRAM_TOKEN)


async def send_alert(message):
    try:
        prefix = "🚀 [Production]" if ENVIRONMENT == "production" else "🧪 [Staging]"
        await bot.send_message(chat_id=CHAT_ID, text=f"{prefix} {message}")
        print("✅ Alert sent:", message)
    except Exception as e:
        print("❌ Failed to send alert:", e)


def check_docker_containers():
    client = docker.from_env()
    unhealthy = []
    for container in client.containers.list():
        status = container.attrs['State']['Status']
        name = container.name
        if status != "running":
            unhealthy.append(name)
    return unhealthy


def check_cpu_memory():
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    if cpu > CPU_THRESHOLD or memory > MEM_THRESHOLD:
        return cpu, memory
    return None


def check_backend_health():
    try:
        response = requests.get(BACKEND_URL)
        if response.status_code != 200:
            return f"❌ Django Health Check Failed: {response.status_code}"
    except Exception as e:
        return f"❌ Error checking Django: {e}"
    return None


def check_frontend_health():
    try:
        response = requests.get(FRONTEND_URL)
        if response.status_code != 200:
            return f"❌ Next.js Health Check Failed: {response.status_code}"
    except Exception as e:
        return f"❌ Error checking Next.js: {e}"
    return None


async def main():
    unhealthy = check_docker_containers()
    if unhealthy:
        await send_alert(f"🚨 Unhealthy Docker Containers: {', '.join(unhealthy)}")

    usage = check_cpu_memory()
    if usage:
        cpu, mem = usage
        await send_alert(f"⚠️ High Usage Alert: CPU {cpu}%, RAM {mem}%")

    backend_msg = check_backend_health()
    if backend_msg:
        await send_alert(backend_msg)

    # frontend_msg = check_frontend_health()
    # if frontend_msg:
    #     await send_alert(frontend_msg)

    print("Monitoring checks completed.")


if __name__ == "__main__":
    asyncio.run(main())
