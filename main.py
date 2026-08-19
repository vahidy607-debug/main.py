import telebot
from telebot import types
import sqlite3
import time
import random
import threading

API_TOKEN = '8963819793:AAH5UFaQOUN65IkWpCT_nJiLPS7_KvPAdRY'
ADMIN_ID = 8624115573
CHANNEL_LINK = 'https://t.me/bot_py_Hoshmand'
CHANNEL_USERNAME = '@bot_py_Hoshmand'

bot = telebot.TeleBot(API_TOKEN)

conn = sqlite3.connect('group_bot.db', check_same_thread=False)
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS groups (chat_id INTEGER PRIMARY KEY, title TEXT, added_at INTEGER)')
cur.execute('CREATE TABLE IF NOT EXISTS settings (chat_id INTEGER, key TEXT, value TEXT, PRIMARY KEY (chat_id, key))')
cur.execute('CREATE TABLE IF NOT EXISTS warnings (id INTEGER PRIMARY KEY AUTOINCREMENT, chat_id INTEGER, user_id INTEGER, reason TEXT, warned_at INTEGER)')
cur.execute('CREATE TABLE IF NOT EXISTS filters (id INTEGER PRIMARY KEY AUTOINCREMENT, chat_id INTEGER, keyword TEXT, response TEXT)')
conn.commit()

JOKES = [
"یه روزه میمون میره باشگاه، مربی میگه: چرا اومدی؟ میمونه میگه: میخوام موز نخورم 😅",
"استاد: شاگرد اگه یه سیب داشته باشی و دو تا بشه، چند تا داری؟ شاگرد: سه تا! استاد: نه! شاگرد: چرا؟ سیب اول + دو تا سیب = 3 تا! 🍎",
"مادر: بچه چرا خوابت نمیبره؟ بچه: چون میدونم فردا باید برم مدرسه مادر: پس منم نمیخوابم، چون میدونم فردا باید بیدار شم 😂",
"یارو میره دکتر، دکتر میگه: چی شده؟ میگه: هر وقت آب میخورم درد میکنه. دکتر میگه: لیوانت بردار! 💧",
"معلم: اگه 2 تا سیب داشته باشی و 3 تا برداری چی میشه؟ شاگرد: دزدی میشه! 😂",
"زن به شوهرش: چرا وقتی من حرف میزنم خوابت میبره؟ شوهر: چون تو هم مثل قرص خواب‌آوری عزیزم 😴❤️",
"یه روز کرگدن میره آرایشگاه، میگه: فقط شاخمو کوتاه کن! آرایشگر: باشه ولی با این قیمت نمیشه! کرگدن: چرا؟ آرایشگر: چون ماده هم داره! 🦏",
"رفتیم دکتر گفت قرص بخور، نخوردم. گفت چرا؟ گفتم خوشم نمیاد. گفت: پس بمیر! 💊",
"یارو میخواسته ماهی بگیره، قلاب انداخت، ماهی اومد گفت: آب نیست! 🎣",
"دوستم بهم گفت: چرا قدت بلند نیست؟ گفتم: چون پدرم کوتاهه، دیدم جواب داد، به منم نگفتن! 📏"
]

BIOGRAPHIES = [
"🌟 زندگی مثل یه کتابه، هر روز یه صفحه جدید داره. امروزتو خوب بنویس!",
"🌱 برای رسیدن به هر چیزی، اول باید باور کنی که میتونی.",
"🌈 بعد از هر طوفانی، رنگین‌کمان میاد. صبور باش.",
"✨ تو به اندازه‌ی کافی خوب هستی. فقط خودت باورت نیست.",
"🦋 تغییر از درون شروع میشه، نه از بیرون.",
"🌻 لبخند بزن، دنیا به لبخند تو قشنگ‌تره.",
"💪 امروز سخته، فردا بدتر، پس‌فردا عالی میشه!",
"🕊 آرامشتو پیدا کن، بقیه‌اش میاد.",
"🔥 هیچ‌کس نمیتونه به جای تو رویاهاتو بسازه.",
"🌙 شب‌های تاریک، صبح‌های روشن داره."
]

