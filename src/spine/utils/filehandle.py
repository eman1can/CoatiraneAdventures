import os


class FileType:
    Absolute = 0


class FileHandle:

    def __init__(self, *args):

        self.file = None
        self.fileType = None

        if isinstance(args[0], str):
            if os.path.isdir(args[0]):
                self.file = args[0]
            else:
                self.file = open(args[0], 'r')
        else:
            self.file = args[0]
        if len(args) != 1:
            self.type = args[1]
        else:
            self.type = FileType.Absolute

    def full_path(self):
        if isinstance(self.file, str):
            return self.file
        else:
            return self.file.name

    def path(self):
        if isinstance(self.file, str):
            return os.path.dirname(self.file)
        return os.path.dirname(self.file.name)

    def name(self):
        if isinstance(self.file, str):
            return os.path.basename(self.file)
        return os.path.basename(self.file.name)

    def extension(self):
        if isinstance(self.file, str):
            name = os.path.basename(self.file)
        else:
            name = os.path.basename(self.file.name)
        try:
            dotIndex = name.rindex('.')
        except ValueError:
            return ""
        return name[:dotIndex+1]

    def nameWithoutExtension(self):
        if isinstance(self.file, str):
            return os.path.splitext(os.path.basename(self.file))[0]
        return os.path.splitext(os.path.basename(self.file.name))[0]

    def pathWithoutExtension(self):
        if isinstance(self.file, str):
            path = self.file
        else:
            path = self.file.name
        try:
            dotIndex = path.rindex('.')
        except ValueError:
            return ""
        return path[:dotIndex]

    def type(self):
        return self.type

    def child(self, name):
        if isinstance(self.file, str):
            return FileHandle(f"{self.full_path()}/{name.strip()}", self.type)
        if os.path.splitext(self.file.name)[0] == 0:
            return FileHandle(name, self.type)
        return FileHandle(f"{self.path()}/{name.strip()}", self.type)

    def parent(self):
        return FileHandle(os.path.dirname(self.file.name), self.type)