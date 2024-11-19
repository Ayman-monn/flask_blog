import os 
from pathlib import Path 
from datetime import datetime
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
    # DATABASE CONFIGURATION 
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.environ.get("DATABASE_USERNAME")}:{os.environ.get("DATABASE_PASSWORD")}@localhost/{os.environ.get("DATABASE_NAME")}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    # OWNER DATA  
    OWNER_USERNAME = os.environ.get('OWNER_USERNAME')
    OWNER_EMAIL = os.environ.get('OWNER_EMAIL')
    OWNER_PASSWORD = os.environ.get('OWNER_PASSWORD')
    # Seeds Data 
    ACCOUNT_COUNT = 25
    USER_PASSWORD = "123"
    ADMIN_PERCENTAGE = 10
    ARTICLE_COUNT = 100 
    CUSTOMER_COUNT = 20
    START_DATE = datetime(2024, 9,1)
    LIKE_COUNT= 200




class ProductionCfg(Config): 
    pass 