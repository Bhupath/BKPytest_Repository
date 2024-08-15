#/usr/bin/python

import pytest

@pytest.fixture
def fixturetesting():
  print("Am fixture")
