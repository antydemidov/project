__version__ = '2023.01.09'
__author__ = 'Anton Demidov | @antydemidov'


class CommonResult:
    """Common result holder"""
    def __init__(self,
                 status: str = '',
                 status_bool: bool = None,
                 details: dict = {},
                 **kwargs):
        self.status = status
        self.status_bool = status_bool
        self.details = details
        for key, value in kwargs.items():
            setattr(self, key, value)


class UpdaterResult:
    """
    Updating result object

    Parameters
    ----------
    - current_version : `int`
        ID of the last version of db
    - updated_versions : `list`
        history of updating
    - file_size : `int`
        sum of sizes of each version
    - status : `str`
        string of status
    """
    def __init__(self,
                 current_version: int = 0,
                 updated_versions: list = [],
                 file_size: int = 0,
                 status: str = ''):
        self.current_version = current_version
        self.updated_versions = updated_versions
        self.file_size = file_size
        self.status = status
