from dotenv import load_dotenv
import os

load_dotenv()

tokenbot = os.getenv("BOT_TOKEN")
DB_PATH = "tasks.db"
