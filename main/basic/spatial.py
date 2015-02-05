from PIL import Image
from pylab import * 

class spatial():
    def rotation(self,image,degrees=90):
        rotated = image.rotate(degrees,Image.BILINEAR,False)

        return rotated

    def resize(self,image,width=640,height=480):
        resized = image.resize((width,height))

        return resized

    def colorspace(self,image,space,size=16):
        if space == 'greyscale':
            newspace = image.convert('L')
        elif space == 'color':
            newspace = image.convert('P',dither=Image.NONE,colors=size,palette=Image.ADAPTIVE).\
                    convert('RGB')
        else:
            newspace = None

        return newspace

    def thumbs(self,image,width,height):
        if image.size[0] > width and image.size[1] > height:
            image.thumbnail((width,height))
            return image
        else:
            print '''[THUMBS]: Thumbnail size must be lower or equal to image size.
            Image {0} was not thumbnailed.\n'''.format(filepath)

    def crop(self,image,p1,p2,p3,p4):
        coordinates = (p1,p2,p3,p4)

        region = image.crop(coordinates)
        
        return region

    def histogram(self,image,filepath):
        image = array(self.colorspace(image,'greyscale'))
        
        figure()
        hist(image.flatten(),128)
        xlim([0,255])

        savefig(filepath)
