from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Email, Length, ValidationError

from blog.models.AuthModel import User



class LoginForm(FlaskForm): 
    email = StringField("البريد الإلكتروني", validators=[DataRequired(), Email()])
    password = PasswordField("كلمة السر", validators=[DataRequired()])
    remember = BooleanField("تذكرني")
    submit = SubmitField("تسجيل الدخول")

class RegisterationForm(FlaskForm): 
    username = StringField("اسم المستخدم", validators=[DataRequired(), Length(min=3, max=30)])
    email = StringField("البريد الإلكتروني", validators=[DataRequired(), Email(message="البريد الالكتروني غير صالح")])
    password = PasswordField("كلمة السر", validators=[DataRequired()])
    conform_password = PasswordField("تأكيد كلمة السر", validators=(DataRequired(), EqualTo("password", message="كلمة السر غير متطابقة")))
    submit = SubmitField("تسجيل")

    def validate_email(self, field): 
        if User.query.filter_by(email=field.data).first(): 
            raise ValidationError("البريد الألكتروني موجود مسبقاً. قم بإستعادة كلمة المرور في حال نسيانها.")
        
    def validate_username(self, field): 
        if User.query.filter_by(username=field.data).first(): 
            raise ValidationError("اسم المستخدم يجب ان يكون فريد. قم بإختيار اسم آخر")
        

class RequestResetForm(FlaskForm): 
    email = StringField("البريد الإلكتروني", validators=[DataRequired(), Email(message="البريد الالكتروني غير صالح")])
    submit = SubmitField("استعادة كلمة السر")

    def validate_email(self, field): 
        user =  User.query.filter_by(email=field.data).first() 
        if user is None: 
            raise ValidationError("لا يوجد بريد مسجل بهذا الاسم")



class ResetPasswordForm(FlaskForm): 
    password = PasswordField("كلمة السر", validators=[DataRequired()])
    conform_password = PasswordField("تأكيد كلمة السر", validators=(DataRequired(), EqualTo("password", message="كلمة السر غير متطابقة")))
    submit = SubmitField("تغيير كلمة السر")
    