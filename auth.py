import flickrapi
import os

api_key = os.environ["FLICKR_KEY"]
api_secret = os.environ["FLICKR_SECRET"]

flickr = flickrapi.FlickrAPI(api_key, api_secret)

(token, frob) = flickr.get_token_part_one(perms='delete')

if not token:
    raw_input("Press ENTER after you authorized this program")

print flickr.get_token_part_two((token, frob))
