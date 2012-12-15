from google.appengine.ext import db
from google.appengine.ext.blobstore import BlobReferenceProperty

class File(db.Model):
    blobKey = BlobReferenceProperty(required=True)



def getContentType( filename ): # lists and converts supported file extensions to MIME type
    ext = filename.split('.')[-1].lower()
    if ext == 'zip' : return 'application/zip'
    return None

