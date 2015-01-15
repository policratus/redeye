from PIL import Image
from basic import io

class spatial():
    def rotation(self,filepath,degrees=90):
        fio = io.io() 
        image = fio.open(filepath) 
        rotated = image.rotate(degrees)
        return rotated
