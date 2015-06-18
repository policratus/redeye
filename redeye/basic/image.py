"""
Contains spatial, high level transforms and utils
"""
from PIL import Image
from numpy import array
import matplotlib.pyplot as plt
from basic import io


class BasicImage(io.ImageIO):
    """
    Utility functions for images
    """
    @staticmethod
    def rotation(image, degrees=90):
        """
        Rotates the image a certain degree
        """
        rotated = image.rotate(degrees, Image.BILINEAR, False)

        return rotated

    @staticmethod
    def resize(image, width=640, height=480):
        """
        Resize a image
        """
        resized = image.resize((width, height))

        return resized

    @staticmethod
    def colorspace(image, space, size=16):
        """
        Change image to grey or its color space
        """
        if space == 'greyscale':
            newspace = image.convert('L')
        elif space == 'color':
            newspace = image.convert(
                'P',
                dither=Image.NONE,
                colors=size,
                palette=Image.ADAPTIVE
            ).convert('RGB')
        else:
            newspace = None

        return newspace

    @staticmethod
    def thumbs(image, width, height):
        """
        Create a thumbnail for image
        """
        if image.size[0] > width and image.size[1] > height:
            image.thumbnail((width, height))
            return image
        else:
            print """[THUMBS]: Thumbnail size must be lower
                  or equal to image size. Image was not
                  thumbnailed."""

    @staticmethod
    def crop(image, coordinates):
        """
        Crop a region inimage
        """
        region = image.crop(coordinates)

        return region

    def histogram(self, image, path):
        """
        Generates a image histogram
        """
        file_io = io.BasicFilesIO(path)
        image = array(self.colorspace(image, 'greyscale'))

        data, bins, patches = plt.hist(image.flatten(), 51)
        print '#### Histogram Data ###'
        print 'Data:\n', data, '\n Bins: \n', bins, '\n Patches: \n', patches
        plt.title('Histogram of pixel intensity')
        plt.xlabel('Pixel intensity')
        plt.ylabel('Frequency')
        plt.savefig(
            file_io.change_name(
                path,
                prefix='histogram-',
                extension='png'
            ),
            format='png'
        )

    @staticmethod
    def negative(image):
        """
        Invert values of colorspace
        """
        imarr = array(image)

        imarr = 255 - imarr

        return Image.fromarray(imarr)
