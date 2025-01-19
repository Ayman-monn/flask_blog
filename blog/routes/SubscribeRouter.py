from flask import Blueprint 
from blog.controllers.SubscribeController import SubscibeController

SubscribeRouter = Blueprint('subscirbe_controller', __name__) 


SubscribeRouter.route('/subscription', methods=["GET"])(SubscibeController.subscription)
SubscribeRouter.route('/create-subscription', methods=["GET", "POST"])(SubscibeController.subscription_create)
SubscribeRouter.route('/public-key', methods=["GET"])(SubscibeController.get_publishable_key) 
SubscribeRouter.route('/webhook', methods=["POST"])(SubscibeController.webhook_received)
SubscribeRouter.route('/subscription-success', methods=['GET'])(SubscibeController.subscription_success)

