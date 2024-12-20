from blog import cfg, db
from flask import flash, redirect, render_template, url_for,request
from flask_login import current_user, login_required
import stripe
from blog.models.SubscribeModel import StripeCustomer
from blog.utils.SubscribeUtils import stripe_subscription_create 


class SubscibeController:
    def subscription():
        if current_user.is_anonymous: 
            return render_template('subscribe/subscription.jinja', prices=cfg.prices, title="اشترك")
        customer = StripeCustomer.query.filter_by(user_id=current_user.id).first() 
        if customer and customer.status == "active": 
            flash("قمت بالإشتراك مسبقاً. إذا كنت ترغب بتغيير الإشتراك إضغط علي إدارة الإشتراك", "warning")
            return redirect(url_for('auth_controller.user_account')) 
        else: 
            return render_template('subscribe/subscription.jinja', prices=cfg.prices, title="اشترك")
    
    @login_required
    def subscription_create():
        if current_user.is_admin: 
            flash("لا يمكن للمدير الإشتراك", "warning")
            return redirect(url_for('main_controller.home')) 
        customer = StripeCustomer.query.filter_by(user_id=current_user.id).first()
        if customer and customer.status =="active": 
            flash("يمكنك تعديل الإشتراك من صفحتك الشخصية", "warning") 
            return redirect(url_for('main_controller.home')) 
        try:
            price_id = request.form.get("price_id")
            if not customer:
                new_customer = stripe.Customer.create(email=current_user.email, name=current_user.username)
                subscription = stripe_subscription_create(new_customer.id, price_id)
                customer_db = StripeCustomer(
                    user_id= current_user.id, 
                    customer_id=new_customer.id, 
                    subscription_id=subscription.id 
                )
                db.session.add(customer_db)
                db.session.commit()
            else: 
                subscription = stripe_subscription_create(customer.customer_id, price_id)
                customer.subscription_id= subscription.id
                db.session.commit() 
            sub_description = subscription["latest"]['lines']['data'][0]['description']
            client_secret = subscription.latest_invoice.payment_intent.client_secret
            return render_template('subscribe/payment.jinja', sub_description=sub_description, client_secret=client_secret)
        except: 
            flash("حدث خطأ, يمكنك المحاولة لاحقاً", "warning")
            return redirect(url_for("subscription_controller.subscription"))