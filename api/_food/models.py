from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import app


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.create_all()

# models
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    body = db.Column(db.String, nullable=False)
    #ingredients = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return "<Recipe: %r>" % self.title
    
    def schema(self):
        return {
            'title' :   self.title,
            'body' :    self.body,
            'created_at'  : self.date,
            'id'    : self.id
        }