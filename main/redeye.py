import argparse
from utils import files
from basic import spatial,io

def main():
    f = files.fileutils()
    s = spatial.spatial()
    i = io.io()

    parser = argparse.ArgumentParser(description='Redeye - Computer Vision tools made easy')
    parser.add_argument('path',help='the path where the images reside')
    parser.add_argument('extension',help='the extension of input image files')
    parser.add_argument('--resize',dest='resize',metavar='pixels',type=int,action='store',nargs=2,help='resize the image')

    args = parser.parse_args()

    filelist = f.filelist(args.extension,args.path)

    for ofile in filelist:
        resized = s.resize(ofile,args.resize[0],args.resize[1])
        i.show(resized)
        #converted = s.colorspace(ofile,'greyscale')
        #i.show(converted)
        #rotated = s.rotation(ofile,45)
        #i.show(rotated)

if __name__ == '__main__':
    main()
