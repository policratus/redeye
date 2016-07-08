"""
Contains spatial, high level transforms and utils
"""
from PIL import Image, ImageFilter
import numpy
import matplotlib.pyplot as plot
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

    def histogram(self, image, path, file_prefix='histogram'):
        """
        Generates a image histogram
        """
        image = self.to_array(self.color_space(image, 'greyscale'))

        plot.hist(image.flatten(), 52)
        plot.title('Histogram of pixel intensity')
        plot.xlabel('Pixel intensity')
        plot.ylabel('Frequency')
        plot.savefig(
            self.change_name(
                path,
                prefix=file_prefix + '-',
                extension='png'
            ),
            format='png'
        )
        plot.clf()

    def negative(self, image):
        """
        Invert values of color_space
        """
        imarr = self.to_array(image)

        imarr = 255 - imarr

        return self.array_to_image(imarr)

    @staticmethod
    def channel_lim(value):
        """
        Convert a RGB value from 0-255 to
        0-1 range
        """
        return value / 255

    @staticmethod
    def show_image_gallery(title, images, rows, columns, shape=()):
        """
        Plot or save two or more (processed) images

        Parameters
        ----------
        title: str
            Title of the plot (which will appear top centered)
        images: numpy.ndarray
            A numpy array containing image data
        rows: int
            Number of rows to plot
        columns: int
            Number of columns to plot
        shape: tuple
            A tuple containing the dimensions of image
            (used for reshaping the array if it was flatten)
        """
        plot.suptitle(title, size=30)

        for index, image in enumerate(images):
            if shape:
                image = image.reshape(shape)

            plot.subplot(rows, columns, index + 1)
            luminosity_max = max(image.max(), -image.min())
            plot.imshow(
                image,
                cmap=plot.cm.gray,
                vmin=-luminosity_max,
                vmax=luminosity_max
            )

            plot.xticks(())
            plot.yticks(())

        return plot

    @classmethod
    def save_image_gallery(cls, path, title, images, rows, columns, shape=(), prefix=''):
        """
        Saves a image gallery to disk

        Parameters
        ----------
        path: str
            Path which the gallery will be saved
        title: str
            Title of the plot (which will appear top centered)
        images: numpy.ndarray
            A numpy array containing image data
        rows: int
            Number of rows to plot
        columns: int
            Number of columns to plot
        shape: tuple
            A tuple containing the dimensions of image
            (used for reshaping the array if it was flatten)
        """
        plot_to_save = cls.show_image_gallery(
            title,
            images,
            rows,
            columns,
            shape
        )

        plot_to_save.savefig(
            cls.change_name(
                path,
                prefix=prefix,
                extension='png'
            ),
            format='png'
        )

    @staticmethod
    def flattened_images_centering(images_array):
        """
        Centers (globally and locally) arrays containing
        flattened image arrays (one dimensional)

        Parameters
        ----------
        images_array: numpy.ndarray
            A numpy array with arrays of flattened
            images
        """
        samples, _ = images_array.shape

        images_array = images_array - images_array.mean(axis=0)
        images_array -= images_array.mean(axis=1).reshape(samples, -1)

        return images_array

class FilterImage(BasicImage):
    """
    Encapsulates basic filters
    """
    def execute_histogram_equalization(self, image):
        """
        Perform a histogram equalization

        Parameters
        ----------
        image: PIL Image Object
        """
        image_array = self.to_array(self.color_space(image, 'greyscale'))
        image_array_flat = image_array.flatten()

        im_histogram, bins = numpy.histogram(image_array_flat)

        norm_cumulative_dist = 255 * im_histogram.cumsum() \
            / im_histogram.cumsum()[-1]

        equalized_image = numpy.interp(
            image_array_flat,
            bins[:-1],
            norm_cumulative_dist
        )

        equalized_image = equalized_image.reshape(image_array.shape)

        return self.color_space(self.array_to_image(equalized_image), 'greyscale')

    def save_histogram_equalization(self, path):
        """
        Executes an histogram equalization on the Greyscale level
        and export the histograms before and after transformation

        Parameters
        ----------
        image: PIL Image Object
        path: str
            Path of image to be processed
        """
        image = Image.open(path)

        self.histogram(image, path, 'histogram-before-equalization')

        equalized_image = self.execute_histogram_equalization(image)

        self.histogram(equalized_image, path, 'histogram-after-equalization')

        self.save(equalized_image, path)

    def polynomial_graylevel_transform(self, image, degree=2):
        """
        Transform the graylevel information on the image,
        applying a polynomial transformation, which turns
        dark pixels darker.

        Parameters
        ----------
        degree : int
            Degree used to transform the image polynomially
        """
        if isinstance(degree, int):
            image = self.color_space(image, 'greyscale')
            imarr = self.to_array(image)

            return self.color_space(
                self.array_to_image(255.0 * (imarr / 255.0) ** degree), 'greyscale'
            )

    @staticmethod
    def gaussian(image):
        """
        Applies a Gaussian filter
        """
        if image.mode != 'RGB':
            image = image.convert('RGB')

        gauss = ImageFilter.GaussianBlur()

        return image.filter(gauss)
