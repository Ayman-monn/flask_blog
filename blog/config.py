import os 
from pathlib import Path 
from dotenv import load_dotenv
load_dotenv() 

class Config():
    TESTING = False
    DEBUG = False

class DevelopmentCfg(Config): 
    DEBUG = True 
    APP_DIR = Path(os.path.dirname(os.path.realpath(__file__)))
    CONTROLLER_DIR = APP_DIR / "controllers"
    VIEWS_DIR = APP_DIR / "template"
    STATIC_DIR = APP_DIR / "static"
    IMAGES_DIR = STATIC_DIR / "images"
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.environ.get("DATABASE_USERNAME")}:{os.environ.get("DATABASE_PASSWORD")}@localhost/{os.environ.get("DATABASE_NAME")}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False 


class ProductionCfg(Config): 
    pass 