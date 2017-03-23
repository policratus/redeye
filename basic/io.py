"""
Contains basic operations related to files, images, etc
"""
import os
import numpy
from PIL import Image
import magic
import jellyfish
from config import properties


class BasicIO(object):
    """
    Contains basic IO operations
    """
    @classmethod
    def ls_dir(cls, path):
        """
        List directory contents
        """
        files = os.listdir(path)

        for ffile in files:
            if cls.is_file(
                    os.path.abspath(path) + '/' + ffile
            ):
                yield ffile

    @staticmethod
    def rm_file(filepath):
        """
        Delete a file
        """
        try:
            os.remove(filepath)
        except IOError as io_error:
            print '[BasicIO] The following I/O error occurred: {0}'.format(
                io_error
            )

    @staticmethod
    def mime_file(path):
        """
        Returns the mime type of passed file

        Parameters
        ----------
        path: str
            Path of file to discover mime type
        """
        magic_file = magic.Magic(mime=True, uncompress=True)

        return magic_file.from_file(path)

    @staticmethod
    def is_file(path):
        """
        Tests if a passed path resolves to
        a file or wherever else (like dirs)
        """
        return os.path.isfile(path)

    @staticmethod
    def extension(path):
        """
        Returns the last part of file
        extension

        Parameters
        ----------
        path: str
            The path of file to return
            the last extension
        """
        return os.path.splitext(path)[1].replace('.', '')

class BasicFilesIO(BasicIO):
    """
    File utilities
    """
    @staticmethod
    def absolute_path(file_name, path):
        """
        Mount an absolute path
        """
        return os.path.join(file_name, path)

    def file_list(self, path):
        """
        Creates a file list from a determined path
        """
        if os.path.exists(path):
            working_dir = path
        else:
            raise IOError("File path doesn't exists")

        config = properties.Properties('Image')
        files = []

        try:
            if working_dir:
                for file_dir in self.ls_dir(working_dir):
                    if file_dir.endswith(
                            tuple(
                                config.multi_value(
                                    'SupportedFileExtensions'
                                )
                            )
                    ):
                        files.append(
                            self.absolute_path(
                                working_dir, file_dir
                            )
                        )

            if files:
                return files
            else:
                return None
        except OSError as os_error:
            print 'System error: {0}'.format(os_error)

    @staticmethod
    def change_name(file_path, prefix='', suffix='', extension=''):
        """
        Change the name of a file
        contained in strings
        """
        split_path = os.path.split(file_path)
        path, file_name = split_path[0], os.path.splitext(split_path[1])[0]

        return path + '/' + prefix + file_name + suffix + '.' + extension

    @classmethod
    def is_this_type(cls, path):
        """
        Verify if the mime type of file
        is coherent to its extension

        Parameters
        ----------
        path: str
            Path where the file resides.
        """
        mime_type = cls.mime_file(path)
        actual_type = mime_type.split('/')[1]

        actual_extension = cls.extension(path)

        return jellyfish.jaro_distance(
            unicode(actual_type),
            unicode(actual_extension)
        ) >= 0.9

class ImageIO(BasicFilesIO):
    """
    Basic image operations
    """
    images = []

    @staticmethod
    def open_image(path):
        """
        Open an image, returning its pixel matrix
        """
        try:
            return Image.open(path)
        except IOError as io_error:
            print '[IO] Error open_imageing file: {0}'.format(io_error)

    @staticmethod
    def save(image, path):
        """
        Save file in format especified by extension
        """
        try:
            image.save(path)
        except IOError as io_error:
            print '[IO] Error saving file: {0}'.format(io_error)

    @staticmethod
    def show(image):
        """
        Display an image
        """
        image.show()

    def load_all(self, path):
        """
        Open images in batch and append it to a list
        """
        files_io = BasicFilesIO()
        config = properties.Properties('Image')
        max_open_image_files = int(config.section('MaxBatchImageOpen'))

        files = files_io.file_list(path)

        for image_file in files[:max_open_image_files]:
            self.images.append(self.open_image(image_file))

    def show_all(self, path, refresh=False):
        """
        Display all the images in working path
        """
        if not self.images or refresh:
            self.load_all(path)

        for image in self.images:
            self.show(image)

    @staticmethod
    def array_to_image(array):
        """
        Converts a numpy array representing a
        image to its bitmap representation

        Parameters
        ----------
        array: numpy.ndarray
            Array representing image
        """
        return Image.fromarray(array)

    @staticmethod
    def matrix_of_ns(order, unity=0):
        """
        Return an square 2D array filled with specified
        integer. Useful for kernels.

        Parameters
        ----------
        order: int
            Defining the order of the square matrix.
        unity: int
            Optional unity of array. By default, zero.
        """
        if isinstance(order, int) and \
                isinstance(unity, int):
            if unity == 0:
                return numpy.zeros((order, order), dtype=numpy.int)
            elif unity == 1:
                return numpy.ones((order, order), dtype=numpy.int)
            else:
                array = numpy.zeros((order, order), dtype=numpy.int)
                array.fill(unity)

                return array

    @staticmethod
    def to_array(obj, array_type='uint8'):
        """
        Convert a object
        to numpy array

        Parameters
        ----------
        obj: Object
            An instance of object which the conversion
            is possible
        array_type: str
            Numpy type for the array
        """
        return numpy.array(obj, array_type)

    @staticmethod
    def append_arrays(arrays):
        """
        Appends two or more arrays

        Parameters
        ----------
        arrays: tuple
            A tuple containing two or more arrays
            to append
        """
        if isinstance(arrays, tuple) and len(arrays) >= 2:
            return numpy.concatenate(arrays)

    @classmethod
    def image_shape(cls, image):
        """
        Returns the shape (dimensions) of image
        """
        return cls.to_array(image).shape
