import pytest
from tests.fixtures import *
from servi.manifest import Manifest
import servi.config as c
from servi.config import deep_update
from servi.command import process_and_run_command_line as servi_run
import os
from servi.exceptions import ServiError
from jinja2 import Environment, DictLoader
from pprint import pprint

@pytest.fixture(scope="module", autouse=True)
def config_fixture():
    os.environ['SERVI_TEST'] = '12345'


def test_lookup_fn():
    # Test the jinja2 lookup function

    with pytest.raises(ServiError):
        assert c.lookup('file', 'whatever')

    assert c.lookup('env', 'SERVI_TEST') == '12345'
    assert c.lookup(' EnV ', 'SERVI_TEST') == '12345'

    assert c.lookup('env', 'SLDKJFLSLKLEJRL') is c.LOOKUP_FAILED_MESSAGE

    env = Environment(loader=DictLoader(
        {'test1': 'SERVITEST={{ lookup("env", "SERVI_TEST") }}',
         'test2': 'SERVITEST={{ lookup("env", "SLDKJFLSLKLEJRL") }}'
         }
    ))
    c.setup_jinja(env)

    t = env.get_template('test1')
    assert t.render() == 'SERVITEST=12345'

    t = env.get_template('test2')
    assert t.render() == 'SERVITEST='+c.LOOKUP_FAILED_MESSAGE


TEST_Servifile = """
---
HOST_NAME: 'servi_server'
# comment
SERVI_IGNORE_FILES:
  - "string1"
  - "string2"
MAIN_RSA_KEY_FILE: "{{ lookup('env', 'SERVI_TEST') }}"

"""

def test_process_config(setup_init):
    data = c.process_config(TEST_Servifile)

    print('loaded data: \n')
    pprint(data)
    assert data['HOST_NAME'] == 'servi_server'
    assert data['SERVI_IGNORE_FILES'] == ['string1', 'string2']
    assert data['MAIN_RSA_KEY_FILE'] == '12345'

    data = c.getconfig(c.SERVIFILE, c.TEMPLATE, c.MASTER, c.TMPL_DIR_SITE,
                       c.MASTER_DIR)
    print('Actual servifile:')
    pprint(data)
    assert c.load_user_config()


@pytest.mark.wip
def test_deep_update():
    assert deep_update({"a": {"a1": 1}} , {"a": {"a2": 2}}) == \
        {"a": {"a1": 1, "a2":2 }}

    assert deep_update({"a": {"a1": 1}}, {"b": {"b1": 1}}) == \
           {"a": {"a1": 1}, "b": {"b1": 1}}

    assert deep_update({}, {"b": {"b1": 1}}) == \
           {"b": {"b1": 1}}

    assert deep_update({"a": {"a1": 1}}, {}) == \
           {"a": {"a1": 1}}