CHALLENGES = [
"🎯 چالش: یه پیام بفرست فقط با ایموجی! 👀",
"🎯 چالش: اولین کلمه‌ای که به ذهنت رسید رو بگو!",
"🎯 چالش: یه جوک بگو، بقیه بگن خندیدن یا نه! 😂",
"🎯 چالش: یه چیزی که امروزت رو خوب کرد بگو! 🌟",
"🎯 چالش: اگه میتونستی یه ابرقهرده باشی، کی میشد؟",
"🎯 چالش: آهنگ مورد علاقه‌ت الان چیه؟ 🎵",
"🎯 چالش: یه چیزی که ازش میترسی بگو! 👻",
"🎯 چالش: اگه 10 میلیون داشتی چیکار میکردی؟ 💰",
"🎯 چالش: 3 تا کلمه که بهترت توصیف میکنه بگو!",
"🎯 چالش: آخرین بار کی گریه کردی و چرا؟ 😢"
]

QUOTES = [
"سعدی: تو نیکی مکن هرچه خواهی به تو، که همه نیک و بدت در جهان برخورد.",
"حافظ: از صدای سخن عشق ندیدم خوش‌تر، یادگاری که در این گنبد دوّار بجاست",
"مولانا: دل من دل من دل من، دل دیوانه‌ی من",
"خیام: آن قصر که بر چرخ همیزد پایه، بود از ملک و مال و زر و سیم خایه",
"سعدی: هر که طاووس خواهد جور هندستان کشد",
"حافظ: مرا عهدیست با جانان که تا جان در بدن دارم",
"سهراب سپهری: چشم‌ها را باید شست، جور دیگر باید دید.",
"فروغ فرخزاد: من از دیار عشق آمده‌ام، من از سرزمین آفتاب.",
"نیما یوشیج: ای گل، گل، گل، ای گل سرخ، تو خوش‌تر از هر چه در گیتی است",
"اخوان ثالث: زمان، گذران نیست، گذر است"
]

WELCOME_MESSAGES = [
"خوش اومدی {name}! 👋 امیدوارم اینجا لحظات خوبی داشته باشی.",
"سلام {name}! 🌟 به گروه خوش اومدی!",
"یه نفر جدید اومد! {name} عزیز خوش اومدی! 🎉",
"هلو {name}! 😊 خوش اومدی به جمع ما!",
"خوش اومدی {name}! 💫 یه گروه باحال پیدا کردی!"
]

def get_setting(chat_id, key, default='on'):
    cur.execute('SELECT value FROM settings WHERE chat_id=? AND key=?', (chat_id, key))
    r = cur.fetchone()
    return r[0] if r else default

def set_setting(chat_id, key, value):
    cur.execute('INSERT OR REPLACE INTO settings (chat_id, key, value) VALUES (?,?,?)', (chat_id, key, value))
    conn.commit()

