from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    print(request.method)
    if request.method=='GET':
        ms_array=[]
        ms=Message.query.all()
        for m in ms: 
            m_dict=m.to_dict()
            ms_array.append(m_dict)
        r=make_response(ms_array, 200)
        return r
    if request.method=='POST':
        json_dude=request.get_json()
        new_message=Message(
            username=json_dude['username'],
            body=json_dude['body']
        )
        db.session.add(new_message)
        db.session.commit()
        nm_dict=new_message.to_dict()
        r=make_response(nm_dict, 201)
        return r

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message=Message.query.filter(Message.id==id).first()
    if request.method=='PATCH':
        json_dude=request.get_json()
        for key in json_dude:
            setattr(message, key, json_dude[key])
        db.session.add(message)
        db.session.commit()
        message_dict=message.to_dict()
        r=make_response(message_dict,200)
        return r
    elif request.method=='DELETE':
        db.session.delete(message)
        db.session.commit()
        rb={'delete-successful':True, 'message':"Message deleted"}
        r=make_response(rb, 200)
        return r

if __name__ == '__main__':
    app.run(port=5555)
