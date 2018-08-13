#!/usr/bin/python3
import os,pip,importlib,site

def clr():
    os.system('clear')

def install(package, imp = None, no_import = False):
    pip.main(['install', package])
    if not no_import:
        importlib.reload(site)
        globals()[imp or package] = importlib.import_module(imp or package)

clr()
print("""
rPi-Project-Controller Installer
--------------------------------------
Duinotech
--------------------------------------
Author D.k.West

This script will prompt you with options
and the capital letter is the default 
when you press enter.

Press Enter to continue
""")
input()
clr()
print('='*20)
print('WARNING')
print('='*20)
print('''
this script will make changes to your
device, and presumes that this is a fresh install

If something goes wrong, you _might_ have to re-image
your SD card.

''')
if str(input('ok to continue? [Y/n]')).lower() == 'n':
    exit()

clr()
print('testing internet connection....')
if os.system('ping -c 1 github.com'):
    print('unable to connect to github')
    print('you need an internet connection for this to work')
    exit()

clr()
print("""
Installing dependencies..
""")

install('flask')
try:
    install('gitpython','git') 
    from git import Repo, exc
except ImportError as e:
    print('installed the dependencies but failed to import.')
    print('please run this script again')
    exit()

try:
    Repo.clone_from('http://github.com/duinotech/rPi-Project-Controller',
        '/home/pi/rPi-Project-Controller')
except exc.GitCommandError as e:
    pass

os.chdir('/home/pi/rPi-Project-Controller')
os.system('pip3 install -e .')

clr()
print('setting up webserver to autoboot..')
os.system('echo "@./rPi-Project-Controller/start_neuron.sh" >> ~/.config/lxsession/LXDE-pi/autostart')

clr()
print('-='*10)
print('LCD screen set-up')
print('-='*10)
print('''
    Are you planning on using the 5" touch screen (XC9024)

    and if so, are you going to use it in (P)ortriat or (L)andscape mode?
    
    ( use n for 'no screen': either webserver or self-provided screen mode)
''')
screen = None
while screen not in ['p','l','n']:
    print('please use from the options p, l or n,')
    screen = input('screen? [P/l/n]') or 'p'
    screen = screen.lower()

if screen == 'p' or screen == 'l':
    try:
        Repo.clone_from('http://github.com/goodtft/LCD-show','/home/pi/LCD-show')
    except exc.GitCommandError as e:
        #assumed already have it
        print('failed to get LCD-show from goodtft but I\'ll assume you already have it')
        pass

    try:
        os.chdir('/home/pi/LCD-show')
    except Exception as e:
        print('you don\'t have it, this is bad')
        print('cancelling build, check out this script and install manually')
        print(e)
        exit()
    for line in """
    sudo rm -rf /etc/X11/xorg.conf.d/40-libinput.conf
    sudo cp -rf ./boot/config-5.txt /boot/config.txt
    sudo cp ./usr/inittab /etc/
    sudo cp -rf ./usr/99-fbturbo.conf-HDMI /usr/share/X11/xorg.conf.d/99-fbturbo.conf 
    sudo mkdir /etc/X11/xorg.conf.d/
    sudo cp -rf ./usr/99-calibration.conf-5 /etc/X11/xorg.conf.d/99-calibration.conf 
    sudo dpkg -i -B xserver-xorg-input-evdev_2.10.5-1_armhf.deb
    sudo cp -rf /usr/share/X11/xorg.conf.d/10-evdev.conf /usr/share/X11/xorg.conf.d/45-evdev.conf
    """.split('\n'):
        os.system(line)
    
    if screen == 'p':
        os.system('sudo su -c "echo \"display_rotate=1\" >> /boot/config.txt"')
        os.system('sudo sed -i "4s/.*/Option \\"Calibration\\" \\"208 3905 3910 288\\" /" /etc/X11/xorg.conf.d/99-calibration.conf')
        os.system('sudo sed -i "5s/.*/Option \\"SwapAxes\\" \\"1\\" /" /etc/X11/xorg.conf.d/99-calibration.conf')



clr()
print('-='*15)
print('          All Done!      ')
print('-='*15)
print('the system will now reboot')
for i in range(5):
    print('{}.. '.format(i),end='',flush=True)

print('REBOOT')
os.system('reboot')
