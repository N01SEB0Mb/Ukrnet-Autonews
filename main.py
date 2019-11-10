# created by noisebomb

# coding=utf-8

import json
import source
import asyncio
from time import sleep
from aiogram import Bot
from aiogram.utils.markdown import hbold, hlink


async def checker():
    p = source.Parser(config)

    while True:
        with open("last.news", "rt") as last_file:
            try:
                last = set(map(int, last_file.read().split(" ")))
            except ValueError:
                last = set()

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

        with open("last.news", "wt") as last_file:
            last_file.write(" ".join(map(lambda x: str(x["Id"]), last_update)))

        await asyncio.sleep(config["sleep"])


if __name__ == "__main__":
    with open("config.json", "rb") as config_file:
        config = json.load(config_file)

    with open("tg.json", "rb") as tg_file:
        tg_info = json.load(tg_file)

    while True:
        try:
            bot = Bot(tg_info["bot_token"])
            aio_loop = asyncio.get_event_loop()

            try:
                aio_loop.run_until_complete(checker())
            except KeyboardInterrupt:
                pass
            except BaseException as err:
                print(err)
            finally:
                aio_loop.run_until_complete(bot.close())
        except BaseException as err:
            print(err)
        finally:
            sleep(config["retry sleep"])
