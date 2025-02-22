from pathlib import Path

# 패키지 루트 디렉토리 설정
PACKAGE_ROOT = Path(__file__).parent  # settings.py의 부모 디렉토리(sea_voyage)를 루트로 설정
DATA_DIR = PACKAGE_ROOT / 'data'

MARNET_DIR = DATA_DIR / 'geojson/marnet' 