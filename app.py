from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite'
app.config["JWT_SECRET_KEY"] = "secret"

# registro de extensões
JWTManager(app)
db = SQLAlchemy(app)
Migrate(app, db)

class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    name = data["name"]
    user = User.query.filter_by(name=name).first()
    if user:
        token = create_access_token({ "id": user.id })
        return jsonify({ "token": token }), 201    
    return jsonify({ "error": "usuario nao existe!" }), 400

@app.route("/protected")
@jwt_required
def protected():
     return jsonify({ "message": "secret" })

if __name__ == "__main__":
    app.run(debug=True)