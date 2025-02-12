from flask import Blueprint

from blog.controllers.UserController import UserController
from blog.controllers.AdminController import AdminController

AuthRouter = Blueprint('auth_controller', __name__) 
# Admin Control
AuthRouter.route("/register", methods=['POST', 'GET'])(UserController.user_register)
AuthRouter.route("/login", methods=['POST', 'GET'])(UserController.user_login)
AuthRouter.route("/logout")(UserController.user_logout)
AuthRouter.route("/reset_password", methods=['POST', 'GET'])(UserController.reset_request)
AuthRouter.route("/reset_password/<token>", methods=['POST', 'GET'])(UserController.reset_pass)
AuthRouter.route("/account")(UserController.user_account) 
# Owner Control
AuthRouter.route("/sub-panal/user_control")(AdminController.users_control) 
AuthRouter.route("/sub-panal/role-grant/<int:user_id>")(AdminController.role_grant) 
AuthRouter.route("/sub-panal/role-revoke/<int:user_id>")(AdminController.role_revoke) 


