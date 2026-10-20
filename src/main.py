# OneUBot
# https://github.com/CodCatDev/OneUBot
# APACHE 2.0 LICENSE

from config import *

from pyrogram.client import Client
from pyrogram import filters, enums
from pyrogram.types import Message
import pythonping as ping
import psutil
import time
from pathlib import Path
from platform import python_version, system, machine, release

sessionPath = Path(__file__).resolve().parent / "sessions"
sessionPath.mkdir(exist_ok=True)

sessionFile = sessionPath / "OneUBot"
systemVersion = f"{system()} {release()} ({machine()}) | Python {python_version()}"

app = Client(
    str(sessionFile),
    api_id=apiId,
    api_hash=apiHash,
    phone_number=number,
    device_model=f"OneUBot v{version}",
    system_version=system(),
    app_version=systemVersion,
    lang_code="ru",
)

@app.on_start()
async def start(client):
    print("OneUBot started!")
    print(systemVersion)

def formatTime(seconds_count: int) -> str:
    days, remainder = divmod(seconds_count, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    uptime_parts = []
    if days > 0:
        uptime_parts.append(f"{days}д")
    if hours > 0 or days > 0:
        uptime_parts.append(f"{hours}ч")
    if minutes > 0 or hours > 0 or days > 0:
        uptime_parts.append(f"{minutes}м")
    uptime_parts.append(f"{seconds}с")
    
    return " ".join(uptime_parts)

def pingServer():
    r = ping.ping(pingDomain, count=1)
    return r.rtt_avg_ms

@app.on_message(filters.command("server", prefixes=".") & filters.me)
async def serverStatus(client: Client, message: Message):
    await message.edit(
        f"<blockquote>{e.wait} Замеряем данные...</blockquote>",
        parse_mode=enums.ParseMode.HTML
    )
    bannerOne = f"{e.banner.one}{e.banner.two}"
    bannerTwo = f"{e.banner.three}{e.banner.four}"
    ms = pingServer()
    uptime = formatTime(int(time.time() - psutil.boot_time()))
    await message.edit(
        f"<blockquote>{e.server} OneUBot v{version}</blockquote>" \
        f"\n<blockquote>{bannerOne}   <b>Ping:</b> <i>{ms}ms</i>" \
        f"\n{bannerTwo}   <b>Uptime:</b> <i>{uptime}</i></blockquote>",
        parse_mode=enums.ParseMode.HTML
    )


app.run()