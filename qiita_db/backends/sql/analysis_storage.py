#!/usr/bin/env python

__author__ = ""
__copyright__ = "Copyright 2013, The Qiita Project"
__credits__ = [""]
__license__ = "BSD"
__version__ = "0.1.0-dev"
__maintainer__ = ""
__email__ = ""
__status__ = "Development"

from qiita_db.backends.sql.base_sql import BaseSQLStorageAPI


class AnalysisStorage(BaseSQLStorageAPI):
    """"""

    def __init__(self):
        """"""
        super(AnalysisStorage, self).__init__()
        