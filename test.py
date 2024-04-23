import os
from dotenv import load_dotenv

load_dotenv()

PASSWORD=os.environ.get('POSTGRES_PASSWORD')

print(PASSWORD)