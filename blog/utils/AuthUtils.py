from flask_mail import Message
from blog import cfg, mail
from flask import url_for 


def send_reset_email(user): 
    token = user.get_reset_token() 
    msg = Message("Password Reset Request", sender=cfg.RESET_MAIL, recipients=[user.email]) 
    msg.body = f"""{url_for('auth_controller.reset_pass', token=token, _external=True)}
    لإستعادة كلمة السر اضغط علي الرابط التالي: """
    print(msg)
    mail.send(msg)
    print("done")