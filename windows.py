import wx
import configparser
 
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
        self.config.read("config.ini")

        blacklist = self.config['Config']['black_list']
        self.config['Config']['black_list'] = f'{blacklist},{self.txt.GetValue()}'

        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)


    def RemoveBlackUser(self, event):
        self.config.read("config.ini")

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

        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)
            string = ''
        
# if __name__ == "__main__":
#     app = wx.App(False)
#     frame = BlackList().Show()
#     app.MainLoop()