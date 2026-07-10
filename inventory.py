import telebot
import time

# Ваш токен
bot = telebot.TeleBot("8532980130:AAHFwn4Xihc42h-ZHz0hLcaysvZiY8zZSz4")
# Имя пака
sticker_pack_name = "Tblchepes_by_fStikBot"

def show_me_stickers():
    try:
        sticker_set = bot.get_sticker_set(sticker_pack_name)
        print(f"Всего стикеров: {len(sticker_set.stickers)}")
        
        # Отправляем стикеры в чат (замените 'ВАШ_ID' на ваш ID в Telegram)
        # Узнать свой ID можно у бота @userinfobot
        my_chat_id = "1449076200" 
        
        for sticker in sticker_set.stickers:
            # Бот пришлет стикер
            bot.send_sticker(my_chat_id, sticker.file_id)
            # И сразу текстом его ID
            bot.send_message(my_chat_id, f"ID: `{sticker.file_id}`", parse_mode="Markdown")
            
            # Небольшая пауза, чтобы Telegram не заблокировал за спам
            time.sleep(1)
            
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    show_me_stickers()