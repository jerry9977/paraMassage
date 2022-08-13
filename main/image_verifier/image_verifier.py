
from PIL import Image
from urllib import request as req
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO

from django.core.exceptions import ValidationError

class ImageVerifier:

    def __init__(self, data_url, field_name, allow_null, form):
        self.data_url = data_url
        self.field_name = field_name
        self.allow_null = allow_null
        self.form = form
        self.memory_file = None
    def is_valid(self):
        if not self.data_url:
            if self.allow_null:
                return True
            else:
                self.form.add_error(self.field_name, ValidationError("This field is required"))
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
            field_name="back_image", 
            name="back", 
            content_type="image/jpeg",
            size=BytesIO(byte).getbuffer().nbytes, 
            charset=None
        )
        return self.memory_file.file