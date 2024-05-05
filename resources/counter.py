from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from models import  db
from models.counter import RequestCount

class RequestCountAPI(MethodView):
    @jwt_required()
    def get(self):
        '''
            This endpoint will return the number of requests which have been served by the server till now.

            Request Payload: ""
            
            Response Payload:
            {'requests': request_count.count}
        '''
        try:
            request_count = RequestCount.query.first()
            return jsonify({'requests': request_count.count}), 200
        except Exception as e:
            return jsonify({'error':e}), 500

class ResetRequestCountAPI(MethodView):
    @jwt_required()
    def post(self):
        '''
            This endpoint will return the number of requests which have been served by the server till now.

            Request Payload: ""
            
            Response Payload:
            {'message': 'request count reset successfully'}
        '''
        try:
            request_count = RequestCount.query.first()
            if request_count:
                request_count.count = 0
                db.session.commit()
            return jsonify({'message': 'request count reset successfully'}), 200
        except Exception as e:
            return jsonify({'error': e}), 500

