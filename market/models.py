from market import db, login_manager
from market import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=30), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=30), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=2000)
    # User can own items
    # backref='owned_user' - it is backreference to User Model.
    # We can grab User object and can access to attribute Items
    # If we have iphone and we want to know owner of this phone, we must use BACKREF
    # LAZY = True. If we do not set up - sql-alchemy will not grab all objects of  items in one shot
    items = db.relationship('Item', backref='owned_user', lazy=True)

    # SHELL : from market.models import db.       db.drop_all(), db.create_all()

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    # for def login_page()
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'

    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price

    def can_sell(self, item_obj):
        return item_obj in self.items

    def to_dict(self):
        return {
            'name': self.username,
            'email_address': self.email_address,
            'password_hash': self.password_hash,
            'budget': self.budget,

        }

    # 2 classmethods for tests
    @classmethod
    def find_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_user_by_id(cls, id):
        return cls.query.filter_by(id=id).first()


# u1 = User(username='jsc', password_hash='123456', email_address='jsc@jsc')
# db.session.add(u1)
# db.session.commit()
# i1 = Item(name='Iphone 10', description='description', barcode='123456789123', price=800)
# i2 = Item(name='MacBookPro', description='description2', barcode='123456789321', price=2000)
# i3 = Item(name='TurboBookPro', description='The best invention by Apple', barcode='123456654456', price=2500)
# item1.owner = User.query.filter_by(username='jsc').first().id
# db.session.add(item1)
# i = Item.query.filter_by(name='MacBookPro').first()
# # i.owned_user  - backref

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1000), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Item: {self.name}"

    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

    def sell(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()

    # def save_to_db(self):
    #     db.session.add(self)
    #     db.session.commit()

    def __init__(self, name, price, barcode, description):
        self.name = name
        self.description = description
        self.price = price
        self.barcode = barcode

    def to_dict(self):
        return {
            'name': self.name,
            'price': self.price,
            'barcode': self.barcode,
            'description': self.description


        }






