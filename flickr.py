import os
import hashlib
import requests
import json

FLICKR_BASE = "http://api.flickr.com/services/rest/"

def api(method, **kwargs):
    kwargs.update({
        "method": "flickr.{}".format(method),
        "format": "json",
        "nojsoncallback": "1",
        "api_key": os.environ["FLICKR_KEY"],
        "auth_token": os.environ["FLICKR_AUTH_TOKEN"],
        })

    # Signature validation
    sig = ''.join([str(u[0]) + str(u[1]) for u in sorted(kwargs.items())])
    kwargs["api_sig"] = hashlib.md5(os.environ["FLICKR_SECRET"] + sig).hexdigest()

    resp = requests.post(FLICKR_BASE, params=kwargs)
    return json.loads(resp.content)
