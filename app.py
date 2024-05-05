from flask import Flask
from flask_jwt_extended import JWTManager
from models import db

from resources.collection import CollectionAPI,CollectionByUUIDAPI
from resources.counter import RequestCountAPI, ResetRequestCountAPI
from resources.movies import MoviesAPI
from resources.register import RegisterAPI

from middleware.request_count import request_count


app = Flask(__name__)
app.config.from_pyfile('config.py')


'''Initialize the database'''
db.init_app(app)

jwt = JWTManager(app)

'''Creating the Table'''
with app.app_context():
     db.create_all()


'''Registering the RegisterAPI'''
app.add_url_rule('/register', view_func=RegisterAPI.as_view('register_api'))


'''Registering the MoviesAPI'''
app.add_url_rule('/movies', view_func=MoviesAPI.as_view('movies_api'))


'''Registering the CollectionAPI'''
app.add_url_rule('/collection', view_func=CollectionAPI.as_view('collection_api'))
app.add_url_rule('/collection/<string:uuid>/', view_func=CollectionByUUIDAPI.as_view('collection_by_uuid_api'))



'''Registering the RequestCount Middleware'''
app.before_request(request_count)


'''Registering the CounterAPI'''
app.add_url_rule('/request-count', view_func=RequestCountAPI.as_view('request_count_api'))
app.add_url_rule('/request-count/reset', view_func=ResetRequestCountAPI.as_view('reset_request_count_api'))


if __name__ == "__main__":
    app.run(debug=True)