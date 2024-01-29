from database import db
 
# Declaring Model
class Product(db.Model):
    __tablename__ = "products"
 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.current_timestamp())

    def __init__(self, name, qty, price):
        self.name = name
        self.qty = qty
        self.price = price
