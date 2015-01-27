from utils import files
from basic import spatial

def main():
    f = files.fileutils()
    s = spatial.spatial()

    try:
        filelist = f.filelist('.jpg','/hdd/redeye-pics')

        for ofile in filelist:
            s.colorspace(ofile,'color',size=2)

    except Exception, e:
        print '[MAIN]: {0}'.format(e)

if __name__ == '__main__':
    main()
