import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.environ.get("REDIS_URL")
QUEUES = ["emails", "Default"]

