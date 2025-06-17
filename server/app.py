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

@app.route('/messages')
def messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([msg.to_dict() for msg in messages]), 200


@app.route('/messages/<int:id>')
def messages_by_id(id):
    return ''

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()

    if not data or not data.get('body') or not data.get('username'):
        return {"error": "Missing required fields"}, 400

    message = Message(
        body=data['body'],
        username=data['username']
    )

    db.session.add(message)
    db.session.commit()

    return jsonify(message.to_dict()), 201


@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get(id)
    if not message:
        return {"error": "Message not found"}, 404

    data = request.get_json()
    if 'body' in data:
        message.body = data['body']
        db.session.commit()

    return jsonify(message.to_dict()), 200


@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get(id)
    if not message:
        return {"error": "Message not found"}, 404

    db.session.delete(message)
    db.session.commit()
    return {"message": "Message deleted"}, 200




if __name__ == '__main__':
    app.run(port=5777)
