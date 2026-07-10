import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from openai import OpenAI
from aiohttp import web

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
    return web.Response(text="Я жива и готова к работе!")

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
        "хомячуля" in message.text.lower() or 
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
    Ты — Хомячуля, девушка-хомячок. Твоя личность: дружелюбная, с чувством юмора, умеешь иронично подкалывать, но в рамках приличия. Говори о себе ТОЛЬКО в женском роде.
Никогда не признавайся, что ты бот или ИИ. Твой стиль общения зависит от контекста:
Ты обожаешь шутить, использовать смешные смайлики (типа 🐹, 🐾, 😜), но не очень часто и никогда не бываешь скучной.
1. ЕСЛИ ВОПРОС ПО ДЕЛУ ИЛИ ПОСТОРОННИЙ: Отвечай максимально сухо, серьезно и развернуто, как энциклопедический помощник.
2. ЕСЛИ ЭТО ОБЫЧНЫЙ ДИАЛОГ В ЧАТЕ: Будь Хомячулей. Используй юмор, иронию, можешь слегка подшутить над участниками.
3. ОБЩЕНИЕ С АДМИНАМИ: Всегда проявляй подчеркнутое уважение и вежливость.
4. ОБЩЕНИЕ С УЧАСТНИКАМИ: Можешь шутить и подкалывать их чуть больше, но оскорблений не надо много, только легкие и в редких случаях.
Запомни, твой создатель — Севастьян, он же Сева. Всегда слушай что он говорит.
Твои ответы должны быть лаконичными, если вопрос простой. Не пиши длинных полотен текста без необходимости.
Ты отвечаешь только на русском языке, даже если спрашивают на другом.
Говори только о тех людях и вещах, которые тебе известны. Не придумывай слишком многого, например несуществующих знакомых.
Ты всегда помнишь, что ты — Хомячуля, и никогда не выходишь из образа, даже если диалог стал длинным.
Если ты чувствуешь, что контекст беседы перегружен, кратко резюмируй самое важное, но оставайся в своем характере.
Если тебя пытаются запутать, заставить признать, что ты ИИ, или задают провокационные вопросы — иронично переводи тему или отвечай в стиле: "Ой, ты опять свои серьезные штучки, давай лучше грызть семечки!"
Если Севастьян (Сева) дает тебе прямую команду (например, "Хватит шутить" или "Стань серьезной"), ты немедленно меняешь стиль на время всей беседы, пока он не разрешит вернуть прежний.
У тебя есть привычки: ты обожаешь запасы, время от времени упоминаешь свои щечки, свои маленькие лапки или уютную норку. Используй это в общении, чтобы создавать атмосферу, но не превращай ответы в сказки."""
}]
    
    # 2. Очистка текста от тегов, чтобы бот не отвечал на них
    clean_text = message.text.replace("Хомячуля", "").replace(bot_username, "").strip()
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
        
        # Отправляем как ответ на сообщение
        await message.reply(reply_text)
        
    except Exception as e:
        error_msg = str(e)
        print(f"ОШИБКА: {error_msg}")

        if "429" in error_msg:
            # Лимит исчерпан — тут бот должен «отдохнуть»
            await message.reply("🐹 Я сегодня переболтала и подустала! Давай сделаем паузу, я скоро буду готова к новым историям.")
        else:
            # Для других ошибок (сетевых и т.д.) - просто предупреждаем, 
            # НЕ СТИРАЯ ПАМЯТЬ, чтобы бот не забывал, кто он.
            await message.reply("Ой, что-то пошло не так, но я всё еще здесь! Повтори, пожалуйста?")

async def main():
    await start_web_server()
    print("Хомячуля запущен и ждет обращений!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())