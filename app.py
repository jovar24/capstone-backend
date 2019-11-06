from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku
import os
from flask_cors import CORS

app = Flask(__name__)
heroku = Heroku(app)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ruaasrwlmgtfxf:13303bd59a4e332c07afe12bf766871eb731c5be954b0b0617b950432da5479c@ec2-174-129-253-140.compute-1.amazonaws.com:5432/d7ekolga4bffnl'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), unique= False)
    content = db.Column(db.String(300), unique=False)
    
    def __init__(self, title, content):
        self.title = title
        self.content = content

class ReviewSchema(ma.Schema):
    class Meta:
        fields = ['id','title', 'content']

review_schema = ReviewSchema()
reviews_schemas = ReviewSchema(many = True)     

@app.route('/review', methods=["POST"])
def post_review():
    title = request.json['title']
    content = request.json['content']

    new_review = Review(title, content)

    db.session.add(new_review)
    db.session.commit()

    review = Review.query.get(new_review.id)

    return review_schema.jsonify(review)

@app.route('/reviews', methods= ["GET"])
def get_reviews():
        all_reviews = Review.query.all()
        result = reviews_schemas.dump(all_reviews)
        return jsonify(result) 

@app.route('/review/<id>', methods=["DELETE"])
def erease_rev(id):
    review = Review.query.get(id)
    db.session.delete(review)
    db.session.commit()        

    return "Review has been deleted"

if __name__ == '__main__':
    app.run(debug=True)
