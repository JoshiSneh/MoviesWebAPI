from flask import jsonify, request
from flask.views import MethodView
from flask_jwt_extended import create_access_token
from db import db
from models.user import User


class RegisterAPI(MethodView):
    def post(self):
        '''
            This endpoint will register a user

            Request Payload:
            {
                “username”: <desired username>,
                “password”: <desired password>
            }

            Response Payload:
            {
                “access_token”: <Access Token>
            }
        '''
        try:
            data = request.get_json()
            print(data)
            username = data["username"]
            password = data["password"]

            if not username and not password:
                raise ValueError("Username and Password are required")
            
            if User.query.filter_by(username=username).first():
                raise ValueError("Username already exists")
            

            '''Storing the User'''
            new_user = User(username=username,password=password)
            db.session.add(new_user)
            db.session.commit()

            '''Creating the Access Token'''
            access_token = create_access_token(identity=username,fresh=True)

            return jsonify({'access_token': access_token}), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 400



