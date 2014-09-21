from tests.fixtures import *
import pytest
from commands.utils.utils import *

@pytest.mark.wip
def test_find_up():
    assert find_up('/serviplate/servi/servi/commands', 'servi') == \
        '/serviplate/servi/servi'
    assert find_up('/serviplate/servi/servi', 'servi') == \
        '/serviplate/servi/servi'
    assert find_up('/serviplate/servi', 'servi') == '/serviplate/servi'
    assert find_up('/serviplate', 'servi') is None
    assert find_up('/', 'servi') is None