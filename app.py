from flask import Flask, request, jsonify

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# instantiate flask app
app = Flask(__name__)

# set configs 
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///datebase.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# instatiate db object 
db = SQLAlchemy(app)

# create marshmallow object 
ma = Marshmallow(app)

# cerate database
class List(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable = False)
    age = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(20), nullable = False)

    def __repr__(self):
        return self.id

# create list schemas 

class ListSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'age', 'city')

# create instance of schemas 

list_schema = ListSchema(many=False)  # only 1 record
lists_schema = ListSchema(many=True) # many record

#create route

@app.route("/list", methods = ["POST"] )
def add_list():
    try: 
        name = request.json['name']
        age = request.json['age']
        city = request.json['city']

        new_list = List(name=name,age=age,city=city)   
        db.session.add(new_list)
        db.session.commit()
        return list_schema.jsonify(new_list)  
    
    except Exception as e:
        return jsonify({"error" : "invalid request"})


# Get list

@app.route("/list", methods = ["GET"])
def get_lists():
    lists = List.query.all()
    result_set = lists_schema.dump(lists)
    return jsonify(result_set)

# specific id ka get 

@app.route("/list/<int:id>", methods = ["GET"])
def get_list(id):
    list = List.query.get_or_404(int(id))
    return list_schema.jsonify(list)


# update list 

@app.route("/list/<int:id>", methods = ["PUT"])
def update_list(id):
    list = List.query.get_or_404(int(id))
    name = request.json['name']
    age = request.json['age']
    city = request.json['city']

    list.name = name
    list.age = age
    list.city = city

    db.session.commit()
    return list_schema.jsonify(list)

    
# delete list 

@app.route("/list/<int:id>", methods = ["DELETE"])
def delete_list(id):
    list = List.query.get_or_404(int(id))
    db.session.delete(list)
    db.session.commit()

    return jsonify({"success" : "List delete"})
    
if __name__ == "__main__":
    app.run(debug=True)
