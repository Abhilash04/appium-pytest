"""
This module contains different pytest marks
"""

import pytest
from funcy import compose

welcome = compose(pytest.mark.welcome)
login = compose(pytest.mark.login)
registration = compose(pytest.mark.registration)
sanity = compose(pytest.mark.sanity)
regression = compose(pytest.mark.regression)
