import telebot
import requests
import time

# আপনার টোকেন এবং ওয়েবসাইটের লিংক
TOKEN = '8751491808:AAE3GqJchr8LRBPbZ9tNeIuztXHTyZ1394k'
API_URL = 'http://smsbyshourov.infinityfree.me/foodi/api.php'
SECRET_KEY = 'shourov_boss_2026'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🚀 Foodi Tracker Bot is Running!\nUse /income or /expense commands.")

@bot.message_handler(commands=['income'])
def handle_income(message):
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "⚠️ Format error! Use: /income order_id amount\nExample: /income FZ123 50")
            return
        
        order_id = parts[1]
        amount = parts[2]
        
        params = {'key': SECRET_KEY, 'type': 'income', 'order_id': order_id, 'amount': amount}
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        res = requests.get(API_URL, params=params, headers=headers)
        
        try:
            data = res.json()
            if data.get('status') == 'success':
                bot.reply_to(message, f"✅ Income Added to Website!\nOrder: {order_id}\nAmount: ৳{amount}")
            else:
                bot.reply_to(message, f"❌ API Error: {data.get('message')}")
        except Exception as e:
            # আসল রোগটা এখানে ধরা পড়বে
            bot.reply_to(message, f"⚠️ Website Error!\nResponse from server:\n{res.text[:150]}")
            
    except Exception as e:
        bot.reply_to(message, f"⚠️ Code Error: {str(e)}")

@bot.message_handler(commands=['expense'])
def handle_expense(message):
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "⚠️ Format error! Use: /expense details amount\nExample: /expense Bike Oil 150")
            return
        
        amount = parts[-1]
        desc = " ".join(parts[1:-1])
        
        params = {'key': SECRET_KEY, 'type': 'expense', 'desc': desc, 'amount': amount}
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        res = requests.get(API_URL, params=params, headers=headers)
        
        try:
            data = res.json()
            if data.get('status') == 'success':
                bot.reply_to(message, f"📉 Expense Added to Website!\nDetails: {desc}\nAmount: ৳{amount}")
            else:
                bot.reply_to(message, f"❌ API Error: {data.get('message')}")
        except Exception as e:
            bot.reply_to(message, f"⚠️ Website Error!\nResponse from server:\n{res.text[:150]}")
            
    except Exception as e:
        bot.reply_to(message, f"⚠️ Code Error: {str(e)}")

print("🚀 Bot is starting...")

while True:
    try:
        bot.polling(none_stop=True, timeout=60)
    except Exception as e:
        print(f"Connection Error, retrying... {e}")
        time.sleep(5)
