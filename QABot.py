#/usr/bin/python

from __future__ import annotations

import argparse
import os
import sys
import subprocess
import yaml

output = subprocess.getoutput("python --version").split(" ")[1]
py_version = output.split(" ")

if int(py_version[0])>=3 and int(py_version[1])>=7:
  print(f"Python Version: {output}")

else:
  print("Kindly install the python version above 3.7")
  sys.exit(1)

class QABot:

  MTCIL_ENV = "mtcil_env"

  @classmethod
  def install_python_modules(cls):
    """
    * Documentation:
    """
    os.system("pip install -r requirements.txt")

  @classmethod
  def setup_virtual_env(cls):
    """
    * Documentation:
    """
    try:
      print("Setting up the vent for python project")
      output = subprocess.getoutput("which python3")
      os.system(f"{output} -m venv {cls.MTCIL_ENV}")
      print(f"Please Execute: source {cls.MTCIL_ENV}/bin/activate\n Then Proceed to install python modules")
    except Exception as err:
      print(f"Exception was occured with: {err}")

  @classmethod
  def main(cls, method: str, command: str = None):
    """
    * Documentation:
    param method: str
    param command: str
    """
    print("="*10+"Welcome to BK Automaton Framework "+"="*10)
    print("****")
    print("*   *")
    print("*     *")
    print("*     *")
    print("*   *")
    print("*")
    print("*")
    if method == "install modules":
      cls.install_python_modules()
    elif method == "enable venv":
      cls.setup_virtual_env()
    if command:
      pass

if __name__=="__main__":
  obj = QABot()
  parset = argparse.ArgumentParser(description="Console APplication for \n1. Install 3rd part modules",
                                  usage="Use argument approaches and for better understanding use helper")
  subparser = parser.add_subparsers(dest="method", description="Only one position argument is allowed")
  subparser.add_parser("install modules")
  subparser.add_parser("setup virtual env")
  parser.add_argument("-c","--command", help="Parse the pytest command to execute")
  args = parser.parse_args()
  obj.main(args)
