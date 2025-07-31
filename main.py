from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
import asyncio
import os

import links
import bd


bot = Bot(token=os.environ['BOT_TOKEN'])
dp = Dispatcher()


@dp.message(F.text == "/start")
async def start_command(message: Message):
    await message.reply("Hi!\nI'm CinemaBot!\nWrite title of any film and\
                         I will try to find information about it and a link to watch online.")


@dp.message(F.text == "/help")
async def help_command(message: Message):
    await message.reply("Write title of a film without any extra symbols. \
                        Commands: /history to see your requests, /stats to see statistics")


@dp.message(F.text == "/history")
async def history_command(message: Message):
    user_id = message.from_user.id
    history = bd.get_history(user_id)
    if not history:
        await message.reply("No history yet")
    else:
        await message.reply("\n".join(history))


@dp.message(F.text == "/stats")
async def stats_command(message: Message):
    user_id = message.from_user.id
    stats = bd.get_stats(user_id)
    if not stats:
        await message.reply("No statistics yet")
    else:
        response = "\n".join([f"{film}: {count}" for film, count in stats.items()])
        await message.reply(response)


@dp.message()
async def movie_handler(message: Message):
    user_id = message.from_user.id
    query = message.text
    movie = await links.search_movie(query)
    bd.save_query(user_id, query, movie['title'])
    if 'poster' in movie:
        photo_url = movie['poster']
        caption = (
                    f"Title: {movie['title']}\n"
                    f"Rating: {movie['rating']}\n"
                    f"Description: {movie['description']}\n"
                    f"Link: {movie['link']}"
                )
        await bot.send_photo(message.chat.id, photo_url, caption=caption)
    else:
        caption = (
                    f"Title: {movie['title']}\n"
                    f"Rating: {movie['rating']}\n"
                    f"Description: {movie['description']}\n"
                    f"Link: {movie['link']}"
                )
        await message.reply(caption)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    bd.init_db()
    asyncio.run(main())
