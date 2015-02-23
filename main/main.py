from utils import files
from basic import spatial, io
from shellparser import parser


def main():
    f = files.fileutils()
    s = spatial.spatial()
    p = parser.parser()
    i = io.io()

    args = p.constructparser()

    try:
        filelist = f.filelist('.jpg', args.path)

        if filelist:
            for ofile in filelist:
                image = i.open(ofile)

                if args.colorspace:
                    i.save(s.colorspace(image, args.colorspace, size=2), ofile)
                elif args.resize:
                    i.save(
                        s.resize(image, args.resize[0], args.resize[1]), ofile)
                elif args.rotate:
                    i.save(s.rotation(image, args.rotate), ofile)
                elif args.thumbs:
                    i.save(
                        s.thumbs(image, args.thumbs[0], args.thumbs[1]), ofile)
                elif args.crop:
                    i.show(s.crop(image, args.crop[0], args.crop[1],
                                  args.crop[2], args.crop[3]
                                  ))
                elif args.hist:
<< << << < HEAD
                    s.histogram(image, ofile)
== == == =
                    s.histogram(image, ofile)
                elif args.negative:
                    i.save(s.negative(image),ofile)
>>>>>>> 6a8c3c1a9eb99ce2cd9cda1d790f4f658f06ad4b

    except Exception as e:
        print '[MAIN]: {0}'.format(e)

if __name__ == '__main__':
    main()
