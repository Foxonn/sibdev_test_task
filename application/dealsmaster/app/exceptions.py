class CustomBaseException(Exception):
    msg = "в процессе обработки файла произошла ошибка."
    message = None

    def __init__(self, message=None):
        if message:
            self.message = message

    def __str__(self):
        return "Error, Desc: %s - %s" % (self.message, self.msg)


class CsvFileTypeError(CustomBaseException):
    message = 'File don`t have data'


class CsvFileNeedKeys(CustomBaseException):
    pass
