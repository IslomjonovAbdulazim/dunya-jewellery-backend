# Pure Uzbek messages for users

# Welcome messages
ADMIN_WELCOME = "🔧 Admin Panel - Dunya Jewellery\n\nXush kelibsiz! Quyidagi tugmalardan foydalaning:"
CLIENT_WELCOME = "🌟 Dunya Jewellery ga xush kelibsiz!\n\nChiroyli zargarlik mahsulotlarimiz bilan tanishing:"

# Help messages
ADMIN_HELP = (
    "🔧 *Admin Buyruqlari*\n\n"
    "• `/start` - Asosiy menyu\n"
    "• `/add` - Mahsulot qo'shish\n"
    "• `/add_contact` - Kontakt qo'shish"
)

CLIENT_HELP = "💍 *Dunya Jewellery*\n\n• `/start` - Asosiy menyu\n• Mahsulotlarni ko'rish uchun tugmalardan foydalaning"

# Product messages
NO_PRODUCTS_ADMIN = "📦 Mahsulotlar yo'q. Yangi qo'shing."
NO_PRODUCTS_CLIENT = "🔍 Hozircha mahsulotlar mavjud emas."
ALL_PRODUCTS_HEADER = "📦 *Barcha mahsulotlar*"
CLIENT_PRODUCTS_HEADER = "🛍️ *Bizning mahsulotlar*"

# Product creation
ADD_PRODUCT_START = "✏️ Yangi mahsulot qo'shamiz!\n\nMahsulot nomini yuboring:"
ENTER_DESCRIPTION = "📄 Mahsulot tavsifini yuboring:"
ENTER_SIZES = "📏 O'lchamlarni yuboring (16.5, 17, 18):"
ENTER_IMAGES = "📸 Rasmlarni yuboring yoki 'tayyor' yozing:"

# Product editing
EDIT_TITLE_PROMPT = "📝 Yangi nom yuboring yoki /skip:"
EDIT_DESCRIPTION_PROMPT = "📄 Yangi tavsif yuboring yoki /skip\n\n💡 Hozirgi: {}"
EDIT_SIZES_PROMPT = "📏 Yangi o'lchamlar yuboring yoki /skip\n\n💡 Hozirgi: {}"
EDIT_IMAGES_PROMPT = "📸 Yangi rasmlarni yuboring yoki 'tayyor' yozing\n\n💡 Hozirgi: {} ta"

# Success messages
PRODUCT_CREATED = "✅ '{}' yaratildi! ID: {}"
PRODUCT_UPDATED = "✅ '{}' yangilandi!"
PRODUCT_DELETED = "✅ '{}' o'chirildi!"
IMAGE_ADDED = "📸 {}-rasm qo'shildi! Yana yuboring yoki 'tayyor' yozing."

# Error messages (Pure Uzbek)
ACCESS_DENIED = "❌ Sizga ruxsat yo'q"
PRODUCT_NOT_FOUND = "❌ Mahsulot topilmadi"
CONTACT_NOT_FOUND = "❌ Kontakt topilmadi"
INVALID_SIZE_FORMAT = "❌ Noto'g'ri format! Masalan: 16.5, 17, 18"
ERROR_OCCURRED = "❌ Xatolik: {}"
INVALID_IMAGES_ERROR = "⚠️ Rasmlar buzilgan - qayta yuklang"
INVALID_FILE_ID_ERROR = "⚠️ Rasmlar noto'g'ri - qayta yuklang"

# Confirmation
DELETE_CONFIRMATION = "🗑️ *O'chirishni tasdiqlang*\n\nMahsulot: *{}*\n\nRostdan o'chirasizmi?"
DELETE_CANCELLED = "❌ Bekor qilindi"

# Contact management
CONTACT_MANAGEMENT_HEADER = "📞 Kontaktlar"
NO_CONTACTS_ADMIN = "📞 Kontaktlar yo'q."
ADD_CONTACT_START = "📞 Yangi kontakt qo'shamiz!\n\nKontakt nomini yuboring:"
ENTER_TELEGRAM_USERNAME = "📱 Telegram username yuboring (@username yoki bo'sh):"
ENTER_PHONE_NUMBER = "📞 Telefon raqam yuboring (+998901234567 yoki bo'sh):"
ENTER_INSTAGRAM_USERNAME = "📷 Instagram username yuboring (@username yoki bo'sh):"

# Contact editing
EDIT_CONTACT_LABEL = "🏷️ Yangi nom yuboring yoki /skip:"
EDIT_CONTACT_TELEGRAM = "📱 Yangi Telegram yuboring yoki /skip\n\n💡 Hozirgi: {}"
EDIT_CONTACT_PHONE = "📞 Yangi telefon yuboring yoki /skip\n\n💡 Hozirgi: {}"
EDIT_CONTACT_INSTAGRAM = "📷 Yangi Instagram yuboring yoki /skip\n\n💡 Hozirgi: {}"

# Contact success
CONTACT_CREATED = "✅ Kontakt '{}' yaratildi! ID: {}"
CONTACT_UPDATED = "✅ Kontakt '{}' yangilandi!"
CONTACT_DELETED = "✅ Kontakt '{}' o'chirildi!"
DELETE_CONTACT_CONFIRMATION = "🗑️ *Kontaktni o'chirish*\n\nKontakt: *{}*\n\nRostdan o'chirasizmi?"

# Order message
ORDER_MESSAGE = (
    "📞 Buyurtma\n\n"
    "🆔 Mahsulot: {}\n\n"
    "📱 Telefon: +998 90 123 45 67\n"
    "💬 Telegram: @dunya_jewellery"
)

# Templates
PRODUCT_TEMPLATE_CLIENT = "💍 {}\n\n📝 {}\n📏 O'lchamlar: {}"

PRODUCT_TEMPLATE_ADMIN = (
    "{} {}\n\n"
    "📝 {}\n"
    "📏 O'lchamlar: {}\n"
    "🖼️ Rasmlar: {} ta\n"
    "🆔 ID: {}"
)

CONTACT_TEMPLATE_ADMIN = (
    "{} {}\n\n"
    "📱 Telegram: {}\n"
    "📞 Telefon: {}\n"
    "📷 Instagram: {}\n"
    "🆔 ID: {}"
)

CONTACT_TEMPLATE_CLIENT = "*{}*\n📱 {}\n📞 {}\n📷 {}"

# Default values
DEFAULT_DESCRIPTION = "Tavsif yo'q"
DEFAULT_SIZES = "O'lcham yo'q"
DEFAULT_ADMIN_SIZES = "Yo'q"
CURRENT_VALUE_NONE = "Hozir yo'q"

# Button texts
BTN_PRODUCTS = "💍 Mahsulotlar"
BTN_CONTACT = "📞 Bog'lanish"
BTN_ADMIN_PRODUCTS = "📦 Mahsulotlar"
BTN_ADMIN_CONTACTS = "📞 Kontaktlar"
BTN_ORDER = "📞 Buyurtma"
BTN_EDIT = "✏️ Tahrirlash"
BTN_DELETE = "🗑️ O'chirish"
BTN_ADD_NEW = "➕ Yangi"
BTN_ADD_CONTACT = "➕ Kontakt"
BTN_CONFIRM_DELETE = "✅ Ha"
BTN_CANCEL = "❌ Yo'q"
BTN_BACK_MAIN = "🔙 Asosiy"
BTN_BACK_TO_LIST = "🔙 Ro'yxat"