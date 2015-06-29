"""
Contains spatial, high level transforms and utils
"""
from PIL import Image, ImageFilter
import numpy as np
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
    def color_space(image, space, size=16):
        """
        Change image to grey or its color space
        """
        if space == 'greyscale':
            new_space = image.convert('L')
        elif space == 'color':
            new_space = image.convert(
                'P',
                dither=Image.NONE,
                palette=Image.ADAPTIVE,
                colors=size
            ).convert('RGB')
        else:
            new_space = None

        return new_space

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
        image = self.to_array(self.color_space(image, 'greyscale'))

        _, _, _ = plt.hist(image.flatten(), 51)
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

    def negative(self, image):
        """
        Invert values of color_space
        """
        imarr = self.to_array(image)

        imarr = 255 - imarr

        return Image.fromarray(imarr)

    @staticmethod
    def channel_lim(value):
        """
        Convert a RGB value from 0-255 to
        0-1 range
        """
        return value / 255

    @staticmethod
    def to_array(image):
        """
        Convert a PIL Image object
        to numpy array
        """
        return np.array(image)

class FilterImage(BasicImage):
    """
    Encapsulates basic filters
    """
    def histogram_equalization(self, image):
        """
        Perform a histogram equalization
        """
        image_array = self.to_array(self.color_space(image, 'greyscale'))
        image_array_flat = image_array.flatten()

        im_histogram, bins = np.histogram(image_array_flat)

        norm_cumulative_dist = 255 * im_histogram.cumsum() \
            / im_histogram.cumsum()[-1]

        equalized_image = np.interp(
            image_array_flat,
            bins[:-1],
            norm_cumulative_dist
        )

        equalized_image = equalized_image.reshape(image_array.shape)

        return Image.fromarray(equalized_image)

    def gaussian(self, image):
        """
        Applies a Gaussian filter
        """
        if image.mode != 'RGB':
            image = image.convert('RGB')

        gauss = ImageFilter.GaussianBlur()

        return image.filter(gauss)
