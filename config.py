from dotenv import load_dotenv
import os

load_dotenv('.env')
admin_id = set(map(int, os.environ.get('admins').split(',')))
ai_api_key = os.environ.get('ai_api_key')
bot_token = os.environ.get('bot_token')
