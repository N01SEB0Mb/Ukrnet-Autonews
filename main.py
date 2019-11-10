# created by noisebomb

# coding=utf-8

import asyncio
from asyncio import sleep
from aiogram import Bot
from aiogram.utils.markdown import hbold, hlink, hide_link

import json
import parser
from time import sleep

with open("config.json", "rb") as config_file:
    config = json.load(config_file)

with open("tg.json", "rb") as tg_file:
    tg_info = json.load(tg_file)


async def checker():
    p = parser.Parser(config)
    while True:
        with open("last.news", "rt") as last_file:
            last = {parser.New(json.loads(line.replace("\n", ""))) for line in last_file.readlines()}

        last_update = p.get_last()
        news = last_update - last

        for new in news:
            info = p.get_info(new)
            if info:
                title, description, image = info
                msg = f'{hbold(title)}\n\n{description}{hlink("Подробнее", new["Url"])}'

                if image:
                    await bot.send_photo(tg_info["channel_id"], image, caption=msg, parse_mode="HTML")
                else:
                    await bot.send_message(tg_info["channel_id"], msg, parse_mode="HTML")
            else:
                last_update.remove(new)

        with open("last.news", "wt") as last_file:
            last_file.write("\n".join(map(str, last_update)))

        await asyncio.sleep(config["sleep"])


if __name__ == "__main__":
    bot = Bot(tg_info["bot_token"])
    aio_loop = asyncio.get_event_loop()

    try:
        aio_loop.run_until_complete(checker())
    except KeyboardInterrupt:
        pass
    finally:
        aio_loop.run_until_complete(bot.close())
