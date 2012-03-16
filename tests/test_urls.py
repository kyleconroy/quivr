from web import app
from mock import patch
from nose.tools import assert_equals


client = app.test_client()


get_urls = [
    "/photos",
    "/photos/1",
    "/photos/1/sizes",
    "/photos/1/favorites",
    "/photos/1/comments",
    "/photos/1/people",
    "/photos/1/suggestions",
    "/photos/1/notes",
    "/photos/1/galleries",
    "/activity",
    "/favorites",
    "/photosets",
    "/photosets/1",
    "/photosets/1/comments",
    "/galleries",
    "/galleries/1",
    "/galleries/1/photos",
    "/galleries/1/photos/1",
    "/tags",
    "/blogs",
    "/blogs/1",
    "/collections",
    "/collections/1",
    "/users/1",
    "/users/1/favorites",
    "/users/1/groups",
    "/users/1/photos",
    "/users/1/contacts",
    "/login/oauth/authorize",
    "/groups",
    "/groups/1",
    "/groups/1/photos",
]

post_urls = [
    "/login/oauth/access_token",
]


def test_valid_get_url():
    for url in get_urls:
        yield check_valid_get_url, url


def check_valid_get_url(url):
    with patch("web.flickr.api") as mock:
        mock.return_value = {}
        resp = client.get(url)
        assert_equals(resp.status_code, 200)

def test_valid_post_url():
    for url in post_urls:
        yield check_valid_url, url


def check_valid_url(url):
    with patch("web.flickr.api") as mock:
        mock.return_value = {}
        resp = client.post(url)
        assert_equals(resp.status_code, 200)

