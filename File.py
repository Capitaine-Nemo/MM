__author__ = 'lantos'

import hashlib
import os
import string


class File:
    """ File class"""

    def __init__(self, fileName, path, is_folder_a=True):
        # print "creation de l'object File"
        # print "fileName= \t", fileName
        # print "path= \t", path
        """

        :type is_folder_a: bool
        """
        if os.path.exists(path + '/' + fileName):
            self.fileName = fileName
            self.fileExtension = string.strip(os.path.splitext(fileName)[1], '.')
            assert isinstance(path, str)
            if is_folder_a:
                self.path_a = set([path])
                self.path_b = set([])
            else:
                self.path_a = set([])
                self.path_b = set([path])
            self.md5Sum = hashlib.md5(open(path + '/' + fileName, 'r').read()).hexdigest()
            # print "\nCreation de l'object File"
            #   print "fileName= \t", self.fileName
            #   print "path= \t", self.path
            #   print "fileExtension= \t", self.fileExtension
            #   print "md5Sum= \t", self.md5Sum
        else:
            file = []
            for root, dirs, files in os.walk(path, followlinks=True):
                for i in files:
                    file.append(os.path.join(root, i))
            for i in file:
                print i
            raise Exception

    @property
    def fileName(self):
        return self.__fileName

    @property
    def path_a(self):
        return self.__path_a

    @property
    def path_b(self):
        return self.__path_b

    @property
    def fileExtension(self):
        return self.__fileExtension

    @property
    def md5Sum(self):
        return self.__md5Sum

    @property
    def depth(self):
        return self.__depth

    def __eq__(self, other):
        if self.fileName == other.fileName:
            if self.md5Sum == other.md5Sum:
                return True
        return False

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash(self.fileName) * len(self.path_a)

    def computeDepth(self, root):
        self.root = root
        # print "root=\t", root
        # print "file path=\t", self.path

        pathRoot = string.split(root, '/')
        depth = 0
        for path_a in self.path_a:
            pathFile = string.split(path_a, '/')
            index = 0
            for i in pathRoot:
                if not (i == pathFile[index]):
                    raise Exception("Error File is not in path:\t ", root)
                else:
                    pathFile.remove(i)
                    # print "pathFile=\t", pathFile
            depth = max(depth, len(pathFile))
        self.depth = depth
        return self.depth

    def add_path(self, file, is_folder_a=True):
        if self == file:
            if is_folder_a:
                self.path_a |= file.path_a
                self.path_b |= file.path_b
            else:
                self.path_a |= file.path_b
                self.path_b |= file.path_a
