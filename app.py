import telebot
import requests

# ТВОИ ДАННЫЕ
TOKEN = "8769201612:AAFV-F0AX5YLHjqhkcxpZwKTuubpR6HUKgI"
PROXY_KEY = "sk-0Pa1swG0k5kbhQYSCM6NOdVWQ5i4Qd7D"
URL_IMAGE = "https://api.proxyapi.ru/openai/v1/images/generations"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda m: True)
def draw(m):
    bot.send_message(m.chat.id, "🎨 Принято! Рисую...")
    try:
        headers = {"Authorization": f"Bearer {PROXY_KEY}"}
        payload = {"model": "dall-e-3", "prompt": m.text, "size": "1024x1024"}
        res = requests.post(URL_IMAGE, json=payload, headers=headers, timeout=120)

        if res.status_code == 200:
            bot.send_photo(m.chat.id, res.json()['data'][0]['url'])
        else:
            bot.send_message(m.chat.id, f"❌ Ошибка API: {res.text}")
    except Exception as e:
        bot.send_message(m.chat.id, f"⚠️ Ошибка: {e}")

if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)
