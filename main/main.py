from utils import files
from basic import spatial,io

def main():
    f = files.fileutils()
    s = spatial.spatial()
    i = io.io()

    try:
        filelist = f.filelist('.jpg','/hdd/redeye-pics')

        for ofile in filelist:
            resized = s.resize(ofile,640,480)
            i.show(resized)
            converted = s.colorspace(ofile,'greyscale')
            i.show(converted)
            rotated = s.rotation(ofile,45)
            i.show(rotated)
    except Exception, e:
        print '[ERROR]: {0}'.format(e)

if __name__ == '__main__':
    main()
