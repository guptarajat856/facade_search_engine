from main_app import app
import threading
import urllib2
import time
from flask import request, jsonify
from main_app.utils import fetch_data


@app.route('/')
def main_route():
    query = request.args.get('q')
    if not query:
        return jsonify({
                'error': 'Empty query passed'
            }), 400
    
    return_data = fetch_data(query)

    final_response = {}
    final_response['query'] = query
    final_response['results'] = return_data

    return jsonify(final_response)