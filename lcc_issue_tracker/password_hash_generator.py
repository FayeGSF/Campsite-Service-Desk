from collections import namedtuple
from flask import Flask
from flask_bcrypt import Bcrypt


UserAccount= namedtuple('UserAccount',['username','password'])
app = Flask(__name__)
flask_bcrypt = Bcrypt(app)

users =[UserAccount('JamesSmith', 'Pass123!'),
UserAccount('maryjohnson001',  'Pass456@'),
UserAccount('robertobrowno',  '1234Pass!'),
UserAccount('patwil123',  'TestPass789#'),
UserAccount('JJones41',  'MyPass2025$'), 
UserAccount('cherrygarciaJen',  'Pass!Qwerty'),
UserAccount('MicMillerx',  'TempPass@123'),
UserAccount('LinDavis',  'Pass2025$'),
UserAccount('WillRodPod',  'StrongPass#001'), 
UserAccount('ElizabethMartinez',  'PassW@ord789'),
UserAccount('HertDavid',  'SimplePass!34'),
UserAccount('NotJenLopez',  'NewPass456&'),
UserAccount('JosephGlez',  'TestAcc#567'),
UserAccount('KParezzz',  'Secret#Pass123'),
UserAccount('CharlesYoung',  'Pass12$5678'),
UserAccount('SusanAllen',  'Qwerty@2025'),
UserAccount('ThomasSanChez',  'T3stP@ssWord'),
UserAccount('Nancy24wRight',  'Alpha#B@tta'),
UserAccount('ChristopherKing',  'RandomP@ss1'),
UserAccount('PatriciaScott',  'Temp$Pass2025'),
UserAccount('Danieldaygreen',  'Secure!Pass001'),
# helpers
UserAccount('DorothyAdams',  'Pass$5678Word'),
UserAccount('MarkBaker',  'Str0ngPass!234'),
UserAccount('JenniferNelson',  'Code$Pass4321'),
UserAccount('StevenCarter',  'Hello@World123'),
UserAccount('hELENmITchell987',  'Test!Code2025'),
# admin
UserAccount('EdwardPerez',  'SafePass!1234'),
UserAccount('LisaRoberts',  'NewCode@234'),
UserAccount('briAnwalkErr',  'Password$001'),

 ]
print('Username | Password | Hash | Password Matches Hash')

for user in users:
    password_hash=flask_bcrypt.generate_password_hash(user.password)
    password_matches_hash = flask_bcrypt.check_password_hash(password_hash, user.password)
    print(f'{user.username} | {user.password} | {password_hash.decode()} | {password_matches_hash}')

