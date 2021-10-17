import os
import json
from datetime import datetime, timezone, timedelta
from flask import Flask, jsonify, request
import jwt
from .encoder import MyJSONEncoder
from .db import get_db, init_db
from .auth import get_aut_token, validate_auth_token

def create_app():
    app = Flask(__name__)
    app.json_encoder = MyJSONEncoder

    @app.route("/")
    def index():
        return "Hello World!"

    @app.post('/authorize')
    def authorize():
        try:
            data = json.loads(request.data.decode("utf8"))
            username = data.get('username')
            password = data.get('password')

            token = get_aut_token(username, password)
            if token:
                return jsonify({'auth_token': token})
            else:
                app.logger.warning("%s / %s", username, password)
                return jsonify({'error': "permission denied"}), 403
        except Exception as ex:
            app.logger.exception(ex)
            return jsonify({'error': str(ex)}), 400


    @app.get('/accounts')
    def accounts():
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ""
        auth = validate_auth_token(auth_token)
        if not auth:
            return jsonify({'error': "permission denied"}), 403

        sort = request.args.get('sort')
        sort_dir = request.args.get('sort_dir')
        limit = request.args.get('limit')
        country = request.args.get('country')
        mfa = request.args.get('mfa')
        name = request.args.get('name')
        next_cursor = request.args.get('next_cursor')

        if sort not in ["amt", "createdDate"]:
            sort = "createdDate"
        
        # parse and determine sort order
        if not sort_dir:
            sort_dir = 1
        else:
            try:
                sort_dir = float(sort_dir)
                if sort_dir > 0:
                    sort_dir = 1
                else:
                    sort_dir = -1
            except:
                sort_dir = 1

        # parse results per page
        if not limit or not limit.isnumeric():
            limit = 10
        else:
            limit = int(limit)

        # filter results
        search_filter = {}
        if country:
            search_filter['country'] = country
        if mfa:
            search_filter['mfa'] = mfa
        if name:
            # filter name by first or last name match, can change to regex for partial match
            search_filter['$or'] = [{'firstName': name}, {'lastName': name}]
        if next_cursor:
            # pagination, seek to next result based on next_cursor from previous result set
            try:
                if sort_dir > 0:
                    sort_dir_key = '$gte'
                else:
                    sort_dir_key = '$lte'

                if sort == "createdDate":
                    next_value = datetime.fromisoformat(next_cursor)    
                elif sort == "amt":
                    next_value = int(next_cursor)
                else:
                    next_value = None

                if next_value:
                    sort_value = {}
                    sort_value[sort_dir_key] = next_value
                    search_filter[sort] = sort_value
            except Exception as ex:
                app.logger.exception(ex)
        
        app.logger.info(search_filter)

        db = get_db()
        total_results = db.accounts.count_documents(search_filter)
        results = db.accounts.find(search_filter).limit(limit + 1).sort(sort, sort_dir)
        
        # we fetched one more result than requested so we know what the
        # next result set should start at for pagination
        results = list(results)
        if len(results) > limit:
            last = results.pop()
            next_cursor = last.get(sort)
        else:
            next_cursor = None

        response = {
            'results': results,
            'total_results': total_results,
            'next_cursor': next_cursor
        }
        return jsonify(response)

    init_result = init_db(app)
    app.logger.info("inserted %d docs", init_result)

    return app
