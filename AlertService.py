import win32serviceutil
import win32service
import win32event
import servicemanager
import win32ts
import win32profile
import win32process
import win32con

import socket
import requests
import time
import sys
from pathlib import Path


class ExampleService(win32serviceutil.ServiceFramework):
    _svc_name_ = "AlertService"
    _svc_display_name_ = "Alert Service"
    _svc_description_ = "Description"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def main(self):
        console_session_id = win32ts.WTSGetActiveConsoleSessionId()
        console_user_token = win32ts.WTSQueryUserToken(console_session_id)
        environment = win32profile.CreateEnvironmentBlock(console_user_token, False)
        startupInfo = win32process.STARTUPINFO()
        startupInfo.dwFlags = win32process.STARTF_USESHOWWINDOW
        startupInfo.wShowWindow = win32con.SW_NORMAL

        while True:
            win32process.CreateProcessAsUser(console_user_token,
                                             str(Path.home()) + "/AppData/Roaming/CorporationChat/alert/alert.exe",
                                             None, None, None, 0,  win32con.NORMAL_PRIORITY_CLASS,
                                             environment, None, startupInfo)
            requests.get("https://chat-b4ckend.herokuapp.com/service/")
            time.sleep(5)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(ExampleService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        # pyinstaller --hiddenimport win32timezone AlertService.py
        # sc queryex AlertService
        # taskkill / PID 1084 / F
        win32serviceutil.HandleCommandLine(ExampleService)
