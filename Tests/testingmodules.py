#/usr/bin/python

import pytest

class TestingModule:
  def hello_world(self):
    return "Hello World mawa"
  def gd_mrng(self):
    return "Gd Mrng ra mawa"
  @Pytest.fixture
  def fixturetesting(self):
    return "Hello Fixture"
