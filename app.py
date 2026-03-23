import telebot
import requests
from io import BytesIO

# ТВОИ КЛЮЧИ И ТОКЕНЫ
TOKEN = "8769201612:AAFV-F0AX5YLHjqhkcxpZwKTuubpR6HUKgI"
PROXY_KEY = "sk-0Pa1swG0k5kbhQYSCM6NOdVWQ5i4Qd7D"
URL_IMAGE = "https://api.proxyapi.ru/openai/v1/images/generations"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda m: True)
def draw(m):
    # 1. Отправляем сообщение "Принято! Рисую..."
    msg = bot.send_message(m.chat.id, "🎨 Принято! Рисую, подождите немного...")
    try:
        # 2. Формируем запрос к OpenAI через прокси
        headers = {"Authorization": f"Bearer {PROXY_KEY}"}
        payload = {"model": "dall-e-3", "prompt": m.text, "size": "1024x1024"}
        res = requests.post(URL_IMAGE, json=payload, headers=headers, timeout=120)

        if res.status_code == 200:
            # 3. Получаем URL картинки
            img_url = res.json()['data'][0]['url']

            # 4. СКАЧИВАЕМ КАРТИНКУ СЕБЕ В ПАМЯТЬ
            img_data = requests.get(img_url).content

            # 5. ОТПРАВЛЯЕМ КАРТИНКУ КАК ФАЙЛ ( BytesIO)
            bot.send_photo(m.chat.id, BytesIO(img_data))

            # 6. Удаляем временное сообщение "Принято!"
            bot.delete_message(m.chat.id, msg.message_id)
        else:
            bot.reply_to(m, f"❌ Ошибка API: {res.text}")
    except Exception as e:
        bot.reply_to(m, f"⚠️ Ошибка: {e}")

if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)
