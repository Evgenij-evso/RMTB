import wx.adv
import wx
import os
import configparser

config_path = 'C:/FESTASHKA/config.ini'
config = configparser.ConfigParser()
class BlackList(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Добавление в черный список")

        loc = wx.Icon(r'C:/FESTASHKA/img/icon.png', wx.BITMAP_TYPE_PNG)
        self.SetIcon(wx.Icon(loc))
        
        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetBackgroundColour("#edede9")

        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Добавляем панель так, чтобы она корректно отображалась на всех платформах. 
 
        self.txt = wx.TextCtrl(panel, value="",size=(150,25))
        self.txt.SetBackgroundColour("#d6ccc2")
        
        add = wx.Button(panel, wx.ID_ANY, "Add",size=(45,27))
        remove = wx.Button(panel, wx.ID_ANY, "Remove",size=(65,27))
        add.Bind(wx.EVT_BUTTON,self.AddBlackList)
        remove.Bind(wx.EVT_BUTTON,self.RemoveBlackUser)

        h_sizer.Add(self.txt, 0, wx.CENTER)
        h_sizer.Add(remove,0,wx.CENTER)
        h_sizer.Add(add, 0, wx.CENTER)
 
        main_sizer.Add((0,0), 1, wx.EXPAND)
        main_sizer.Add(h_sizer, 0, wx.CENTER)
        main_sizer.Add((0,0), 1, wx.EXPAND)
 
        panel.SetSizer(main_sizer)

        self.config = configparser.ConfigParser()
 
    def AddBlackList(self, event):
        self.config.read(config_path)

        blacklist = self.config['Config']['black_list']
        self.config['Config']['black_list'] = f'{blacklist},{self.txt.GetValue()}'

        with open(config_path, 'w') as configfile:
            self.config.write(configfile)


    def RemoveBlackUser(self, event):
        self.config.read(config_path)

        remote_text = self.config['Config']['black_list']
        remote_list = remote_text.split(',')

        string = ''
        for i_pop in range(len(remote_list)):
            if remote_list[i_pop] == self.txt.GetValue():
                pass
            else:
                if i_pop == 0:
                    string += str(remote_list[i_pop])
                else:
                    string += ',' + str(remote_list[i_pop])

        self.config['Config']['black_list'] = string

        with open(config_path, 'w') as configfile:
            self.config.write(configfile)
            string = ''



config.read(config_path)

TRAY_TOOLTIP = config['Settings']['tray_name']
TRAY_ICON = config['Settings']['path_tray_icon']
PROCESS_NAME = config['Settings']['process_name']
PATH_TELEGRAM_BOT = config['Settings']['path_telegram_bot']

os.system('start ' + PATH_TELEGRAM_BOT)


def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item


class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Black list add', self.black_list)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def set_icon(self, path):
        icon = wx.Icon(path)
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_left_down(self, event):
        print ('Tray icon was left-clicked.')
    
    def black_list(self, event):
        BlackList().Show()

    def on_exit(self, event):
        os.system(f'taskkill /f /im {PROCESS_NAME}')
        wx.CallAfter(self.Destroy)
        self.frame.Close()

class App(wx.App):
    def OnInit(self):
        frame=wx.Frame(None)
        self.SetTopWindow(frame)
        TaskBarIcon(frame)
        return True

def main():
    app = App(False)
    app.MainLoop()


if __name__ == '__main__':
    main()