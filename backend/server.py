from flask import Flask
import datetime
from flask_cors import CORS
from flask import request
from database import db

x = datetime.datetime.now()

app = Flask(__name__)
CORS(app)

db_name = 'inventory.db'

# mysql://username:password@host:port/database_name
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
 
# Suppresses warning while tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
# Initialising SQLAlchemy with Flask App
db.init_app(app)

@app.route("/api/home", methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        name = request.json.get('name')
        qty = request.json.get('qty')
        price = request.json.get('price')

        add_product = Product(
            name,
            qty,
            price
        )

        db.session.add(add_product)
        db.session.commit()
        return {"message": "Data has been added successfully"}
    
    details = Product.query.all()
    return {
        "details": details
    }
    
def create_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    from models import Product
    create_db()
    app.run(debug=True)
