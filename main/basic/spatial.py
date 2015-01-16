from PIL import Image
from basic import io

class spatial():
    fio = io.io() 

    def rotation(self,filepath,degrees=90):
        image = self.fio.open(filepath) 
        rotated = image.rotate(degrees)
        return rotated

    def resize(self,filepath,width=640,height=480):
        image = self.fio.open(filepath)
        resized = image.resize((width,height))
        return resized

    def colorspace(self,filepath,space):
        image = self.fio.open(filepath)

        if space == 'greyscale':
            newspace = image.convert('L')
        else:
            newspace = None

        return newspace
