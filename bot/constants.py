# Text constants and messages for the bot

# Welcome messages
ADMIN_WELCOME = "🔧 *Admin Panel - Dunya Jewellery*\n\nXush kelibsiz! Quyidagi tugmani bosing:"
CLIENT_WELCOME = "🌟 *Dunya Jewellery*ga xush kelibsiz!\n\nBizning go'zal zargarlik buyumlarimiz bilan tanishib chiqing:"

# Help messages
ADMIN_HELP = (
    "🔧 *Admin Buyruqlari*\n\n"
    "• `/products` - Barcha mahsulotlar\n"
    "• `/add` - Mahsulot qo'shish\n"
    "• `/edit 1` - 1-ID mahsulotni tahrirlash\n"
    "• `/delete 1` - 1-ID mahsulotni o'chirish"
)

CLIENT_HELP = (
    "💍 *Dunya Jewellery*\n\n"
    "• /start - Asosiy menyu\n"
    "• Mahsulotlarni ko'rish uchun tugmalardan foydalaning"
)

# Product management messages
NO_PRODUCTS_ADMIN = "📦 Mahsulotlar yoq. /add buyrugi bilan qoshing."
NO_PRODUCTS_CLIENT = "🔍 Hozircha mahsulotlar mavjud emas."
ALL_PRODUCTS_HEADER = "📦 *Barcha mahsulotlar:*"
CLIENT_PRODUCTS_HEADER = "🛍️ *Bizning mahsulotlar:*"
PRODUCTS_COUNT = "📋 Jami: {} ta mahsulot"
SELECT_PRODUCT = "👆 Mahsulotni tanlang:"

# Product creation workflow
ADD_PRODUCT_START = "✏️ Yangi mahsulot qoshamiz!\n\nMahsulot *nomini* yuboring:"
ENTER_DESCRIPTION = "*Tavsifni* yuboring:"
ENTER_SIZES = "*Olchamlarni* yuboring (16.5, 17, 18):"
ENTER_IMAGES = "Rasmlarni yuboring yoki 'tayyor' yozing:"

# Product editing workflow
EDIT_TITLE_PROMPT = "Yangi *nom* yuboring yoki /skip:"
EDIT_DESCRIPTION_PROMPT = "Yangi *tavsif* yuboring yoki /skip\n\n📝 Hozirgi tavsif: _{}_"
EDIT_SIZES_PROMPT = "*Olchamlar* (16.5, 17, 18) yoki /skip\n\n📏 Hozirgi olchamlar: _{}_"
EDIT_IMAGES_PROMPT = "Yangi rasmlarni yuboring yoki 'tayyor' yozing\n\n🖼️ Hozirgi rasmlar: {} ta\n\n💡 Yangi rasm qoshsangiz, eskisi almashadi"

# Success messages
PRODUCT_CREATED = "✅ '{}' yaratildi! ID: {}"
PRODUCT_UPDATED = "✅ '{}' yangilandi!"
PRODUCT_DELETED = "✅ '{}' muvaffaqiyatli ochirildi!"
IMAGE_ADDED = "📸 {}-rasm qoshildi! Yana rasm yuboring yoki 'tayyor' yozing."

# Error messages
ACCESS_DENIED = "❌ Ruxsat yoq"
PRODUCT_NOT_FOUND = "❌ Mahsulot topilmadi"
INVALID_SIZE_FORMAT = "❌ Notogri format. Masalan: 16.5, 17, 18"
ERROR_OCCURRED = "❌ Xatolik: {}"
INVALID_IMAGES_ERROR = "⚠️ Rasmlar xato - qayta yuklang"
INVALID_FILE_ID_ERROR = "⚠️ Rasmlar xato (File ID invalid) - qayta yuklang"

# Confirmation messages
DELETE_CONFIRMATION = "🗑️ *Ochirishni tasdiqlang*\n\nMahsulot: *{}*\n\nRostdan ham ochirishni xohlaysizmi?"
DELETE_CANCELLED = "Bekor qilindi"

# Contact information
CONTACT_INFO = (
    "📞 *Boglanish malumotlari*\n\n"
    "📱 Telefon: +998 90 123 45 67\n"
    "💬 Telegram: @dunya_jewellery\n"
    "📍 Manzil: Toshkent sh., Amir Temur kochasi\n"
    "🕐 Ish vaqti: 9:00 - 18:00"
)