def is_admin(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ['administrator', 'creator']
    except:
        return False

def is_bot_admin(chat_id):
    try:
        member = bot.get_chat_member(chat_id, bot.get_me().id)
        return member.status in ['administrator', 'creator']
    except:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    text = f"سلام {message.from_user.first_name}! 👋\n\n"
    text += f"من ربات مدیریت گروه {CHANNEL_USERNAME} هستم! 🤖\n\n"
    text += "قابلیت‌های من:\n"
    text += "🛡 ضد اسپم و ضد لینک\n"
    text += "👋 خوش‌آمدگویی خودکار\n"
    text += "😂 جوک و چالش\n"
    text += "📝 بیوگرافی و سخن بزرگان\n"
    text += "⚙️ تنظیمات کامل\n"
    text += "📊 آمار گروه\n"
    text += "🔇 سکوت / بن / اخطار\n"
    text += "🎮 بازی و سرگرمی\n\n"
    text += f"برای دیدن دستورات، /help بزن.\n\n"
    text += f"📢 کانال ما: {CHANNEL_LINK}"
    bot.reply_to(message, text, parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def help_cmd(message):
    text = "📋 دستورات ربات:\n\n"
    text += "مدیریت:\n"
    text += "⚙️ /settings - تنظیمات\n"
    text += "🔇 /mute - سکوت کاربر (ریپلای)\n"
    text += "🔊 /unmute - رفع سکوت (ریپلای)\n"
    text += "🚫 /ban - بن کاربر (ریپلای)\n"
    text += "⚠️ /warn - اخطار (ریپلای)\n"
    text += "🧹 /clean - پاکسازی پیام\n\n"
    text += "سرگرمی:\n"
    text += "😂 /joke - جوک\n"
    text += "🎯 /challenge - چالش\n"
    text += "📝 /bio - بیوگرافی\n"
    text += "💬 /quote - سخن بزرگان\n"
    text += "👤 /me - اطلاعات خودت\n"
    text += "🎲 /dice - تاس\n"
    text += "🔮 /8ball سوال - جادوی 8 توپ\n"
    text += "❤️ /love - عشق سنج (ریپلای)\n\n"
    text += "ابزار:\n"
    text += "📊 /stats - آمار گروه\n"
    text += "🆔 /id - آیدی\n"
    text += "📌 /pin - سنجاق (ریپلای)\n"
    text += "🏷 /tag متن - تگ همه\n"
    text += "🔗 /filter کلمه | جواب - فیلتر کلمه\n"
    text += "ℹ️ /info - اطلاعات کاربر (ریپلای)"
    bot.reply_to(message, text, parse_mode='Markdown')

@bot.message_handler(commands=['settings'])
def settings_cmd(message):
    if message.chat.type == 'private':
        bot.reply_to(message, "❌ این دستور فقط تو گروه کار میکنه.")
        return
    chat_id = message.chat.id
    user_id = message.from_user.id
    if not is_admin(chat_id, user_id):
        bot.reply_to(message, "❌ فقط ادمین‌ها میتونن.")
        return
    text = "⚙️ تنظیمات گروه:\n\n"
    features = {
    'antispam': '🛡 ضد اسپم',
    'antilink': '🔗 ضد لینک',
    'welcome': '👋 خوش‌آمدگویی',
    'challenges': '🎯 چالش خودکار',
    'filters': '🔍 فیلتر کلمات'
    }
    for key, name in features.items():
        status = get_setting(chat_id, key, 'on')
        icon = "✅" if status == 'on' else "❌"
        text += f"{icon} {name}: {status}\n"
    text += "\n🔧 برای تغییر هر گزینه، رو دکمه بزن:"
    mk = types.InlineKeyboardMarkup(row_width=2)
    btns = []
    for key, name in features.items():
        btns.append(types.InlineKeyboardButton(f"{name}", callback_data=f"toggle_{key}"))
    mk.add(*btns)
    bot.send_message(chat_id, text, reply_markup=mk, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda c: c.data.startswith('toggle_'))
def toggle_setting(cb):
    chat_id = cb.message.chat.id
    user_id = cb.from_user.id
    if not is_admin(chat_id, user_id):
        bot.answer_callback_query(cb.id, "❌ فقط ادمین!", show_alert=True)
        return
    key = cb.data.replace('toggle_', '')
    current = get_setting(chat_id, key, 'on')
    new = 'off' if current == 'on' else 'on'
    set_setting(chat_id, key, new)
    bot.answer_callback_query(cb.id, f"{'✅ فعال' if new == 'on' else '❌ غیرفعال'} شد", show_alert=True)
    settings_cmd(cb.message)

@bot.message_handler(commands=['joke'])
def joke(message):
    bot.reply_to(message, f"😂 جوک:\n\n{random.choice(JOKES)}", parse_mode='Markdown')

@bot.message_handler(commands=['challenge'])
def challenge(message):
    bot.reply_to(message, f"🎯 چالش:\n\n{random.choice(CHALLENGES)}", parse_mode='Markdown')

@bot.message_handler(commands=['bio'])
def bio(message):
    bot.reply_to(message, f"📝 بیوگرافی:\n\n{random.choice(BIOGRAPHIES)}", parse_mode='Markdown')

@bot.message_handler(commands=['quote'])
def quote_cmd(message):
    bot.reply_to(message, f"💬 سخن بزرگان:\n\n_{random.choice(QUOTES)}_", parse_mode='Markdown')

@bot.message_handler(commands=['me'])
def me_cmd(message):
    u = message.from_user
    text = f"👤 اطلاعات شما:\n\n"
    text += f"🆔 آیدی: {u.id}\n"
    text += f"📛 نام: {u.first_name}\n"
    if u.last_name:
        text += f"👨‍👩‍👦 نام خانوادگی: {u.last_name}\n"
    if u.username:
        text += f"📱 یوزرنیم: @{u.username}\n"
    text += f"🤖 ربات: {'بله' if u.is_bot else 'خیر'}\n"
    bot.reply_to(message, text)

@bot.message_handler(commands=['dice'])
def dice_cmd(message):
    result = random.randint(1, 6)
    bot.send_dice(message.chat.id, emoji='🎲')
    bot.send_message(message.chat.id, f"🎲 عدد شما: {result}")

@bot.message_handler(commands=['8ball'])
def eight_ball(message):
    answers = ["بله حتماً! ✅", "نه! ❌", "شاید 🤔", "بعداً بپرس 🕐", "100% بله! 🎯", "به نظر نمیرسه 😕", "حتماً! 💯", "احتمالش کمه 😅", "آره داداش! 👍", "نه بابا! 🙅", "فکر نکنم 🤷", "حتماً! 🌟"]
    if ' ' in message.text:
        question = message.text.split(' ', 1)[1]
    else:
        question = "..."
    bot.reply_to(message, f"🔮 سوال: {question}\n\n🎱 جواب: {random.choice(answers)}", parse_mode='Markdown')

@bot.message_handler(commands=['love'])
def love(message):
    if not message.reply_to_message:
        bot.reply_to(message, "❌ رو پیام کسی ریپلای کن!")
        return
    u1 = message.from_user
    u2 = message.reply_to_message.from_user
    percent = random.randint(0, 100)
    hearts = "❤️" * (percent // 10) + "🖤" * (10 - percent // 10)
    text = f"❤️ عشق سنج\n\n"
    text += f"👤 {u1.first_name} ❤️ {u2.first_name}\n\n"
    text += f"💕 درصد عشق: {percent}%\n"
    text += f"{hearts}\n\n"
    if percent > 80:
        text += "🔥 عالیه! عشق واقعیه!"
    elif percent > 50:
        text += "💖 خوبه ولی کار داره!"
    elif percent > 30:
        text += "💔 امیدوار باش!"
    else:
        text += "😢 بهتره دنبال یکی دیگه باشی!"
    bot.reply_to(message, text)

@bot.message_handler(commands=['info'])
def info_user(message):
    if not message.reply_to_message:
        u = message.from_user
    else:
        u = message.reply_to_message.from_user
    try:
        member = bot.get_chat_member(message.chat.id, u.id)
        status = member.status
    except:
        status = "نامشخص"
    text = f"👤 اطلاعات کاربر:\n\n"
    text += f"🆔 آیدی: {u.id}\n"
    text += f"📛 نام: {u.first_name}\n"
    if u.last_name:
        text += f"👨‍👩‍👦 نام خانوادگی: {u.last_name}\n"
    if u.username:
        text += f"📱 یوزرنیم: @{u.username}\n"
    text += f"👑 نقش: {status}\n"
    text += f"🤖 ربات: {'بله' if u.is_bot else 'خیر'}\n"
    bot.reply_to(message, text)

@bot.message_handler(commands=['id'])
def id_cmd(message):
    if message.reply_to_message:
        u = message.reply_to_message.from_user
        text = f"👤 آیدی: {u.id}"
    else:
        text = f"👤 آیدی شما: {message.from_user.id}\n💬 آیدی چت: {message.chat.id}"
    bot.reply_to(message, text)

@bot.message_handler(commands=['mute'])
def mute_user(message):
    if message.chat.type == 'private':
        return
    if not is_admin(message.chat.id, message.from_user.id):
        bot.reply_to(message, "❌ فقط ادمین!")
        return
    if not message.reply_to_message:
        bot.reply_to(message, "❌ رو پیام کسی ریپلای کن!")
        return
    if not is_bot_admin(message.chat.id):
        bot.reply_to(message, "❌ من ادمین نیستم!")
        return
    try:
        bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, can_send_messages=False, can_send_media_messages=False, can_send_other_messages=False, can_add_web_page_previews=False)
        bot.reply_to(message, f"🔇 {message.reply_to_message.from_user.first_name} سکوت شد!")
    except Exception as e:
        bot.reply_to(message, f"❌ خطا: {e}")

@bot.message_handler(commands=['unmute'])
def unmute_user(message):
    if message.chat.type == 'private':
        return
    if not is_admin(message.chat.id, message.from_user.id):
        bot.reply_to(message, "❌ فقط ادمین!")
        return
    if not message.reply_to_message:
        bot.reply_to(message, "❌ رو پیام کسی ریپلای کن!")
        return
    if not is_bot_admin(message.chat.id):
        bot.reply_to(message, "❌ من ادمین نیستم!")
        return
    try:
        bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True)
        bot.reply_to(message, f"🔊 {message.reply_to_message.from_user.first_name} رفع سکوت شد!")
    except Exception as e:
        bot.reply_to(message, f"❌ خطا: {e}")

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.chat.type == 'private':
        return
    if not is_admin(message.chat.id, message.from_user.id):
        bot.reply_to(message, "❌ فقط ادمین!")
        return
    if not message.reply_to_message:
        bot.reply_to(message, "❌ رو پیام کسی ریپلای کن!")
        return
    if not is_bot_admin(message.chat.id):
        bot.reply_to(message, "❌ من ادمین نیستم!")
        return
    try:
        bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        bot.reply_to(message, f"🚫 {message.reply_to_message.from_user.first_name} بن شد!")
    except Exception as e:
        bot.reply_to(message, f"❌ خطا: {e}")

@bot.message_handler(commands=['warn'])
def warn_user(message):
    if message.chat.type == 'private':
        return
    if not is_admin(message.chat.id, message.from_user.id):
        bot.reply_to(message, "❌ فقط ادمین!")
        return
    if not message.reply_to_message:
        bot.reply_to(message, "❌ رو پیام کسی ریپلای کن!")
        return
    target = message.reply_to_message.from_user
    reason = "تخلف"
    if len(message.text.split()) > 1:
        reason = message.text.split(None, 1)[1]
    cur.execute('INSERT INTO warnings (chat_id, user_id, reason, warned_at) VALUES (?,?,?,?)', (message.chat.id, target.id, reason, int(time.time())))
    conn.commit()
    cur.execute('SELECT COUNT(*) FROM warnings WHERE chat_id=? AND user_id=?', (message.chat.id, target.id))
    warns = cur.fetchone()[0]
    bot.reply_to(message, f"⚠️ {target.first_name} اخطار گرفت!\n\n📝 دلیل: {reason}\n⚠️ تعداد اخطارها: {warns}/3")
    if warns >= 3:
        if is_bot_admin(message.chat.id):
            try:
                bot.ban_chat_member(message.chat.id, target.id)
                bot.send_message(message.chat.id, f"🚫 {target.first_name} به دلیل 3 اخطار بن شد!")
            except:
                pass

@bot.message_handler(commands=['clean'])
def clean_messages(message):
    if message.chat.type == 'private':
        return
    if not is_admin(message.chat.id, message.from_user.id):
        bot.reply_to(message, "❌ فقط ادمین!")
        return
    if not is_bot_admin(message.chat.id):
        bot.reply_to(message, "❌ من ادمین نیستم!")
        return
    try:
        n = 20
        if len(message.text.split()) > 1:
            try:
                n = int(message.text.split()[1])
                n = min(n, 100)
            except:
                pass
        deleted = 0
        for i in range(message.message_id, message.message_id - n, -1):
            try:
                bot.delete_message(message.chat.id, i)
                deleted += 1
            except:
                pass
        msg = bot.send_message(message.chat.id, f"🧹 {deleted} پیام پاک شد!")
        time.sleep(3)
        try:
            bot.delete_message(message.chat.id, msg.message_id)
        except:
            pass
    except Exception as e:
        bot.reply_to(message, f"❌ خطا: {e}")

@bot.message_handler(commands=['pin'])
def pin_msg(message):
    if message.chat.type == 'private':
        return
    if not is_admin(message.chat.id, message.from_user.id):
        return
    if not message.reply_to_message:
        bot.reply_to(message, "❌ رو پیام ریپلای کن!")
        return
    if not is_bot_admin(message.chat.id):
        bot.reply_to(message, "❌ من ادمین نیستم!")
        return
    try:
        bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
        bot.reply_to(message, "📌 پیام سنجاق شد!")
    except Exception as e:
        bot.reply_to(message, f"❌ خطا: {e}")

@bot.message_handler(commands=['tag'])
def tag_all(message):
    if message.chat.type == 'private':
        return
    if not is_admin(message.chat.id, message.from_user.id):
        return
    if not is_bot_admin(message.chat.id):
        return
    try:
        text = message.text.split(None, 1)[1] if len(message.text.split()) > 1 else "📢 توجه!"
        members = bot.get_chat_administrators(message.chat.id)
        mentions = [f"[{m.user.first_name}](tg://user?id={m.user.id})" for m in members if not m.user.is_bot]
        chunk_size = 5
        for i in range(0, len(mentions), chunk_size):
            chunk = mentions[i:i+chunk_size]
            bot.send_message(message.chat.id, f"{text}\n\n" + " ".join(chunk), parse_mode='Markdown')
            time.sleep(0.5)
    except Exception as e:
        bot.reply_to(message, f"❌ خطا: {e}")

@bot.message_handler(commands=['filter'])
def add_filter(message):
    if message.chat.type == 'private':
        return
    if not is_admin(message.chat.id, message.from_user.id):
        return
    parts = message.text.split(None, 2)
    if len(parts) < 3:
        bot.reply_to(message, "❌ استفاده: /filter کلمه | جواب")
        return
    try:
        keyword, response = parts[1], parts[2]
        cur.execute('INSERT INTO filters (chat_id, keyword, response) VALUES (?,?,?)', (message.chat.id, keyword.lower(), response))
        conn.commit()
        bot.reply_to(message, f"✅ فیلتر «{keyword}» اضافه شد!")
    except Exception as e:
        bot.reply_to(message, f"❌ خطا: {e}")

@bot.message_handler(commands=['stats'])
def stats(message):
    if message.chat.type == 'private':
        return
    try:
        count = bot.get_chat_members_count(message.chat.id)
        text = f"📊 آمار گروه:\n\n"
        text += f"👥 تعداد اعضا: {count}\n"
        text += f"📛 نام: {message.chat.title}\n"
        text += f"🆔 آیدی: {message.chat.id}\n"
        if message.chat.username:
            text += f"📱 یوزرنیم: @{message.chat.username}\n"
        bot.reply_to(message, text)
    except Exception as e:
        bot.reply_to(message, f"❌ خطا: {e}")

user_msg_count = {}

@bot.message_handler(func=lambda m: True, content_types=['text'])
def anti_spam(message):
    if message.chat.type == 'private':
        return
    chat_id = message.chat.id
    user_id = message.from_user.id
    if get_setting(chat_id, 'antilink', 'on') == 'on':
        if message.text and ('http://' in message.text or 'https://' in message.text or 't.me/' in message.text):
            if not is_admin(chat_id, user_id) and is_bot_admin(chat_id):
                try:
                    bot.delete_message(chat_id, message.message_id)
                    bot.send_message(chat_id, f"🚫 {message.from_user.first_name} لینک فرستادی! پاک شد.")
                    return
                except:
                    pass
    if get_setting(chat_id, 'antispam', 'on') == 'on':
        if not is_admin(chat_id, user_id):
            key = (chat_id, user_id)
            now = time.time()
            if key not in user_msg_count:
                user_msg_count[key] = []
            user_msg_count[key].append(now)
            user_msg_count[key] = [t for t in user_msg_count[key] if now - t < 10]
            if len(user_msg_count[key]) > 5:
                if is_bot_admin(chat_id):
                    try:
                        bot.delete_message(chat_id, message.message_id)
                        bot.restrict_chat_member(chat_id, user_id, can_send_messages=False, can_send_media_messages=False, can_send_other_messages=False, can_add_web_page_previews=False)
                        bot.send_message(chat_id, f"🔇 {message.from_user.first_name} به دلیل اسپم سکوت شد!")
                        user_msg_count[key] = []
                    except:
                        pass
    if get_setting(chat_id, 'filters', 'on') == 'on' and message.text:
        cur.execute('SELECT keyword, response FROM filters WHERE chat_id=?', (chat_id,))
        filters = cur.fetchall()
        for kw, resp in filters:
            if kw in message.text.lower():
                bot.reply_to(message, resp)
                break

@bot.message_handler(content_types=['new_chat_members'])
def welcome(message):
    chat_id = message.chat.id
    cur.execute('INSERT OR IGNORE INTO groups (chat_id, title, added_at) VALUES (?,?,?)', (chat_id, message.chat.title, int(time.time())))
    conn.commit()
    if get_setting(chat_id, 'welcome', 'on') != 'on':
        return
    for new_user in message.new_chat_members:
        if new_user.is_bot:
            continue
        welcome_text = random.choice(WELCOME_MESSAGES).format(name=new_user.first_name)
        welcome_text += f"\n\n📢 کانال ما: {CHANNEL_LINK}"
        mk = types.InlineKeyboardMarkup()
        mk.add(types.InlineKeyboardButton("📢 عضو کانال شو", url=CHANNEL_LINK))
        try:
            bot.send_message(chat_id, welcome_text, reply_markup=mk, parse_mode='Markdown')
        except:
            bot.send_message(chat_id, welcome_text)

last_challenge_time = {}
last_ad_time = {}

def auto_challenges():
    while True:
        try:
            cur.execute('SELECT chat_id FROM groups')
            chats = cur.fetchall()
            for (chat_id,) in chats:
                if get_setting(chat_id, 'challenges', 'on') != 'on':
                    continue
                if not is_bot_admin(chat_id):
                    continue
                now = time.time()
                if chat_id not in last_challenge_time or now - last_challenge_time[chat_id] > 7200:
                    try:
                        challenge_type = random.choice(['joke', 'challenge', 'bio', 'quote'])
                        if challenge_type == 'joke':
                            content = f"😂 جوک:\n\n{random.choice(JOKES)}"
                        elif challenge_type == 'challenge':
                            content = f"🎯 چالش:\n\n{random.choice(CHALLENGES)}"
                        elif challenge_type == 'bio':
                            content = f"📝 بیوگرافی:\n\n{random.choice(BIOGRAPHIES)}"
                        else:
                            content = f"💬 سخن بزرگان:\n\n_{random.choice(QUOTES)}_"
                        content += f"\n\n📢 {CHANNEL_LINK}"
                        bot.send_message(chat_id, content, parse_mode='Markdown')
                        last_challenge_time[chat_id] = now
                        time.sleep(2)
                    except:
                        pass
            time.sleep(60)
        except:
            time.sleep(60)

def auto_ad():
    while True:
        try:
            cur.execute('SELECT chat_id FROM groups')
            chats = cur.fetchall()
            for (chat_id,) in chats:
                if not is_bot_admin(chat_id):
                    continue
                now = time.time()
                if chat_id not in last_ad_time or now - last_ad_time[chat_id] >= 3600:
                    try:
                        mk = types.InlineKeyboardMarkup()
                        mk.add(types.InlineKeyboardButton("📢 عضو کانال شو", url=CHANNEL_LINK))
                        bot.send_message(chat_id, f"📢 تبلیغ:\n\n🤖 بهترین ربات مدیریت گروه!\n\n{CHANNEL_LINK}", reply_markup=mk, parse_mode='Markdown')
                        last_ad_time[chat_id] = now
                        time.sleep(2)
                    except:
                        pass
            time.sleep(60)
        except:
            time.sleep(60)

if __name__ == '__main__':
    print("🤖 ربات مدیریت گروه روشن شد!")
    threading.Thread(target=auto_challenges, daemon=True).start()
    threading.Thread(target=auto_ad, daemon=True).start()
    bot.infinity_polling()
