#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, The Qiita Project"
__credits__ = ["Jose Antonio Navas Molina", "Joshua Shorenstein"]
__license__ = "BSD"
__version__ = "0.1.0-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.edu"
__status__ = "Development"

from .backends.sql import (SQLUser, SQLAnalysis, SQLStudy, SQLSample, SQLJob,
                           SQLMetadataMap)
from .backends.fs import FSUser, FSAnalysis, FSStudy, FSSample, FSJob
from qiita_db.config import qiita_db_config


if qiita_db_config.backend == "SQL":
    UserStorage = SQLUser
    AnalysisStorage = SQLAnalysis
    StudyStorage = SQLStudy
    SampleStorage = SQLSample
    JobStorage = SQLJob
    MetadataMapStorage = SQLMetadataMap
elif qiita_db_config.backend == "FS":
    UserStorage = FSUser
    AnalysisStorage = FSAnalysis
    StudyStorage = FSStudy
    SampleStorage = FSSample
    JobStorage = FSJob
else:
    raise ValueError("Backend not recognized: %s" % qiita_db_config.backend)
