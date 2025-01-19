from blog import stripe, db
from blog.models.SubscribeModel import StripeCustomer
from datetime import datetime

def stripe_subscription_create(customer_id, price_id):
    subscription = stripe.Subscription.create(
        customer=customer_id, 
        items=[{
            "price": price_id
        }],
        payment_behavior="default_incomplete", 
        payment_settings={"save_default_payment_method": "on_subscription"},
        expand=['latest_invoice.payment_intent']
    )
    return subscription 



def handle_subscription_db(data_object): 
    customer_db = StripeCustomer.query.filter_by(subscription_id=data_object.id).first()
    if customer_db: 
        customer_db.amount = data_object['items']['data'][0]['price']['unit_amount'] / 100 
        customer_db.subscription_type = data_object['items']['data'][0]['plan']['interval'] 
        customer_db.subscription_start = datetime.fromtimestamp(data_object['current_period_start'])
        customer_db.subscription_end = datetime.fromtimestamp(data_object['current_period_end'])
        customer_db.status = data_object.status
        customer_db.subscription_canceled = data_object.cancel_at_period_end
        db.session.commit() 
