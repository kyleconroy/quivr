import os
import urllib

def scrape():
    try:
        os.mkdir("flickr_docs")
    except IOError:
        pass

    for method in open("methods.txt"):
        method = method.strip()
        doc_path = os.path.join("flickr_docs", "{}.html".format(method))
        if os.path.exists(doc_path):
            continue
        url = "http://www.flickr.com/services/api/{}.html".format(method)
        print url
        urllib.urlretrieve(url, doc_path)

scrape()
