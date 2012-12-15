from __future__ import with_statement

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.blobstore import BlobReader
from blobfile import File;

class RepoDownload(webapp.RequestHandler):
    
    
    def get(self):
        fileName = self.request.url[self.request.url.rfind('/')+1:]

        file = File.get_by_key_name(fileName)
        if file is None:
            self.error(404)
            return

        blob_key =  file.blobKey.key()
        blob_reader = BlobReader(blob_key)
        value = blob_reader.read() #TODO : test as it is not recommended for big files (https://developers.google.com/appengine/docs/python/blobstore/blobreaderclass)
        
        self.response.headers['Content-Type'] = 'application/octet-stream'
        self.response.out.write(value);


application = webapp.WSGIApplication([('.*', RepoDownload)], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
