from __future__ import with_statement

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import files
from blobfile import File;
from blobfile import getContentType;

import logging

class RepoUpload(webapp.RequestHandler):
    
    
    def post(self):
        fileupload = self.request.POST.get("file",None)
        if fileupload is None :
            logging.debug("no file provided")
            self.error(400)
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write( "No file provided")
            return

        name=fileupload.filename
        contentType = getContentType( name )
        if contentType is None:
            logging.debug("unsuported file type for " + name)
            self.error(400)
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write( "Unsupported file type: " + name)
            return

        data= fileupload.file.read()
        mimeType=contentType

        file = File.get_by_key_name(name)
        if file is not None:
            self.error(409)
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write( "Artifact with same Id/version already there ")
            return

        # Create the file
        file_name = files.blobstore.create(mime_type='application/octet-stream',_blobinfo_uploaded_filename=name)#_blobinfo_uploaded_filename not tested

        # Open the file and write to it
        with files.open(file_name, 'a') as f:
            f.write(data)

        # Finalize the file. Do this before attempting to read it.
        files.finalize(file_name)

        # Get the file's blob key
        blob_key = files.blobstore.get_blob_key(file_name)

        file = File(key_name=name,blobKey=blob_key)
        file.put()
        
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('uploaded ' + name + ' at ' + str(blob_key))


application = webapp.WSGIApplication([('/.*', RepoUpload)], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
