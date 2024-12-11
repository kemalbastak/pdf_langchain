class FileSizeException(ValueError):

    def __init__(self, message: str = "File size too large", name: str = "FileSizeException", status_code: int = 413):
        self.message = message
        self.name = name
        self.status_code = status_code
        super().__init__(self.message, self.name)