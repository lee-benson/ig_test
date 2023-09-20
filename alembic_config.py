import os
from dotenv import load_dotenv
from alembic.config import Config

load_dotenv()

db_url = os.environ.get('DATABASE_URL')

alembic_cfg = Config('alembic.ini')
alembic_cfg.set_main_option('sqlaclhemy.url', db_url)