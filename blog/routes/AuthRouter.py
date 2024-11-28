from flask import Blueprint

from blog.controllers.UserController import UserController


AuthRouter = Blueprint('auth_controller', __name__) 

AuthRouter.route("/register", methods=['POST', 'GET'])(UserController.user_register)
AuthRouter.route("/login", methods=['POST', 'GET'])(UserController.user_login)
AuthRouter.route("/logout")(UserController.user_logout)
