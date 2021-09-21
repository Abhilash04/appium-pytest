import pytest

from SupportLibraries.driver_factory import DriverFactory


@pytest.fixture(scope="session")
def driver(request, platform):
    print("session_level_setup: Running session level setup.")
    df = DriverFactory(platform)
    driver = df.get_driver_instance()
    driver.reset()
    session = request.node
    for item in session.items:
        cls = item.getparent(pytest.Class)
        setattr(cls.obj, "driver", driver)
    driver._platform = platform
    yield
    print("session_level_setup: Running session level teardown.")
    driver.quit()


@pytest.fixture(scope="session")
def platform(request):
    plat = request.config.getoption("--platform").lower()
    if plat not in ['ios', 'android', 'bs_android', 'bs_ios']:
        raise ValueError("platform value must be in ['ios', 'android', 'bs_android', 'bs_ios']")
    return plat


def pytest_addoption(parser):
    parser.addoption("--platform", action='store', default='browser_stack')
