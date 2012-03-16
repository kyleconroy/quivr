import os
import flickr
from flask import Flask, jsonify, abort, make_response, request
from flask.views import MethodView

# Reddit 6837818396
# Me 6839706724

app = Flask(__name__)

class Root(MethodView):

    def get(self):
        return jsonify({"links": {"photos": request.url + "photos"}})


class Photos(MethodView):

    def get(self):
        data = flickr.api("photos.getRecent", page=request.args.get("page", 1))

        try:
            next_page = int(data["photos"]["page"]) + 1
            prev_page = max(int(data["photos"]["page"]) - 1, 1)
            photos = data["photos"]["photo"],
        except KeyError:
            next_page = 2
            prev_page = 1
            photos = []

        return jsonify({
            "photos": [],
            "paging": {
                "next": "{}?page={}".format(request.base_url, next_page),
                "prev": "{}?page={}".format(request.base_url, prev_page),
            }
        })


class Photo(MethodView):

    def get(self, photo_id):
        return jsonify(flickr.api("photos.getInfo", photo_id=photo_id))

    def post(self, photo_id):
        if "tags" in request.form:
            flickr.api("photos.setTags", photo_id=photo_id,
                                         tags=request.form["tags"])
        return jsonify(flickr.api("photos.getInfo", photo_id=photo_id))

    def delete(self, photo_id):
        flickr.api("photos.delete", photo_id=photo_id)
        return make_response("", 204)


class Sizes(MethodView):

    def get(self, photo_id):
        return jsonify(flickr.api("photos.getSizes", photo_id=photo_id))


class Favs(MethodView):

    def get(self, photo_id):
        return jsonify(flickr.api("photos.getFavorites", photo_id=photo_id))


class Comments(MethodView):

    def get(self, photo_id):
        return jsonify(flickr.api("photos.comments.getList", photo_id=photo_id))


class Notes(MethodView):

    def get(self, photo_id):
        return jsonify(flickr.api("photos.notes.getList", photo_id=photo_id))


class People(MethodView):

    def get(self, photo_id):
        return jsonify(flickr.api("photos.people.getList", photo_id=photo_id))


class Suggestions(MethodView):

    def get(self, photo_id):
        return jsonify(flickr.api("photos.suggestions.getList",
                       photo_id=photo_id))


class PhotoGalleries(MethodView):

    def get(self, photo_id):
        return jsonify(flickr.api("photos.galleries.getListForPhoto", 
                       photo_id=photo_id))


class UserFavorites(MethodView):

    def get(self):
        return jsonify(flickr.api("photos.favorites.getList"))


class Photosets(MethodView):

    def get(self):
        return jsonify(flickr.api("photosets.getList"))


class Photoset(MethodView):

    def get(self, set_id):
        return jsonify(flickr.api("photosets.getInfo", set_id=set_id))


class PhotosetComments(MethodView):

    def get(self, set_id):
        return jsonify(flickr.api("photosets.comments.getList", set_id=set_id))


class Tags(MethodView):

    def get(self):
        return jsonify(flickr.api("photosets.tags.getListUser"))


class Galleries(MethodView):

    def get(self):
        return jsonify(flickr.api("photos.galleries.getList"))


class Gallery(MethodView):

    def get(self, gallery_id):
        return jsonify(flickr.api("photos.galleries.getInfo", 
                       gallery_id=gallery_id))


class GalleryPhotos(MethodView):

    def get(self, gallery_id):
        return jsonify(flickr.api("photos.galleries.getPhotos", 
                       gallery_id=gallery_id))


class GalleryPhoto(MethodView):

    def get(self, gallery_id, photo_id):
        return jsonify({})

    def post(self, gallery_id, photo_id):
        return jsonify(flickr.api("photos.galleries.editPhoto", 
                       gallery_id=gallery_id, photo_id=photo_id))


class Activity(MethodView):

    def get(self):
        return jsonify(flickr.api("photos.activity.userComments"))


class Blogs(MethodView):

    def get(self):
        return jsonify(flickr.api("blogs.getList"))


class Blog(MethodView):

    def get(self, blog_id):
        return jsonify({})

    def post(self, blog_id):
        """Not sure about this endpoint"""
        return jsonify(flickr.api("blogs.postPhoto", blog_id=blog_id))


class Collection(MethodView):

    def get(self, collection_id):
        return jsonify(flickr.api("collections.getInfo",
                       collection_id=collection_id))


class Collections(MethodView):

    def get(self):
        return jsonify({})


class Authorize(MethodView):

    def get(self):
        return jsonify({})


class Token(MethodView):

    def post(self):
        return jsonify({})


class User(MethodView):

    def get(self, user_id):
        return jsonify({})


class PublicFavorites(MethodView):

    def get(self, user_id):
        return jsonify(flickr.api("favorites.getPublicList", user_id=user_id))


class PublicContacts(MethodView):

    def get(self, user_id):
        return jsonify(flickr.api("contacts.getPublicList", user_id=user_id))


def add_view(url, view):
    app.add_url_rule(url, view_func=view.as_view(str(view).lower()))


add_view('/', Root)
add_view('/photos', Photos)
add_view('/photos/<photo_id>', Photo)
add_view('/photos/<photo_id>/favorites', Favs)
add_view('/photos/<photo_id>/sizes', Sizes)
add_view('/photos/<photo_id>/comments', Comments)
add_view('/photos/<photo_id>/notes', Notes)
add_view('/photos/<photo_id>/people', People)
add_view('/photos/<photo_id>/suggestions', Suggestions)
add_view('/photos/<photo_id>/galleries', PhotoGalleries)
add_view('/favorites', UserFavorites)
add_view('/photosets', Photosets)
add_view('/photosets/<set_id>', Photoset)
add_view('/photosets/<set_id>/comments', PhotosetComments)
add_view('/tags', Tags)
add_view('/galleries', Galleries)
add_view('/galleries/<gallery_id>', Gallery)
add_view('/galleries/<gallery_id>/photos', GalleryPhotos)
add_view('/galleries/<gallery_id>/photos/<photo_id>', GalleryPhoto)
add_view('/activity', Activity)
add_view('/login/oauth/authorize', Authorize)
add_view('/login/oauth/access_token', Token)
add_view('/blogs', Blogs)
add_view('/blogs/<blog_id>', Blog)
add_view('/collections', Collections)
add_view('/collections/<collection_id>', Collection)
add_view('/users/<user_id>', User)
add_view('/users/<user_id>/favorites', PublicFavorites)
add_view('/users/<user_id>/contacts', PublicContacts)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

