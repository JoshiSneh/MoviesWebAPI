from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from models.collections import Collection
from models.movies import Movie



class CollectionAPI(MethodView):
    @jwt_required()
    def post(self):
        '''
            This endpoint will create a collection

            Request Payload:
            {
                “title”: “<Title of the collection>”,
                “description”: “<Description of the collection>”,
                “movies”: [
                        {
                            “title”: <title of the movie>,
                            “description”: <description of the movie>,
                            “genres”: <generes>,
                            “uuid”: <uuid>
                        }, ...
                ]
            }

            Response Payload:
            {
                “collection_uuid”: <uuid of the collection item>
            }

        '''
        try:
            data = request.get_json()

            if not ("title" in data):
                return jsonify({"message":"title is required"}), 404

            if not ("description" in data):
                return jsonify({"message":"description is required"}), 404
            
            if not ("movies" in data):
                return jsonify({"message":"movies are required"}), 404

            title = data["title"]
            description = data["description"]
            movies = data["movies"]
            
            if not (title and description and movies):
                return jsonify({"message":"title, description and movies are required"}), 404
            
            user_name = get_jwt_identity()
            print(user_name)

            '''Creating a New Collection'''
            new_collection = Collection(title=title,description=description,username=user_name)
            db.session.add(new_collection)
            db.session.commit()

            '''Adding a Movie to the collection'''
            for movie_data in movies:
                movie_title = movie_data.get('title')
                movie_description = movie_data.get('description')
                movie_genres = movie_data.get('genres')
                movie_uuid = movie_data.get('uuid')

                new_movie = Movie(
                    title=movie_title,
                    description=movie_description,
                    genres=movie_genres,
                    uuid=movie_uuid,
                    collection_id=new_collection.id
                )
                db.session.add(new_movie)
            db.session.commit()

            return jsonify({'collection_uuid': new_collection.uuid}), 201
        except Exception as e:
            return jsonify({'error': e}), 500

    @jwt_required()
    def get(self):
        '''
            This endpoint will fetch all the collection of a user

            Response Payload:
            {
                “is_success”: True,
                “data”: {
                    “collections”: [
                    {
                        “title”: “<Title of my collection>”,
                        “uuid”: “<uuid of the collection name>”
                        “description”: “My description of the collection.”
                    },
                    ...
                    ],
                    “favourite_genres”: “<My top 3 favorite genres based on the
                    movies I have added in my collections>.”
                }
            }
        '''   
        try:
            user_name = get_jwt_identity()
            collections = Collection.query.filter_by(username=user_name).all()

            if not collections:
                return jsonify({"message":"no collections found for the user!"}), 404

            collection_data = []
            favorite_genres = []
            
            for collection in collections:
                collection_data.append({
                    'title': collection.title,
                    'uuid': collection.uuid,
                    'description': collection.description
                })

                movies = Movie.query.filter_by(collection_id=collection.id).all()

                for movie in movies:
                    if movie.genres:
                        favorite_genres.append(movie.genres.split(','))


            map_list = {}
            
            '''Below code is for sorting the top 3 genre of a user from its collection'''
            for fav_gene in favorite_genres:
                for indi_fav_gen in fav_gene:
                    if indi_fav_gen in map_list:
                        map_list[indi_fav_gen]+=1
                    else:
                        map_list[indi_fav_gen]=1

            sorted_fav_genere = sorted(map_list.items(), key=lambda item: item[1], reverse=True)[:3]
            
            fav_top_3_genere = [genre[0] for genre in sorted_fav_genere]


            response_data = {
                'is_success': True,
                'data': {
                    'collections': collection_data,
                    'favorite_genres': fav_top_3_genere
                }
            }
            return jsonify(response_data), 200
        except Exception as e:
            return jsonify({'error': e}), 500

class CollectionByUUIDAPI(MethodView):
    @jwt_required()
    def get(self, uuid):
        '''
            This endpoint will fetch the collection by UUID

            Response Payload:
            { 
                “title”: <Title of the collection>,
                “description”: <Description of the collection>,
                “movies”: <Details of movies in my collection>
            }
        '''
        try:
            get_collection = Collection.query.filter_by(uuid=uuid).first()

            if not get_collection:
                return jsonify({"message":"no collection exist with the given uuid"}), 404
            
            '''Creating the collection data'''
            collection_data = {
                "title":get_collection.title,
                "description":get_collection.description,
                "movies":[]
            }

            '''Fetching the Movie data with the collection id'''
            get_movies = Movie.query.filter_by(collection_id=get_collection.id).all()

            for movie in get_movies:
                movie_data = {
                    'title':movie.title,
                    'description':movie.description,
                    'genres':movie.genres,
                    "uuid":movie.uuid
                }
                collection_data["movies"].append(movie_data)

            return jsonify(collection_data), 200

        except Exception as e:
            return jsonify({'error':e})

    @jwt_required()
    def put(self, uuid):
        '''
            This endpoint will update the collection by UUID

            Request Payload:
            {
                “title”: <Optional updated title>,
                “description”: <Optional updated description>,
                “movies”: <Optional movie list to be updated>,
            }
            
            Response Payload:
            {'message': 'collection updated successfully'}
        '''
        try:
            data = request.get_json()
            get_collection = Collection.query.filter_by(uuid=uuid).first()
            
            if not get_collection:
                 return jsonify({"message":"no collection exist with the given uuid"}), 404
            
            '''Checking for the title in the input json'''
            if "title" in data:
                get_collection.title = data['title']

            '''Checking for the description in the input json'''
            if "description" in data:
                get_collection.description = data["description"]

            '''Checking for the movies in the input json'''
            if "movies" in data:
                for movie_data in data["movies"]:
                    movie_title = movie_data.get('title')
                    movie_description = movie_data.get('description')
                    movie_genres = movie_data.get('genres')
                    movie_uuid = movie_data.get('uuid')

                    new_movie = Movie(
                        title=movie_title,
                        description=movie_description,
                        genres=movie_genres,
                        uuid=movie_uuid,
                        collection_id=get_collection.id
                    )

                    db.session.add(new_movie)

            db.session.commit()
            return jsonify({'message': 'collection updated successfully'}), 200
        except Exception as e:
            return jsonify({'error':e})

    @jwt_required()
    def delete(self, uuid):
        '''
            This endpoint will delete the collection by UUID

            Request Payload: ""
            
            Response Payload:
            {'message': 'collection deleted successfully'}
        '''
        try:
            get_collection = Collection.query.filter_by(uuid=uuid).first()
            if get_collection:
                db.session.delete(get_collection)
                db.session.commit()
                return jsonify({'message': 'collection deleted successfully'}), 200
            else:
                 return jsonify({"message":"no collection exist with the given uuid"}), 404
        except Exception as e:
            return jsonify({'error':e})



