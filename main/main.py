from utils import files

f = files.fileutils()

def main():
    print f.filelist('/home/nelson/Desktop','.tgz')

if __name__ == '__main__':
    main()
