
from PIL import Image
from urllib import request as req
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO

from django.core.exceptions import ValidationError

class ImageVerifier:

    def __init__(self, data_url, allow_null=True):
        self.data_url = data_url
        self.memory_file = None
        self.allow_null = allow_null
    def is_valid(self):
        if not self.data_url:
            if self.allow_null:
                return True
            else:
                return False

        try:
            byte = self._data_url_to_byte(self.data_url)
        except Exception as e:
            print("Fail to convert data url to byte")
            print(e)
            return False

        try:
            file = self._byte_to_file(byte)
        except Exception as e:
            print("Fail to convert byte to file")
            print(e)
            return False
        
        try:
            image = Image.open(file)
            image.verify()
            return True
        except Exception as e:
            print("Fail to verify image")
            print(e)
            return False

    def _data_url_to_byte(self, data_url):
        with req.urlopen(data_url) as response:
            return response.read()
            
    def _byte_to_file(self, byte):
        self.memory_file = InMemoryUploadedFile(
            file=BytesIO(byte), 
            field_name="body_image", 
            name="body", 
            content_type="image/jpeg",
            size=BytesIO(byte).getbuffer().nbytes, 
            charset=None
        )
        return self.memory_file.file
    
class CustomMemoryFile:

    def __init__(self, data_url):
        self.data_url = data_url
        self.memory_file = None
        try:
            byte = self._data_url_to_byte(self.data_url)
        except Exception as e:
            print("Fail to convert data url to byte")
            print(e)

        try:
            file = self._byte_to_file(byte)
        except Exception as e:
            print("Fail to convert byte to file")
            print(e)

    def _data_url_to_byte(self, data_url):
        with req.urlopen(data_url) as response:
            return response.read()
            
    def _byte_to_file(self, byte):
        self.memory_file = InMemoryUploadedFile(
            file=BytesIO(byte), 
            field_name="image", 
            name="body.jpg", 
            content_type="image/jpeg",
            size=BytesIO(byte).getbuffer().nbytes, 
            charset=None
        )