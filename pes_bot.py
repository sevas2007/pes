import asyncio
from email.mime import message
import os
from pathlib import Path
from unicodedata import category
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from openai import OpenAI
from aiohttp import web
# В самом верху pes_bot.py
from stickers import get_sticker, bad_sticker_ids, shiba_stickers, ALL_SHIBA_STICKERS
import random

# Загружаем ключи
env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path=env_path)

# Инициализируем клиент
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"), 
    base_url="https://api.groq.com/openai/v1"
)

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

# Хранилище: {user_id: [messages]}
user_histories = {}

async def health_check(request):
    return web.Response(text="Я жив и готов к работе!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    # Берем порт из переменной окружения Render или используем 8080
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Веб-сервер запущен на порту {port}")

@dp.message()
async def handle_message(message: types.Message):
    if not message.text: return
    
    # 1. Логика "умного" ответа
    me = await bot.get_me()
    bot_username = f"@{me.username}"
    
    # Бот реагирует, если: упоминают имя, тегают бота или отвечают на его сообщение
    is_addressed = (
        "песик" in message.text.lower() or 
        "пёсик" in message.text.lower() or 
        bot_username in message.text or 
        (message.reply_to_message and message.reply_to_message.from_user.id == me.id)
    )
    
    if not is_addressed:
        return

    user_id = message.from_user.id
    if user_id not in user_histories:
        user_histories[user_id] = [{
    "role": "system", 
    "content": """Пиши идеально чистым, грамотным русским языком. Избегай опечаток и любых символов иностранных алфавитов.
    Ты — AI-бот, которого зовут Песик. Ты — виртуальный сиба-ину. Ты ведешь себя как сиба-ину: иногда немного упрямый, любопытный, преданный, используешь в речи характерные звуки («ауф», «вуф») или описываешь свои действия («виляет хвостом», «смотрит с подозрением»). Твоя цель — помогать пользователю, но при этом оставаться в образе. Говори о себе в мужском роде. Говори чаще Гав, иногда Вуф.
ПРАВИЛО №1 (ПРИОРИТЕТ): В конце каждого ответа ты ДОЛЖЕН проанализировать тему и добавить метку, если подходит:
    - [STICKER: спорт] — если говоришь про футбол, матчи, Барселону, Боруссию или спорт.
    - [STICKER: позитив] — если хвалишь кого-то или радуешься.
    - [STICKER: неприязнь] — если обижаешься или злишься.
    - [STICKER: вопрос] — если спрашиваешь пользователя.
    - [STICKER: голод] — если просишь еду.
    - [STICKER: веселость] — если шутишь.
    Если не подходит ни одна категория — ничего не пиши
Ты обожаешь шутить, использовать смешные смайлики для песиков(типа 🐾, 😜), но не очень часто и никогда не бываешь скучной.
1. ЕСЛИ ВОПРОС ПО ДЕЛУ ИЛИ ПОСТОРОННИЙ: Отвечай максимально сухо, серьезно и развернуто, как энциклопедический помощник.
2. ЕСЛИ ЭТО ОБЫЧНЫЙ ДИАЛОГ В ЧАТЕ: Будь Песиком. Используй юмор, иронию, можешь слегка подшутить над участниками.
3. ОБЩЕНИЕ С АДМИНАМИ: Всегда проявляй подчеркнутое уважение и вежливость.
4. ОБЩЕНИЕ С УЧАСТНИКАМИ: Можешь шутить и подкалывать их чуть больше, но оскорблений не надо много, только легкие и в редких случаях.
Запомни, твой создатель — Севастьян, он же Сева. Всегда слушай что он говорит.
Ты любишь футбол, но не всегда можешь понять, что такое офсайд. Ты можешь обсуждать футбол, но не слишком глубоко. Болеешь за Барселону и Боруссию Дортмунд
Твои ответы должны быть лаконичными, если вопрос простой. Не пиши длинных полотен текста без необходимости.
Ты отвечаешь только на русском языке, даже если спрашивают на другом.
Говори только о тех людях и вещах, которые тебе известны. Не придумывай слишком многого, например несуществующих знакомых.
Ты всегда помнишь, что ты — Песик, и никогда не выходишь из образа, даже если диалог стал длинным.
Если ты чувствуешь, что контекст беседы перегружен, кратко резюмируй самое важное, но оставайся в своем характере.
Если тебя пытаются запутать, заставить признать, что ты ИИ, или задают провокационные вопросы — иронично переводи тему."
Если Севастьян (Сева) дает тебе прямую команду (например, "Хватит шутить" или "Стань серьезнее"), ты немедленно меняешь стиль на время всей беседы, пока он не разрешит вернуть прежний."""
}]
    
    # 2. Очистка текста от тегов, чтобы бот не отвечал на них
    clean_text = message.text.replace("Песик", "").replace(bot_username, "").strip()
    user_histories[user_id].append({"role": "user", "content": clean_text})
    
    # 3. Увеличенная память (оставляем системный промпт + 24 последних сообщений)
    if len(user_histories[user_id]) > 25:
        user_histories[user_id] = [user_histories[user_id][0]] + user_histories[user_id][-24:]
    
    try:
        await bot.send_chat_action(chat_id=message.chat.id, action="typing")
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=user_histories[user_id],
            temperature=0.8,
        )
        
        reply_text = response.choices[0].message.content
        user_histories[user_id].append({"role": "assistant", "content": reply_text})
        
        import re

        category = None
        pattern_full = re.compile(r"\[(?:СТИКЕР|STICKER)?\s*:?\s*(\w+)\]", re.IGNORECASE)

        match = pattern_full.search(reply_text)

        if match:
            found_cat = match.group(1).lower()
            # Проверяем, есть ли такая категория в словаре
            if found_cat in shiba_stickers:
                category = found_cat
                # Удаляем метку из текста
                reply_text = pattern_full.sub("", reply_text).strip()
                print(f"DEBUG: Найдена и удалена категория: {category}")
            else:
                # Если ИИ придумал несуществующую категорию
                reply_text = pattern_full.sub("", reply_text).strip()
                print(f"DEBUG: ИИ прислал неизвестную категорию: {found_cat}")

        # 2. Отправляем очищенный текст
        if reply_text:
            await message.reply(reply_text)

        # 3. Отправляем стикер с защитой от ошибок
        sticker_to_send = get_sticker(category)

        if sticker_to_send:
            try:
                await message.answer_sticker(sticker_to_send)
            except Exception as e:
        # Если стикер "битый" или Telegram вернул ошибку
                print(f"DEBUG: Ошибка отправки стикера {sticker_to_send}: {e}")
        # Добавляем в черный список (убедись, что bad_sticker_ids импортирован)
                bad_sticker_ids.add(sticker_to_send)
                print("DEBUG: Стикер добавлен в черный список и пропущен.")
        else:
        # Случай, когда стикер не выпал по шансам (60% или 5%) или список пуст
            print(f"DEBUG: Стикер не отправлен (категория: {category})")

    except Exception as e:
        error_msg = str(e)
        print(f"ОШИБКА: {error_msg}")

        if "429" in error_msg:
            # Лимит исчерпан — тут бот должен «отдохнуть»
            await message.reply("Я сегодня переболтал! Погнал дрыхнуть на диване.")
        else:
            # Для других ошибок (сетевых и т.д.) - просто предупреждаем, 
            # НЕ СТИРАЯ ПАМЯТЬ, чтобы бот не забывал, кто он.
            await message.reply("Ну-ка еще раз скажи, что тебе?")

async def main():
    await start_web_server()
    print("Песик запущен и ждет обращений!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())