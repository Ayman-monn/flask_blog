import json
from blog import cfg, db, stripe
from flask import flash, jsonify, redirect, render_template, url_for,request
from flask_login import current_user, login_required
from blog.models.SubscribeModel import StripeCustomer
from blog.utils.SubscribeUtils import handle_subscription_db, stripe_subscription_create, subscription_modify, upgrade_details 


class SubscibeController:
    def get_publishable_key():
        return jsonify(publicKey=cfg.STRIPE_PUBLISHABLE_KEY) 
    
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
            price_id = request.form.get("priceId")
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
            sub_description = subscription["latest_invoice"]['lines']['data'][0]['description']
            print('sub_description',sub_description)
            client_secret = subscription.latest_invoice.payment_intent.client_secret
            print("client_secret", client_secret)
            return render_template('subscribe/payment.jinja', sub_description=sub_description, client_secret=client_secret)
        except: 
            flash("حدث خطأ, يمكنك المحاولة لاحقاً", "warning")
            return redirect(url_for("subscirbe_controller.subscription"))
        

    def webhook_received():
        request_data = json.loads(request.data) 
        webhook_secret = cfg.STRIPE_WEBHOOK_SECRET 
        if webhook_secret: 
            signature = request.headers.get('stripe-signature') 
            try: 
                event = stripe.Webhook.construct_event(
                    payload=request.data, sig_header=signature, secret=webhook_secret
                )
                data = event["data"]
            except Exception as e : 
                return e 
            event_type = event["type"]
        else: 
            data = request_data["data"]
            event_type = request_data["type"]
        data_object = data["object"]
        if event_type == "customer.subscription.updated":
            handle_subscription_db(data_object)
            print(f'تم إنشاء كائن اشتراك {event.id}')
        elif event_type == "invoice.paid": 
            print("payment successed")
        elif event_type == 'setup_intent.created':
            print('تم إنشاء كائن Setup Intent')
        elif event_type == 'setup_intent.succeeded':
            print('تم إضافة طريقة دفع جديدة لعمليات الدفع المستقبلية')
        elif event_type == 'payment_method.attached':
            print('تم إضافة طريقة الدفع الجديدة إلي كائن العميل')
        return jsonify({"satuts" : "success"})

    @login_required
    def subscription_success(): 
        payment_intent_success = request.args.get('paymentIntentStatus') 
        if payment_intent_success is None: 
            flash('يمكنك مشاهدة تفاصيل الإشتراك من صفحتك الشخصية', 'warning')
            return redirect(url_for('auth_controller.user_account'))
        if payment_intent_success == 'succeeded': 
            return render_template('subscribe/payment_success.jinja', title='تم الإشتراك')
        else: 
            flash('حدث خطأ أثناء عملية الدفع تحقق من صفحتك الشخصية', 'warning')
            return redirect(url_for('auth_controller.user_account'))
        

    @login_required
    def upgrade_verifying(price_id): 
        if current_user.is_admin: 
            flash("لا يمكن للمدير الإشتراك", "warning")
            return redirect(url_for('main_controller.home')) 
        if current_user.stripe_customer[0].subscription_canceld: 
            flash("قم بتفعيل الإشتراك أولاً", "warning")
            return redirect(url_for('auth_controller.user_account')) 

        try:
            new_details = upgrade_details(price_id)
            print(new_details)
            return render_template('subscribe/upgrade_subscribe.jinja', new_details=new_details, price_id=price_id)
        except:
            flash('حدث خطأ أثناء ترقية الإشتراك', 'warning')
            return redirect(url_for('main_controller.home'))
        

    @login_required
    def subscription_upgrade(price_id): 
        if current_user.is_admin: 
            flash("لا يمكن للمدير الإشتراك", "warning")
            return redirect(url_for('main_controller.home')) 
        customer = StripeCustomer.query.filter_by(user_id=current_user.id).first()
        if current_user.stripe_customer[0].subscription_canceld: 
            flash("قم بتفعيل الإشتراك أولاً", "warning")
            return redirect(url_for('auth_controller.user_account')) 

        try:
            subscription_modify(price_id, customer.subscription_id)

            flash('تم تغيير الإشتراك بنجاح', 'success')
            return redirect(url_for('auth_controller.user_account'))
        except:
            flash('حدث خطأ أثناء ترقية الإشتراك', 'warning')
            return redirect(url_for('main_controller.home'))
        
    @login_required
    def change_payment_method():
        if current_user.is_admin: 
            flash("لا يمكنك الوصول للصفحة المطلوبة", "warning")
            return redirect(url_for('main_controller.home')) 
        if current_user.stripe_customer[0].subscription_canceld: 
            flash("قم بتفعيل الإشتراك أولاً", "warning")
            return redirect(url_for('auth_controller.user_account')) 
        return render_template('subscribe/change_payment_method.jinja') 


    def create_setup_intent(): 
        customer = current_user.stripe_customer[0]
        setup_intent = stripe.SetupIntent.create(customer=customer.customer_id)
        return jsonify(setup_intent)