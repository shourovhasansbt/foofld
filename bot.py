import telebot
import requests
import time

# আপনার টেলিগ্রাম বট টোকেন এবং ওয়েবসাইটের গোপন লিংক
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
        
        # ওয়েবসাইটে ডাটা পাঠানো
        params = {'key': SECRET_KEY, 'type': 'income', 'order_id': order_id, 'amount': amount}
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(API_URL, params=params, headers=headers).json()
        
        if res.get('status') == 'success':
            bot.reply_to(message, f"✅ Income Added to Website!\nOrder: {order_id}\nAmount: ৳{amount}")
        else:
            bot.reply_to(message, f"❌ API Error: {res.get('message')}")
    except Exception as e:
        bot.reply_to(message, "⚠️ Error processing request!")

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
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(API_URL, params=params, headers=headers).json()
        
        if res.get('status') == 'success':
            bot.reply_to(message, f"📉 Expense Added to Website!\nDetails: {desc}\nAmount: ৳{amount}")
        else:
            bot.reply_to(message, f"❌ API Error: {res.get('message')}")
    except Exception as e:
        bot.reply_to(message, "⚠️ Error processing request!")

print("🚀 Bot is starting...")

# বট যেন কখনোই বন্ধ না হয় তার জন্য Loop
while True:
    try:
        bot.polling(none_stop=True, timeout=60)
    except Exception as e:
        print(f"Connection Error, retrying in 5 seconds... {e}")
        time.sleep(5)
