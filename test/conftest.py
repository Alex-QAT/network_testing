from fixture.application import Application

import pytest
import json
import os.path
import importlib
import jsonpickle
import ftputil

#from fixture.db import DbFixture
#from fixture.orm import ORMFixture

fixture = None
target = None


def load_config(file):
    global target
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with (open(config_file) as f):
            target = json.load(f)
    return target


@pytest.fixture(scope="session")
def config(request):
    return load_config(request.config.getoption("--target"))


@pytest.fixture(scope="session", autouse=True)
def app(request, config):
    global fixture
    browser = request.config.getoption("--browser")
    if fixture is None or not fixture.is_valid():
        #fixture = Application(browser=browser, base_url=config["web"]['baseUrl'])
        # решили передавать не только base_url а весь конфиг, а там уж класс Application пусть сама забирает то что ему нужно
        fixture = Application(browser=browser, config=config)
    fixture.session.ensure_login(username=config["web_admin"]['username'], pswd=config["web_admin"]['password'])
    return fixture

# Фикстура конфигурации web-сервера
@pytest.fixture(scope="session", autouse=True)
def config_server(request, config):
    install_server_config(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])
    def fin():
        restore_server_config(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])
    request.addfinalizer(fin)

# Функция изменения конфигурации web-сервера (по ftp подложить нужный файл)
def install_server_config(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile('config_inc.php.bak'):
            remote.remove('config_inc.php.bak')
        if remote.path.isfile('config_inc.php'):
            remote.rename('config_inc.php','config_inc.php.bak')
        #remote.upload(os.path.join(os.path.dirname(__file__),'..','resources/config_inc.php'), 'config_inc.php')
        remote.upload(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'resources/config_inc.php'), 'config_inc.php')
def restore_server_config(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile('config_inc.php.bak'):
            if remote.path.isfile('config_inc.php'):
                remote.remove('config_inc.php')
            remote.rename('config_inc.php.bak', 'config_inc.php')


#@pytest.fixture(scope="session")
#def db(request):
#    db_cfg = load_config(request.config.getoption("--target"))["db"]
#    dbfixture = DbFixture(host=db_cfg['host'], db_name=db_cfg['db_name'], user=db_cfg['user'], password=db_cfg['password'])
#    def fin():
#        dbfixture.destroy()
#    request.addfinalizer(fin)
#    return dbfixture

#@pytest.fixture(scope="session")
#def orm(request):
#    orm_cfg = load_config(request.config.getoption("--target"))["db"]
#    ormfixture = ORMFixture(host=orm_cfg['host'], db_name=orm_cfg['db_name'], user=orm_cfg['user'], password=orm_cfg['password'])
#    # ORM сама завершает, эта фикстура финализации не требует

#    return ormfixture


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture

#@pytest.fixture
#def check_ui(request):
#    return request.config.getoption("--check_ui")

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--target", action="store", default="target.json")
#    parser.addoption("--check_ui", action="store_true")


def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        if fixture.startswith("data_"):
            testdata = load_from_module(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])
        elif fixture.startswith("json_"):
            testdata = load_from_json(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])

def load_from_module(module):
    return importlib.import_module("data.%s" % module).testdata

def load_from_json(file):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data/%s.json" % file)) as f_out:
        return jsonpickle.decode(f_out.read())