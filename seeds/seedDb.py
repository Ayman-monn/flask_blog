from datetime import timedelta
import os
import random
from flask_seeder import Seeder 
from faker import Faker 
from blog import cfg, bcrypt, db
from blog.models.ArticleModel import Article
from blog.models.AuthModel import User
from blog.models.LikeModel import Like
from blog.models.SubscribeModel import StripeCustomer

fake = Faker("ar_AA")


class SeedDb(Seeder): 
    def add_user(self): 
        names = [fake.unique.first_name()+" "+fake.unique.last_name() for i in range(cfg.ACCOUNT_COUNT)]
        emails = [fake.unique.email() for i in range(cfg.ACCOUNT_COUNT)]
        for name, email in zip(names, emails): 
            user = User(
                username=name, 
                email = email, 
                password= bcrypt.generate_password_hash(cfg.USER_PASSWORD).decode("utf-8"),
                is_admin = fake.boolean(chance_of_getting_true=cfg.ADMIN_PERCENTAGE),
                join_date = fake.date_this_year(),
            )
            print(user)
            db.session.add(user)

    def add_article(self): 
        admins = User.query.filter_by(is_admin=True).all()
        images = []
        dirctory = os.fsencode(cfg.IMAGES_DIR)
        for file in os.listdir(dirctory): 
            filename = os.fsdecode(file) 
            if filename.endswith("png") or filename.endswith("jgp"): 
                images.append(filename) 
        for i in range(cfg.ARTICLE_COUNT): 
            admin = random.choice(admins)
            img = random.choice(images) 
            article = Article(
                user_id = admin.id,
                title = fake.sentence(nb_words=7), 
                content=fake.paragraph(nb_sentences=200),
                article_img = img,
                created_at = fake.date_this_year()  
            )
            print(article)
            db.session.add(article) 


    def add_customer(self): 
        subscribers = User.query.filter_by(is_admin=False).all() 
        for i in range(cfg.CUSTOMER_COUNT): 
            subscriber = random.choice(subscribers) 
            subscribers.remove(subscriber)
            subscription_start = fake.date_between(start_date=cfg.START_DATE)
            db_customer = StripeCustomer(
                user_id = subscriber.id,
                subscription_type = "monthly", 
                status="active", 
                customer_id = fake.lexify(text="id_??????????"),
                subscription_id = fake.lexify(text="sub_??????????"),
                amount=10, 
                subscription_start = subscription_start ,
                subscription_end =  subscription_start + timedelta(days=30),
                subscription_canceld = False 
            )
            print(db_customer) 
            db.session.add(db_customer)
    def add_like(self): 
        subscribers = StripeCustomer.query.filter_by(status="active").all() 
        admins = User.query.filter_by(is_admin=True).all() 
        articles = Article.query.all() 
        subscribers.extend(admins) 
        for i in range(cfg.LIKE_COUNT): 
            liked_user = random.choice(subscribers).id 
            article_id = random.choice(articles).id 
            like = Like(
                liked_user=liked_user, 
                article_id=article_id
            )
            print(like) 
            db.session.add(like) 

    def run(self): 
        self.add_user() 
        self.add_article() 
        self.add_customer() 
        self.add_like()