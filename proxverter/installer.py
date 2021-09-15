import subprocess
import os
import platform

class Installer:

    def __init__(self, output=os.devnull):
        self.chocoline = 'powershell.exe "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString(\'https://community.chocolatey.org/install.ps1\'))'
        self.chocolime = 'powershell.exe "choco install {} -y"'
        self.platform  = platform.system().lower()
        if self.platform == "windows":
            self.startupinfo = subprocess.STARTUPINFO()
            self.startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        self.output    = output

    def activate(self):
        fl = open(self.output, 'w')
        if hasattr(self, 'startupinfo'):
            cmline = subprocess.Popen(
                self.chocoline,
                shell=True,
                stdin=subprocess.PIPE,
                stdout=fl,
                stderr=fl,
                startupinfo=self.startupinfo
            )
        else:
            cmline = subprocess.Popen(
                self.chocoline,
                shell=True,
                stdin=subprocess.PIPE,
                stdout=fl,
                stderr=fl
            )
        cmline.communicate()
        fl.close()

        if cmline.returncode:
            raise ImportError(f"Unable to install choco installer. Return code: {cmline}")

        return cmline.returncode == 0

    def install(self, pkg):
        fl = open(self.output, 'a')
        cmline = subprocess.Popen(
            self.chocolime.format(pkg),
            shell=True,
            stdin=subprocess.PIPE,
            stdout=fl,
            stderr=fl,
            startupinfo=self.startupinfo
        )
        cmline.communicate()
        fl.close()

        if cmline.returncode:
            raise ImportError(f"Unable to install {pkg}. Return code: {cmline}")

        return cmline.returncode == 0
