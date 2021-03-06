import wx
import wx.adv

from win10toast import ToastNotifier

import json
import sys, os
import time
import datetime
import threading


CONFIG = 'config.json'
ICON = "icon/icon.ico"
TITLE = "提醒小助手"

class TimerThread(threading.Thread):
    def __init__(self, parent, configs):
        super(TimerThread, self).__init__()
        self.parent = parent
        self.setDaemon(True)
        self.configs = configs
        self.toaster = ToastNotifier()
        self.update_now = False

    def run(self):
        self.show_notify("小助手开始运行")
        self.build_timetable()
        sleep_t = 60
        while(True):
            cnt = 0
            while(cnt < sleep_t):
                if self.update_now:
                    self.build_timetable()
                    self.update_now = False
                    self.show_notify("配置文件已更新")
                time.sleep(1)
                cnt += 1
            if(datetime.datetime.now().hour == 0 and datetime.datetime.now().minute == 0):
                self.build_timetable()
            cur_time = datetime.datetime.now().hour * 60 + datetime.datetime.now().minute
            weekday = datetime.datetime.weekday(datetime.datetime.now()) + 1
            for t in self.timetable:
                if t[1] == cur_time and (t[0] == 0 or t[0] == weekday):
                    self.show_notify(t[2])
    
    def show_notify(self, msg):
        self.toaster.show_toast(TITLE,
                    msg,
                    icon_path=ICON,
                    duration=5)
        while self.toaster.notification_active(): time.sleep(0.1)

    def build_timetable(self, configs=None):
        if configs:
            self.configs = configs
        self.timetable = []
        cur_time = datetime.datetime.now().hour * 60 + datetime.datetime.now().minute

        for timer in self.configs['timer']:
            i = 0
            t = cur_time
            while(t < 24 * 60):
                while(i < len(timer)):
                    interval = int(timer[i])
                    msg = timer[i + 1]
                    t += interval
                    self.timetable.append([0, t, msg])
                    i += 2
                i = 0
            i = len(timer) - 1
            t = cur_time
            while(t > 0):
                while(i >= 0):
                    interval = int(timer[i - 1])
                    msg = timer[i]
                    self.timetable.append([0, t, msg])
                    t -= interval
                    i -= 2
                i = len(timer) - 1

        for plan in self.configs['plan']:
            self.timetable.append([plan[0], int(float(plan[1])*60), plan[2]])

        self.timetable.sort(key = lambda x : (x[1]))
        # with open('timetable.txt', 'w', encoding='utf8') as f:
        #     for t in self.timetable:
        #         line = "{} {}:{} {}\n".format( t[0], \
        #             int(t[1]/60), int(t[1]%60), t[2])
        #         f.write(line)


class MyTaskBarIcon(wx.adv.TaskBarIcon):
    ID_EXIT = wx.NewIdRef(count=1)
    ID_UPDATE = wx.NewIdRef(count=1)
    ID_TEST = wx.NewIdRef(count=1)

    def __init__(self):
        wx.adv.TaskBarIcon.__init__(self)
        self.SetIcon(wx.Icon(ICON), TITLE)
        self.Bind(wx.EVT_MENU, self.onExit, id=self.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.onUpdate, id=self.ID_UPDATE)
        # self.Bind(wx.EVT_MENU, self.test, id=self.ID_TEST)
        self.read_configs()
        self.timer = TimerThread(self, self.configs)
        self.timer.start()

    def onExit(self, event):
        wx.Exit()
        sys.exit()

    def onUpdate(self, event):
        self.read_configs()
        self.timer.configs = self.configs
        self.timer.update_now = True

    def CreatePopupMenu(self):
        menu = wx.Menu()
        for mentAttr in self.getMenuAttrs():
            menu.Append(mentAttr[1], mentAttr[0])
        return menu

    def getMenuAttrs(self):
        return [ \
                ('更新配置文件', self.ID_UPDATE), \
                ('退出', self.ID_EXIT) \
                ]

    def read_configs(self):
        with open(CONFIG, 'r', encoding='utf8') as f:
            self.configs = json.load(f)
        


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self)
        MyTaskBarIcon()


class MyApp(wx.App):
    def OnInit(self):
        MyFrame()
        return True

if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()