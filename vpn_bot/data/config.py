from environs import Env


env = Env()
env.read_env()


BOT_TOKEN = env.str("BOT_TOKEN")
BOT_NAME = env.str('BOT_NAME')
ADMINS = env.list("ADMINS")
ADMINS_CHAT = env.str("ADMINS_CHAT")
ADMIN_PASSWORD = env.str("ADMINS_PASSWORD")


HOST_DB = env.str('HOST_DB')
USER_DB = env.str('USER_DB')
PASSWORD_DB = env.str('PASSWORD_DB')
DATABASE_DB = env.str('DATABASE_DB')


WEBHOOK_HOST = env.str('WEBHOOK_HOST')
WEBHOOK_PATH = env.str('WEBHOOK_PATH')


WEBHOOK_SSL_CERT = env.str('WEBHOOK_SSL_CERT')
WEBHOOK_SSL_PRIV = env.str('WEBHOOK_SSL_PRIV')
WEBAPP_HOST = env.str('WEBAPP_HOST')
WEBAPP_PORT = env.int('WEBAPP_PORT')


YOO_ACCOUNT_ID = env.str("YOO_ACCOUNT_ID")
YOO_SECRET_KEY = env.str("YOO_SECRET_KEY")
RETURN_URL_YOOKASSA = env.str("RETURN_URL_YOOKASSA")
YOOKASSA_EMAIL = env.str("YOOKASSA_EMAIL")
YOOMONEY_TOKEN = env.str("YOOKASSA_EMAIL")


dict_server = {
    1: {
        "url": "http://123.123.123.123:12312", #тут ничего не трогаем
        "password": "fdsfdfsfdsfds",
        "public_key": "fsdfdsfsd/n4n6nzOJK+SmIUo=fdsfs",
        "country": "🇦🇹 Страна",
        "end_point": "123.123.123.123:12312"
        },
   }

#вставляем свои данные в этот блок
dict_server_x = {
    1: {
        "ip_address": "123.123.123.123:8000", #пункт Чек Листа 1.2.1
        "x_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImFjY2VzcyI6InN1ZG8iLCJpYXQiOjE3MDI5ODU2MTksImV4cCI6MTczNDUyMTYxOX0.71azphio0d23MxPx8CfDx8yv2DJ9QfcYIZcWjrCQV2U", #пункт Чек Листа 5.
        "country": "🇦🇹 Страна" #меняем на страну вашего сервера в формате "*флаг страны* Страна"
    },
}


dict_device = {1: "📱 IOS (IPhone)",
               2: "📱 Android",
               3: "💻 Windows",
               4: "💻 MacOS"}


dict_tariff = {1: "STANDARD"}



dict_protocol = {5: 'Shadowsocks'}


VIDEO_IOS = env.str("VIDEO_IOS")
VIDEO_ANDROID = env.str("VIDEO_ANDROID")
VIDEO_IOS_X = env.str("VIDEO_IOS_X")
VIDEO_ANDROID_X = env.str("VIDEO_ANDROID_X")
VIDEO_WINDOWS_WG = env.str("VIDEO_WINDOWS_WG")
VIDEO_WINDOWS_X = env.str("VIDEO_WINDOWS_X")
VIDEO_MAC_X = env.str("VIDEO_MAC_X")
VIDEO_MAC_WG = env.str("VIDEO_MAC_WG")
