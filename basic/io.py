"""
Contains basic operations related to files, images, etc
"""
import os
from PIL import Image
from config import properties


class BasicIO(object):
    """
    Contains basic IO operations
    """
    @staticmethod
    def ls_dir(path):
        """
        List directory contents
        """
        return os.listdir(path)

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

            return files
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
