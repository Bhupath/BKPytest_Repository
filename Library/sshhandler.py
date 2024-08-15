#/usr/bin/python

import shutil
import subprocess
import paramiko

class ExecuteSSHCommands:

  def __init__(self):
    pass

  @staticmethod
  def execute_command(cmd: str) -> str:
    """
    * Documentation:
    param cmd: str
    return output.stdout: str
    """
    output = None
    try:
      output = subprocess.run(cmd, shell=True, text=True, capture_output=True)
      assert output.return_code == 0, "Command Execution is Failed"
    except AssertionError as err:
      print(f"Exception was occured due to {err}")
      return output
    return output.stdout
  @staticmethod
  def exeucte_remote_command (cmd: str, remote_ip: str, username: str, password: str) -> str:
    output = None
    #paramiko object to implement

