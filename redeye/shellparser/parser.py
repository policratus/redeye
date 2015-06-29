"""
Contains parsing for shell arguments
"""
import argparse


class Parser(object):
    """
    Methods for shell parsing
    """
    @staticmethod
    def construct_parser():
        """
        Construct parsers for arguments
        """
        psh = argparse.ArgumentParser()

        psh.add_argument(
            'path',
            help='Path for image files'
        )

        psh.add_argument(
            '--colorspace',
            help='Perform operations on color space of images',
            choices=['greyscale', 'color'],
            metavar='space'
        )

        psh.add_argument('--resize',
                         help='Resize the image',
                         metavar='pixels',
                         type=int,
                         nargs=2)

        psh.add_argument(
            '--rotate',
            help='Rotate the image \
            (using degrees of rotation as input)',
            metavar='degrees',
            type=int
        )

        psh.add_argument(
            '--thumbs',
            help='Create thumbnails \
            (smaller than actual image size)',
            metavar='pixels',
            type=int,
            nargs=2
        )

        psh.add_argument(
            '--crop',
            help='Crop images',
            metavar='pixel',
            type=int,
            nargs=4
        )

        psh.add_argument(
            '--hist',
            help='Return the histogram of a greyscale convertion',
            action='store_true'
        )

        psh.add_argument(
            '--negative',
            help='Generate inverted (negative) images',
            action='store_true'
        )

        psh.add_argument(
            '--dominant_colors',
            help='Return the dominant colors',
            metavar='colors',
            type=int
        )

        psh.add_argument(
            '--dominant_colors_tuna',
            help='Return the dominant colors suited to TUNA corpus database',
            metavar='colors',
            type=int
        )

        fargs = psh.parse_args()

        return fargs