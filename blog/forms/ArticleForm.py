from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class ArticleForm(FlaskForm): 
    title = StringField("عنوان المقالة", validators=[DataRequired(), Length(min=5, max=255)])
    article_img = FileField("صورة المقالة", validators=[FileAllowed(['png', 'jgp'])])
    content = TextAreaField("محتوي المقالة", validators=[DataRequired(), Length(min=100, max=10000)])
    submit = SubmitField("نشر المقالة")

    
