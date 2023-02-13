from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

 
app= Flask(__name__) # flask app

#setup db connection
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///data.db'
db= SQLAlchemy(app)

app.app_context().push()
# Create a database
class User(db.Model):

              
    id= db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50), unique=True, nullable=False)
    bio = db.Column(db.String(100))

    def __repr__(self):
        with app.app_context():
            return f"{self.name} -> {self.bio}"


# API routes
@app.route('/')
def index():
    return 'Hello Flask!'

@app.route('/user')
def homepage():
    user_data=User.query.all()

    # transform the output to list
    output=[]
    for user in user_data:
        user_detail={"name": user.name, "bio": user.bio}
        output.append(user_detail)
         
    return {"Users": output}

# now let's get Users based on their ids

@app.route('/user/<id>')
def get_user(id):
    user=User.query.get_or_404(id)
    return {"name": user.name, "bio":user.bio}

# add users
@app.route("/user",methods=['POST'])
def add_user():
    user=User(name=request.json['name'], bio=request.json['bio'])
    db.session.add(user)
    db.session.commit()
    return {'id': user.id}

# delete a user
@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    deluser=User.query.get(id)
    if deluser is None:
        return {"404": "User not Found!!"}
    
    db.session.delete(deluser)
    db.session.commit()
    return {"Response": "Ok"}

# update the user's info
@app.route('/user/update/<id>', methods=['PUT'])
def update_user(id):
    updateuser=User.query.get(id)
    if updateuser is None:
        return {'404': 'User not found!!'}
    updateuser.name = request.json.get('name', updateuser.name)
    updateuser.bio = request.json.get('bio', updateuser.bio)

    db.session.commit()
    return {"Response": "Ok"}



# create the db and table using terminal instead, it's the easiest
# in the python console:
# from app import db, User
# db.create_all()
# create an object for the model class
# user1=User(nam, nbio)
# Adding tothe table 
# db.session.add(obj)
# db.session.commit()

# read the data from the table
# obj.query.all()

# add another entry to the db table as 
# db.session.add(user1/obj(name="st", bio="mtth"))

