import configparser

import paramiko


class SSHClient(object):
    def __init__(self, config_sec, config_str='config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_str, encoding='utf-8')
        self.config_sec = config_sec
        self.client = None
        self._connect()

    def __del__(self):
        self.client.close()

    def _connect(self):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(hostname=self.config.get(self.config_sec, 'host'),
                                port=self.config.getint(self.config_sec, 'port'),
                                username=self.config.get(self.config_sec, 'username'),
                                password=self.config.get(self.config_sec, 'password'),
                                timeout=self.config.getfloat(self.config_sec, 'timeout'))
        except Exception as e:
            print("ssh connect %s: " % (self.config.get(self.config_sec, 'host')), e)
            try:
                self.client.close()
            except:
                pass

    def run_cmd(self, command):
        stdin, stdout, stderr = self.client.exec_command(command)
        stdout = stdout.read().decode("utf-8")
        stderr = stderr.read().decode("utf-8")
        return stdout, stderr


def main():
    cmd = "pwd"
    client = SSHClient('ssh1')
    stdout, stderr = client.run_cmd(cmd)
    print(stdout, stderr)


if __name__ == '__main__':
    main()
