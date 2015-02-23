import os


class fileutils():

    def filelist(self, extension, path=''):
        files = []

        try:
            if path == '':
                path = os.path.dirname(os.path.realpath(__file__))

            for filedir in os.listdir(path):
                if filedir.endswith(extension):
                    files.append(os.path.join(path, filedir))

            return files
        except OSError as e:
            print 'System error: {0}'.format(e)
