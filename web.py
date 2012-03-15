import os
import flickr
from flask import Flask, jsonify, abort, make_response, request

# Reddit 6837818396
# Me 6839706724

app = Flask(__name__)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

