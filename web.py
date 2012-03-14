import os
import requests
import json
from flask import Flask, jsonify, abort, make_response, request

FLICKR_BASE = "http://api.flickr.com/services/rest/"

app = Flask(__name__)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

