
from File import *


class Folder:
    """ Folder class"""

    def __init__(self, folderName, path):
        if os.path.isdir(path + '/' + folderName):
            self.folderName = folderName
            self.path = path
            self.realPath = path + '/' + folderName

            # self.folderSize = 0

            self.listOfRealFile = []
            for iFile in os.listdir(path + '/' + folderName):
                if os.path.isfile(path + '/' + folderName + '/' + iFile):
                    if not iFile.startswith('.'):
                        # print iFile
                        self.listOfRealFile.append(iFile)
            self.listOfIdenticalFile = set([])
            self.listOfIdenticalFolder = set([])
            self.isIdentical = False
            self.copyPath = set([])
            # print "\nCreation de l'object Folder"
            # print "folderName= \t", self.folderName
        else:
            raise Exception("Folder\t" + folderName + " not found there\t" + path)

    #
    def add_identical_file(self, file):
        """Try to add an file that is assumed to be identical. Check if the file really exists, before adding it and return true.
        Otherwise it return False.
        :param file: of File type
        :return: True if the given file really exists.
        """
        if self.is_file_contained_in_real_path(file):
            # print self.listOfIdenticalFile
            if file not in self.listOfIdenticalFile:
                if file.path_b:
                    if self.copyPath:
                        intersection_of_path = self.copyPath.intersection(file.path_b)
                        # print "intersection_of_path=\t", intersection_of_path
                        if intersection_of_path:
                            self.listOfIdenticalFile.add(file)
                            self.copyPath = intersection_of_path
                        else:
                            return False
                    else:
                        self.copyPath = file.path_b
                        self.listOfIdenticalFile.add(file)
                else:
                    self.listOfIdenticalFile.add(file)
                return True
        return False

    def add_identical_folder(self, folder):

        if self.is_folder_contained_in_real_path(folder):
            if folder not in self.listOfIdenticalFolder:
                # treatment of copyPath for the parent folder
                # We assume that we already check that the path_b tree is identical:
                # i.e. that the "mirror" folder has a father folder and that
                if self.copyPath:
                    set_copy = folder.copyPath
                    new_set = set([])
                    for p in set_copy:
                        list = string.split(p, '/')
                        list.pop(-1)
                        name = string.join(list, '/')
                        new_set.add(name)

                    intersection_of_path = self.copyPath.intersection(new_set)
                    # print "intersection_of_path=\t", intersection_of_path
                    if intersection_of_path:
                        self.listOfIdenticalFolder.add(folder)
                        if folder.realPath in intersection_of_path:
                            intersection_of_path.remove(folder.realPath)
                            intersection_of_path.add(self.realPath)
                        self.copyPath = intersection_of_path
                    else:
                        return False
                elif folder.copyPath:
                    set_copy = folder.copyPath
                    new_set = set([])
                    for p in set_copy:
                        list = string.split(p, '/')
                        list.pop(-1)
                        name = string.join(list, '/')
                        new_set.add(name)
                    self.copyPath = new_set
                    self.listOfIdenticalFolder.add(folder)
                else:
                    self.copyPath = folder.copyPath
                    self.listOfIdenticalFolder.add(folder)
                # end of treatment of copyPath for the parent folder
                return True
        return False

    def is_file_contained_in_real_path(self, f):
        if self.realPath in f.path_a:
            return f.fileName in self.listOfRealFile
        elif self.realPath in f.path_b:
            return f.fileName in self.listOfRealFile
        return False

    def is_folder_contained_in_real_path(self, folder):
        if self.realPath in folder.path:
            return os.path.isdir(folder.path + '/' + folder.folderName)
        return False

        # a tester

    def __eq__(self, other):
        if self.folderName == other.folderName:
            if self.path == other.path:
                return True
        return False

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash(self.folderName) * len(self.path)

        # path1Original = listOfIdenticalFileName[1][1][0]
        # path2Original = listOfIdenticalFileName[1][1][1]
        # print "path1=\t", path1Original
        # tmpSplittedPath1 = path1Original.split('/')
        # print "tmpSplittedPath1=\t", tmpSplittedPath1
        # print os.listdir(path1Original)
        # numberOfFiles1 =  len(os.listdir(path1Original))
        # print numberOfFiles1
        # numberOfFiles2 =  len(os.listdir(path2Original))
        # print numberOfFiles2
        #
        # tmpSplittedPath2 = path2Original.split('/')
        # nameOfFolder1 = tmpSplittedPath1[-1]
        # nameOfFolder2 = tmpSplittedPath2[-1]
        # isFolderDifferent =True
        # if nameOfFolder1== nameOfFolder2 :
        # if numberOfFiles1 == numberOfFiles2 :
        # for iF in os.listdir(path1Original): #Pour tous les fichiers qui existent vraiment dans le dossier
        # if iF not in listOfNamesOfIdenticalFiles: #je regarde s'il est dans la liste des fichiers identiques
        # isFolderDifferent = False
        # else :
        #                 index = listOfIdenticalFileName.index(iF)
        #                 if listOfIdenticalFileName[index][1][0]!=path1Original:
        #                    isFolderDifferent = False
