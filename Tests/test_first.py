#/usr/bin/python

import pytest
from testingmodules import TestingModule

obj = TestingModule()
#class Level
class Testing:
  @pytest.mark.xfail
  def test_helloworld(self):
    print("Hello World")

@pytest.mark.sanitytest
def test_1sanity():
  print(obj.gd_mrng())
#without markers
def test_sanity():
  print(obj.hello_world)
  print(obj.gd_mrng)

@pytest.mark.userfixtures('fixturetesting)
def test_fixturetest():
  print("fixture test")

