import pytest
from tests.fixtures import *
from servi.manifest import Manifest
import servi.config as c


@pytest.mark.wip
def test_manifest_equal(setup_init):
    m0 = Manifest(c.TEMPLATE)
    m1 = Manifest(c.TEMPLATE)
    assert m0 == m1

def test_qprint(setup_empty):
    assert servi_run('init -q .')