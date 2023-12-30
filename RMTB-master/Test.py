import configparser

config = configparser.ConfigParser()
config.read("config.ini")

print(config['Settings']['path_tray_icon'])

config['Settings']['path_tray_icon'] = 'C:/FESTASHKA/img/icon.png/lgkdsjglksjglsdk'
with open('config.ini', 'w') as configfile:    # save
    config.write(configfile)