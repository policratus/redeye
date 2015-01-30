import argparse

class parser():
    def constructparser(self):
        psh = argparse.ArgumentParser()

        psh.add_argument('path',
                help='Path for image files')

        psh.add_argument('--colorspace',
                help='Perform operations on colorspace of images.',
                metavar='space')

        psh.add_argument('--resize',
                help='Resize the image',
                metavar='pixels',
                type=int,
                nargs=2)

        psh.add_argument('--rotate',
                help='Rotate the image (in degrees)',
                metavar='degrees',
                type=int)

        fargs = psh.parse_args()

        return fargs
