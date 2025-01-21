from flask import flash, redirect, render_template, request, url_for
from blog import bcrypt, db, cfg
from flask_login import login_required, login_user, current_user, logout_user
from flask_paginate import Pagination
from blog.forms.AuthForm import (
    LoginForm,
    RegisterationForm,
    RequestResetForm,
    ResetPasswordForm,
)
from blog.models.AuthModel import User
from blog.models.SubscribeModel import StripeCustomer
from blog.utils.AuthUtils import send_reset_email


class UserController:
    def user_login():
        if current_user.is_authenticated:
            return redirect(url_for("main_controller.home"))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is not None and bcrypt.check_password_hash(
                user.password, form.password.data
            ):
                login_user(user, remember=form.remember.data)
                flash("تم تسجيل الدخول بنجاح", "success")
                return redirect(
                    request.args.get("next") or url_for("main_controller.home")
                )
            else:
                flash(
                    "فشل في تسجيل الدخول تأكد من كتابة البريد الالكتروني وكلمة السر بشكل صحيح.",
                    "dnager",
                )
                return redirect(url_for("auth_controller.user_login"))
        return render_template("auth/login.jinja", form=form, title="تسجيل الدخول")

    def user_register():
        if current_user.is_authenticated:
            return redirect(url_for("main_controller.home"))
        form = RegisterationForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
                "utf-8"
            )
            username = form.username.data
            user = User(
                username=username, email=form.email.data, password=hashed_password
            )
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash(
                f"أهلا بك {username} في المدونة قم بالاشتراك حتي تتمكن من قراءة المقالات",
                "success",
            )
            return redirect(url_for("main_controller.home"))
        return render_template("auth/register.jinja", form=form, title="إنشاء حساب")

    @login_required
    def user_logout():
        logout_user()
        flash("تم تسجيل الخروج", "warning")
        return redirect(url_for("main_controller.home"))

    def reset_request():
        if current_user.is_authenticated:
            return redirect(url_for("main_controller.home"))
        form = RequestResetForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            send_reset_email(user)
            flash("تم إرسال بريد الكتروني يحوى رابط لتغيير كلمة السر", "info")
            return redirect(url_for("auth_controller.user_login"))
        return render_template(
            "auth/reset_request.jinja", form=form, title="أعادة تعيين كلمة السر"
        )

    def reset_pass(token):
        if current_user.is_authenticated:
            return redirect(url_for("main_controller.home"))
        user = User.verify_reset_token(token)
        if user is None:
            flash("انتهت صلاحية الرابط حاول مرة ثانية", "warning")
            return redirect(url_for("auth_controller.reset_request"))
        form = ResetPasswordForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
                "utf-8"
            )
            user.password = hashed_password
            db.session.commit()
            flash("تم تغيير كلمة السر بنجاح، يمكنك تسجيل الدخول الآن", "success")
            return redirect(url_for("auth_controller.user_login"))
        return render_template(
            "auth/reset_pass.jinja", title="إعادة تعيين كلمة السر", form=form
        )

    @login_required
    def user_account():
        if current_user.is_admin:
            pagination = Pagination(total=len(current_user.articles))
            return render_template("auth/account.jinja", pagination=pagination)
        customer = StripeCustomer.query.filter_by(user_id=current_user.id).first()
        if customer and customer.subscription_id is not None:
            title = f"حسابي {current_user.username}"
            return render_template("auth/account.jinja", title=title, customer=customer, prices=cfg.prices)
        else:
            return render_template("auth/account.jinja")
