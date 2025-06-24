import pytest

def pytest_configure(config):
    config.option.htmlpath = 'report.html'
