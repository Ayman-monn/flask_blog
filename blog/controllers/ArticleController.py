from flask import redirect, render_template, url_for, flash
from blog.models.ArticleModel import Article
from blog.forms.ArticleForm import ArticleForm
from blog import db 


class ArticleController: 
    def add_article(): 
        form = ArticleForm() 
        if form.validate_on_submit(): 
            new_article = Article(user_id = 1, title =form.title.data, content=form.content.data)
            db.session.add(new_article) 
            db.session.commit() 
            flash("تمت إضافة المقالة بنجاح", "success")
            return redirect(url_for("main_controller.home"))
        return render_template("articles/article_add.jinja", form=form, legend="إضافة مقالة جديدة", title="إضافة مقالة")
    
    