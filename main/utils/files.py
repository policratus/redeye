class fileutils():
    def filelist(self,path,extension):
        files = []
        try:
            for filedir in os.listdir(path):
                if filedir.endswith(extension):
                    files.append(os.path.join(path,filedir))
            return files
        except OSError, e:
            print 'System error: {0}'.format(e)
