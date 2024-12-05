from flask import render_template 
from blog.models.ArticleModel import Article


class MainController: 
    def home(): 
        articles_list = Article.query.order_by(Article.created_at.desc()).all() 
        return render_template("main/home.jinja", articles_list=articles_list, title="مدونة") 
    
