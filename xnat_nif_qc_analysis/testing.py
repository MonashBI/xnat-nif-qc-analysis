import os.path
from nianalysis.testing import BaseTestCase as NiAnalysisBaseTestCase
import xnat_nif_qc_analysis


class BaseTestCase(NiAnalysisBaseTestCase):

    XNAT_TEST_PROJECT = 'TEST012'
    BASE_TEST_DIR = os.path.abspath(os.path.join(
        os.path.dirname(xnat_nif_qc_analysis.__file__), '..', 'test'))
