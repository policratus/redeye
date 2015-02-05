from utils import files
from basic import spatial
from shellparser import parser

def main():
    f = files.fileutils()
    s = spatial.spatial()
    p = parser.parser()

    args = p.constructparser()

    try:
        filelist = f.filelist('.jpg',args.path)

        for ofile in filelist:
            if args.colorspace:
                s.colorspace(ofile,args.colorspace,size=2)
            elif args.resize:
                s.resize(ofile,args.resize[0],args.resize[1])
            elif args.rotate:
                s.rotation(ofile,args.rotate)
            elif args.thumbs:
                s.thumbs(ofile,args.thumbs[0],args.thumbs[1])
            elif args.crop:
                s.crop(
                        ofile,args.crop[0],args.crop[1],
                        args.crop[2],args.crop[3]
                        )
            elif args.hist:
                s.histogram(ofile)

    except Exception, e:
        print '[MAIN]: {0}'.format(e)

if __name__ == '__main__':
    main()
