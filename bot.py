from rubx import Client
import random, string

bot = Client(auth="YOUR_AUTH", private_key="YOUR_PRIVATE_KEY")

FORCE_CHANNEL = "c0YOURCHANNEL"  # کانال جوین اجباری
STORAGE_CHANNEL = "c0STORAGECHAN"  # کانالی که فایل‌ها داخلش ذخیره میشن

# دیتابیس ساده در حافظه (برای شروع)
files = {}

def random_code(n=6):
    return ''.join(random.choice(string.ascii_uppercase+string.digits) for _ in range(n))

def check_join(guid):
    members = bot.get_group_members(FORCE_CHANNEL)
    for m in members:
        if m["member_guid"] == guid:
            return True
    return False

@bot.on_message()
def handler(msg):

    user = msg.author_guid

    # اگر کاربر فایل بفرسته
    if msg.file:
        # فقط ادمین میتونه فایل بذاره
        if user != YOUR_ADMIN_GUID:
            bot.send_message(msg.chat_id, "❌ فقط مدیر میتونه فایل بذاره.")
            return

        code = random_code()
        # فایل رو به کانال ذخیره فوروارد کن
        res = bot.forward_messages(
            from_object_guid=msg.chat_id,
            to_object_guid=STORAGE_CHANNEL,
            message_ids=[msg.message_id]
        )

        stored_id = res["data"]["message_ids"][0]
        files[code] = stored_id

        link = f"https://rubika.ir/{bot.me.username}?start=FILE_{code}"
        bot.send_message(msg.chat_id, f"✅ فایل ذخیره شد!\n🌐 لینک:\n{link}")
        return

    text = msg.text or ""

    # اگر لینک باز شده
    if text.startswith("/start FILE_"):
        code = text.split()[-1].replace("FILE_", "")

        # چک کردن
        if code not in files:
            bot.send_message(msg.chat_id, "❌ این لینک معتبر نیست.")
            return

        # جوین اجباری
        if not check_join(user):
            bot.send_message(
                msg.chat_id,
                "🔒 برای دانلود فایل ابتدا عضو کانال شوید:\n" +
                "https://rubika.ir/YourChannelUsername"
            )
            return

        msg_id = files[code]
        bot.forward_messages(
            from_object_guid=STORAGE_CHANNEL,
            to_object_guid=msg.chat_id,
            message_ids=[msg_id]
        )
        return
