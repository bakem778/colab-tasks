import discord
from discord.ext import commands
import json
import os
import asyncio
import datetime

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {{bot.user}}")
    await send_task_notifications()

async def send_task_notifications():
    try:
        with open("tasks.json", "r", encoding="utf-8") as f:
            tasks = json.load(f)
        today = datetime.date.today()
        upcoming = []
        mentions = set()

        for task in tasks:
            due = datetime.date.fromisoformat(task["due"])
            delta = (due - today).days
            if not task["done"] and 0 <= delta <= 3:
                upcoming.append(task)
                if task.get("discord_id"):
                    mentions.add(task["discord_id"])

        if upcoming:
            channel = bot.get_channel(int(os.environ["CHANNEL_ID"]))
            mention_str = " ".join(f"<@{uid}>" for uid in mentions)
            msg = f"{mention_str}\n**⏰ 3일 이내 마감 예정 과제 알림**\n"
            for t in upcoming:
                msg += f"- **{{t['subject']}}**: {{t['description']}} (마감일: {{t['due']}})\n"
            await channel.send(msg)

    except Exception as e:
        print("Error sending notifications:", e)

bot.run(os.environ["DISCORD_TOKEN"])
