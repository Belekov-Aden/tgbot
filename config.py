import os


from dotenv import load_dotenv, find_dotenv


load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
PAYMENTS_TOKEN = os.getenv('PAYMENTS_TOKEN')


HOST = os.getenv('HOST')
PGUSER = os.getenv('PGUSER')
PGPASSWORD = os.getenv('PGPASSWORD')