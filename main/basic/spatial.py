from PIL import Image
from numpy import ndarray
from basic import io

class spatial():
    i = io.io()

    def rotation(self,filepath,degrees=90):
        image = self.i.open(filepath) 
        rotated = image.rotate(degrees,Image.BILINEAR,False)

        return rotated

    def resize(self,filepath,width=640,height=480):
        image = self.i.open(filepath)
        resized = image.resize((width,height))

        return resized

    def colorspace(self,filepath,space,size=16):
        image = self.i.open(filepath)

        if space == 'greyscale':
            newspace = image.convert('L')
        elif space == 'color':
            newspace = image.convert('P',dither=Image.NONE,colors=size,palette=Image.ADAPTIVE).\
                    convert('RGB')
        else:
            newspace = None

        return newspace

    def thumbs(self,filepath,width,height):
        image = self.i.open(filepath)

        if image.size[0] > width and image.size[1] > height:
            image.thumbnail((width,height))
            return image
        else:
            print '''[THUMBS]: Thumbnail size must be lower or equal to image size.
            Image {0} was not thumbnailed.\n'''.format(filepath)

    def crop(self,filepath,p1,p2,p3,p4):
        image = self.i.open(filepath)
        
        coordinates = (p1,p2,p3,p4)

        region = image.crop(coordinates)
        
        return region

    def histogram(self,filepath):
        image = self.colorspace(filepath,'greyscale')
        
        histim = image.histogram()
        
        return histim
