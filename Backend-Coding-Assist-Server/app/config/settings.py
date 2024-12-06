import os.path

from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()


class Settings:
    ENVIRONMENT = os.getenv('ENVIRONMENT')  # 환경 변수 ENVIRONMENT를 읽음
    ENGINE_SERVER = os.getenv(f'{ENVIRONMENT.upper()}_ENGINE_SERVER')

    OPEN_API_KEY = os.getenv('OPEN_API_KEY')
