from flask import Blueprint 
from blog.controllers.ArticleController import ArticleController

ArticleRouter = Blueprint("article_controller", __name__, url_prefix="/article") 

ArticleRouter.route("/article_add", methods=["POST", "GET"])(ArticleController.add_article) 

