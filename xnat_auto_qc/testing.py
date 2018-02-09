import os.path
from nianalysis.testing import BaseTestCase as NiAnalysisBaseTestCase
import xnat_auto_qc


class BaseTestCase(NiAnalysisBaseTestCase):

    XNAT_TEST_PROJECT = 'TEST012'
    BASE_TEST_DIR = os.path.abspath(os.path.join(
        os.path.dirname(xnat_auto_qc.__file__), '..', 'test'))
