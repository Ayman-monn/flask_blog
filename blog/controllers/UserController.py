from flask import flash, redirect, render_template, request, url_for
from blog import bcrypt, db
from flask_login import login_required, login_user, current_user, logout_user
from blog.forms.AuthForm import LoginForm, RegisterationForm
from blog.models.AuthModel import User


class UserController: 
    def user_login(): 
        if current_user.is_authenticated:
            return redirect(url_for("main_controller.home"))
        form = LoginForm() 
        if form.validate_on_submit(): 
            user = User.query.filter_by(email = form.email.data).first()
            if user is not None or bcrypt.check_password_hash(user.password, form.password.data): 
                login_user(user, remember=form.remember.data)
                flash("تم تسجيل الدخول بنجاح", "success")
                return redirect(request.args.get("next") or url_for("main_controller.home"))
            else: 
                flash("فشل في تسجيل الدخول تأكد من كتابة البريد الالكتروني وكلمة السر بشكل صحيح.","dnager")
                return redirect(url_for("auth_controller.user_login"))
        return render_template("auth/login.jinja", form=form, title="تسجيل الدخول")

    def user_register(): 
        if current_user.is_authenticated:
            return redirect(url_for("main_controller.home"))
        form = RegisterationForm()
        if form.validate_on_submit(): 
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
            username = form.username.data
            user = User(username=username, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            login_user(user) 
            flash(f"أهلا بك {username} في المدونة قم بالاشتراك حتي تتمكن من قراءة المقالات", "success")
            return redirect(url_for("main_controller.home"))
        return render_template('auth/register.jinja', form=form, title="إنشاء حساب")
    
    @login_required
    def user_logout(): 
        logout_user() 
        flash("تم تسجيل الخروج", "warning")
        return redirect(url_for('main_controller.home'))
