from flask import Blueprint 
from blog.controllers.SubscribeController import SubscibeController

SubscribeRouter = Blueprint('subscirbe_controller', __name__) 


SubscribeRouter.route('/subscription', method=["GET"])(SubscibeController.subscription)
SubscribeRouter.route('/create-subscription', method=["GET", "POST"])(SubscibeController.subscription_create)

