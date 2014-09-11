from test.fixtures import *
import pytest
from commands.utils.semantic import *


def test_semantic_version():
    assert SemanticVersion('1.1') > SemanticVersion('1.0')
    assert SemanticVersion('1.0.0') == SemanticVersion('1.0')
    assert SemanticVersion('1.0.1') < SemanticVersion('1.0.2')
    assert SemanticVersion('1').bump_ver(MAJOR) == SemanticVersion('2.0.0')
    assert SemanticVersion('1').bump_ver(MINOR) == SemanticVersion('1.1.0')
    assert SemanticVersion('1').bump_ver(PATCH) == SemanticVersion('1.0.1')
    assert str(SemanticVersion('3.3.14')) == '3.3.14'
    assert SemanticVersion('1.0.14') > SemanticVersion('1.0.2')
    with pytest.raises(ValueError):
        SemanticVersion('1.2.3.4')
    with pytest.raises(ValueError):
        SemanticVersion('hello')
    with pytest.raises(ValueError):
        SemanticVersion(10)

