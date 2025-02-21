#!/usr/bin/python
import paramiko
from util.log import createLogger

logger = createLogger()
class SSHServer:
    def __init__(self, ip, usr, keyfile):
        self.key = paramiko.RSAKey.from_private_key_file(keyfile)
        self.host = paramiko.SSHClient()
        self.host.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #self.host.connect(hostname=ip,username=usr,password=pwd)
        self.host.connect(hostname=ip,username=usr,pkey=self.key)
        logger.info('Estalished a session')
    def __del__(self):
        """
        * Documentation: Close the session
        """
        self.host.close()
        logger.info('Connection Closed')

    def executeCmd(self, cmd):
        """
        * Documentation: Execute the command from the remote.
        param cmd: str: Command to be execute
        """
        logger.debug(f"Executing: {cmd}")
        _stdin, _stdout, _stderr = self.host.exec_command(cmd, get_pty=True)
        _stdout.flush()
        output = _stdout.read().decode()
        logger.debug(f"output: {output}")
        return output