# Contact management messages
CONTACT_MANAGEMENT_HEADER = "📞 *Kontakt boshqaruvi:*"
NO_CONTACTS_ADMIN = "📞 Kontaktlar yo'q. Yangi kontakt qo'shing."
ADD_CONTACT_START = "📞 Yangi kontakt qo'shamiz!\n\nKontakt *nomini* yuboring (masalan: Asosiy, Savdo, Yordam):"
ENTER_TELEGRAM_USERNAME = "Telegram username yuboring (@username formatida yoki bo'sh qoldiring):"
ENTER_PHONE_NUMBER = "Telefon raqam yuboring (+998901234567 formatida yoki bo'sh qoldiring):"
ENTER_INSTAGRAM_USERNAME = "Instagram username yuboring (@username formatida yoki bo'sh qoldiring):"

# Contact editing prompts
EDIT_CONTACT_LABEL = "Yangi *nom* yuboring yoki /skip:"
EDIT_CONTACT_TELEGRAM = "Yangi *Telegram username* yuboring yoki /skip\n\n📱 Hozirgi: _{}_"
EDIT_CONTACT_PHONE = "Yangi *telefon raqam* yuboring yoki /skip\n\n📞 Hozirgi: _{}_"
EDIT_CONTACT_INSTAGRAM = "Yangi *Instagram username* yuboring yoki /skip\n\n📷 Hozirgi: _{}_"

# Contact success messages
CONTACT_CREATED = "✅ Kontakt '{}' yaratildi! ID: {}"
CONTACT_UPDATED = "✅ Kontakt '{}' yangilandi!"
CONTACT_DELETED = "✅ Kontakt '{}' muvaffaqiyatli o'chirildi!"

# Contact confirmation
DELETE_CONTACT_CONFIRMATION = "🗑️ *Kontaktni o'chirishni tasdiqlang*\n\nKontakt: *{}*\n\nRostdan ham o'chirishni xohlaysizmi?"

# Contact display template
CONTACT_TEMPLATE_ADMIN = (
    "{} *{}*\n\n"
    "📱 Telegram: {}\n"
    "📞 Telefon: {}\n"
    "📷 Instagram: {}\n"
    "🆔 ID: {}"
)

CONTACT_TEMPLATE_CLIENT = "*{}*\n📱 {}\n📞 {}\n📷 {}"

# Order message
ORDER_MESSAGE = (
    "📞 Mahsulot ID: {}\n\n"
    "Buyurtma berish uchun quyidagi raqamga qongiroq qiling:\n"
    "+998 90 123 45 67\n\n"
    "Yoki @dunya_jewellery ga yozing"
)

# Product display templates
PRODUCT_TEMPLATE_CLIENT = "💍 *{}*\n\n📝 {}\n📏 *Olchamlar:* {}\n\n📞 Buyurtma uchun admin bilan boglanish"

PRODUCT_TEMPLATE_ADMIN = (
    "{} *{}*\n\n"
    "📝 {}\n"
    "📏 *Olchamlar:* {}\n"
    "🖼️ *Rasmlar:* {} ta\n"
    "🆔 *ID:* {}"
)

# Default values
DEFAULT_DESCRIPTION = "Tavsif yoq"
DEFAULT_SIZES = "Belgilanmagan"
DEFAULT_ADMIN_SIZES = "Yoq"
CURRENT_VALUE_NONE = "Hozir yoq"

# Button texts (will be used in keyboards.py)
BTN_PRODUCTS = "💍 Mahsulotlar"
BTN_CONTACT = "📞 Bog'lanish"
BTN_ADMIN_PRODUCTS = "📦 Mahsulotlar"
BTN_ADMIN_CONTACTS = "📞 Kontaktlar"
BTN_ORDER = "📞 Buyurtma berish"
BTN_EDIT = "✏️ Tahrirlash"
BTN_DELETE = "🗑️ Ochirish"
BTN_ADD_NEW = "➕ Yangi qoshish"
BTN_ADD_CONTACT = "➕ Kontakt qoshish"
BTN_CONFIRM_DELETE = "✅ Ha, ochirish"
BTN_CANCEL = "❌ Bekor qilish"
BTN_BACK_MAIN = "🔙 Asosiy menyu"
BTN_BACK_TO_LIST = "🔙 Ro'yxatga qaytish"