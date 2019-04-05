import sys
import os
from setuptools.command.install import install

project_name = "kdPythonAPIViewer"
class install_cmd(install):
    def run(self):
        install.run(self)
        try :
            if sys.platform =="win32" :
                    script_file =  os.path.join(self._get_desktop_folder(),project_name + '.bat')
                    with open(script_file, "w") as f:
                        f.write("@echo off\r\nstart " + project_name + ".exe")
            elif sys.platform == "linux":
                    import stat
                    script_file =  os.path.join(self._get_desktop_folder(),project_name + '.sh')
                    with open(script_file, "w") as f:
                        f.write("#!/bin/sh\n" + project_name)
                        st = os.stat(script_file)
                        os.chmod(script_file, st.st_mode | stat.S_IEXEC)
        except Exception as e:
            print("can not create start script." + str(e))
    def _get_desktop_folder(self):
        import subprocess
        try:
            return subprocess.check_output(['xdg-user-dir',
                                            'DESKTOP']).decode('utf-8').strip()
        except Exception:
            return os.path.join(os.path.expanduser('~'), 'Desktop')   
