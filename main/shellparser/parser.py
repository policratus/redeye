import argparse


class parser():

    def constructparser(self):
        psh = argparse.ArgumentParser()

        psh.add_argument('path',
                         help='Path for image files')

        psh.add_argument('--colorspace',
                         help='Perform operations on color space of images',
                         choices=['greyscale', 'color'],
                         metavar='space')

        psh.add_argument('--resize',
                         help='Resize the image',
                         metavar='pixels',
                         type=int,
                         nargs=2)

        psh.add_argument('--rotate',
                         help='Rotate the image (using degrees of rotation as input)',
                         metavar='degrees',
                         type=int)

        psh.add_argument('--thumbs',
                         help='Create thumbnails (smaller than actual image size)',
                         metavar='pixels',
                         type=int,
                         nargs=2)

        psh.add_argument('--crop',
                         help='Crop images',
                         metavar='pixel',
                         type=int,
                         nargs=4)

        psh.add_argument('--hist',
                         help='Return the histogram of a greyscale convertion',
                         action='store_true')

        fargs = psh.parse_args()

        return fargs
