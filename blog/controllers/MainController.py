from flask import render_template 
from blog import cfg 
from blog.models.ArticleModel import Article
from blog.utils.MainUtils import Paginate

class MainController: 
    def home(): 
        # articles_list = Article.query.order_by(Article.created_at.desc()).all() 
        pagination, article_per_page = Paginate(cfg.POSTS_PER_PAGE, Article, Article.created_at.desc())
        return render_template("main/home.jinja", article_per_page=article_per_page, pagination=pagination, title="مدونة") 
    
