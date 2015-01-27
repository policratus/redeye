from PIL import Image
from basic import io

class spatial():
    i = io.io()

    def rotation(self,filepath,degrees=90):
        image = self.i.open(filepath) 
        rotated = image.rotate(degrees,Image.BILINEAR,False)

        self.i.save(rotated,filepath)

    def resize(self,filepath,width=640,height=480):
        image = self.i.open(filepath)
        resized = image.resize((width,height))

        self.i.save(resized,filepath)

    def colorspace(self,filepath,space,size=16):
        image = self.i.open(filepath)

        if space == 'greyscale':
            newspace = image.convert('L')
        elif space == 'color':
            newspace = image.convert('P',dither=Image.NONE,colors=size,palette=Image.ADAPTIVE).\
                    convert('RGB')
        else:
            newspace = None

        self.i.save(newspace,filepath)

    def thumbs(self,filepath):
        thumb = self.i.open(filepath)
        thumb.thumbnail((64,64))
        self.i.save(thumb,filepath)
