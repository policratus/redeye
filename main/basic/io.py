from PIL import Image

class io():
    def open(self,filepath):
        return Image.open(filepath)

    def save(self,image,filepath):
        try:
            image.save(filepath)
        except Exception, e:
            print 'Erro saving file: {0}'.format(e)

    def show(self,image):
        image.show()
