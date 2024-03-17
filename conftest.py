import pytest
from src.settings import results

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "integration"
    )


@pytest.fixture
def clear_results():
    results.clear()