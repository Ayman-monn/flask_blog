import stripe 

def stripe_subscription_create(customer_id, price_id):
    subscription = stripe.Subscription.create(
        customer=customer_id, 
        items=[{
            "price": price_id
        }],
        payment_behavior="default_incomplete", 
        payment_settings={"save_default_payment_method": "on_subscription"},
        expand=['latest_invoice.payment_intent'],
    )
    return subscription 

