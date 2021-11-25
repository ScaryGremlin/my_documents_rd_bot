from os import getenv

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")
BOT_ID = getenv("BOT_ID")
BOT_ADMINS = getenv("BOT_ADMINS").split(",")
DB_FILE_NAME = getenv("DB_FILE_NAME")
