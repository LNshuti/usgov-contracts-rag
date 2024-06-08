import sys
import os
import pytest

@pytest.fixture(autouse=True)
def set_up_paths():
    root_dir = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, root_dir)
