from flask import jsonify, redirect, render_template, request, url_for, flash
from flask_login import current_user, login_required
from blog.models.ArticleModel import Article
from blog.forms.ArticleForm import ArticleForm
from blog import db
from blog.models.LikeModel import Like
from blog.models.SubscribeModel import StripeCustomer 


class ArticleController: 
    def article_add(): 
        form = ArticleForm() 
        if form.validate_on_submit(): 
            new_article = Article(user_id = 1, title =form.title.data, content=form.content.data)
            db.session.add(new_article) 
            db.session.commit() 
            flash("تمت إضافة المقالة بنجاح", "success")
            return redirect(url_for("main_controller.home"))
        return render_template("articles/article_add.jinja", form=form, legend="إضافة مقالة جديدة", title="إضافة مقالة")
    
    
    def article_show(id:int): 
        article = Article.query.get_or_404(id) 
        if current_user.is_authenticated: 
            customer = StripeCustomer.query.filter_by(user_id=current_user.id).first() 
            if customer and customer.status == "active": 
                return render_template("articles/article.jinja", customer=customer, article=article, title=article.title) 
        
        return render_template("articles/article.jinja", article=article, title= article.title) 

    @login_required
    def article_like(id):
        if request.method == 'GET':
            flash('لا تمتلك صلاحية الوصول للصفحة المطلوبة', 'danger')
            return redirect(url_for('main_controller.home'))
        
        try:
            customer = StripeCustomer.query.filter_by(user_id=current_user.id).first()
            article = Article.query.filter_by(id=id).first() 
            if customer and customer.status == "active" or current_user.is_admin: 
                like = Like.query.filter_by(liked_user=current_user.id, article_id=article.id).first()
                if like: 
                    db.session.delete(like)
                    db.session.commit() 
                else:
                    like = Like(liked_user=current_user.id, article_id=article.id)
                    db.session.add(like)
                    db.session.commit()             
                return jsonify({"likes": len(article.likes),
                                "liked": current_user.id in map(lambda x : x.liked_user, article.likes)})
            else: 
                flash("يجب عليك الاشتراك للاعجاب ","warning")
                return redirect(url_for("article_controller.article_show", article_id=article.id, id=article.id))
        except:
            flash("المقالة غير موجودة", "danger") 
            return redirect(url_for("main_controller.home"))