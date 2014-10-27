from servi.manifest import Manifest
import servi.config as c
from tests.fixtures import *


def test_manifest_equal(setup_init):
    m0 = Manifest(c.TEMPLATE)
    m1 = Manifest(c.TEMPLATE)
    assert m0 == m1
