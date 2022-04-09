import telebot
import qrcode
import image
import time
import os

from keyboa import Keyboa


DNS = '10.0.0.1'
Public_key = 'key'
IP = ''
PORT = 0 
bot = telebot.TeleBot('') # telegram bot keys
verefy_id = [12343] # user id from admin telegram
config_patch = './config_files'

def verification(id):
    return (1 if id in verefy_id else 0)


@bot.message_handler(commands=["show_keys"])
def show_keys(message):
    if verification(message.from_user.id):
        @bot.callback_query_handler(func=lambda call: True)
        def check_user(call):
            user = call.data
            bot.send_photo(message.chat.id, photo=open(f'./config_files/{user}.png', 'rb'))
            bot.send_document(message.chat.id, document=open(f'./config_files/{user}.conf', 'rb'))

        try:
            counter = 0
            while True:
                bot.delete_message(message.chat.id, message.message_id - counter)
        except:
            pass

        users = [file.replace('.conf', '') for file in os.listdir('./config_files') if 'conf' in file]
        user_kb = Keyboa(items=users, copy_text_to_callback=True,  items_in_row=3)

        bot.send_message(message.chat.id, reply_markup=user_kb(), text='Users:')





@bot.message_handler(commands=["add_connect"])
def add_connect(message):
    def send_data(message, connect_name):
        bot.send_photo(message.chat.id, photo=open(f'./config_files/{connect_name}.png', 'rb'))
        bot.send_document(message.chat.id, document=open(f'./config_files/{connect_name}.conf', 'rb'))
        os.system('systemctl restart wg-quick@wg0')


    def name_connect(message):
        bot.send_message(message.chat.id, 'Send me connection name:')
        bot.register_next_step_handler(message, ip_address)

    def ip_address(message):
        connect_name = message.text
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id-1)
        bot.send_message(message.chat.id, 'Send me user ip:')
        bot.register_next_step_handler(message, create_connect, connect_name)

    def create_connect(message, connect_name):
        ip = message.text
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id-1)
        bot.send_message(message.chat.id, '🔃Generate keys🔃')

        os.system(f'wg genkey | tee /etc/wireguard/{connect_name}_privatekey | wg pubkey | tee /etc/wireguard/{connect_name}_publickey')
        time.sleep(3)
        with open(f'./{connect_name}_privatekey', 'r') as fprivatkey, open(f'./{connect_name}_publickey', 'r') as fpublickey, open(f'./config_files/{connect_name}.conf', 'w') as configfile:
            privatkey = fprivatkey.read()
            publickey = fpublickey.read()

            configfile_text = (f'''[Interface]
PrivateKey = {privatkey}
Address = 10.0.0.{ip}/24
DNS = {DNS}

[Peer]
PublicKey = {Public_key}
AllowedIPs = 0.0.0.0/0
Endpoint = {IP}:{PORT}
PersistentKeepalive = 20
''')
            configfile.write(configfile_text)
        config_for_server = f'''\n\n#{connect_name}
[Peer]
PublicKey = {publickey}AllowedIPs = 10.0.0.{ip}/32'''
        os.system(f'echo "{config_for_server}" >> ./wg0.conf')
        img = qrcode.make(configfile_text)
        img.save(f'./config_files/{connect_name}.png')

        send_data(message, connect_name)

    try:
        counter = 0
        while True:
            bot.delete_message(message.chat.id, message.message_id - counter)
    except:
        pass
    name_connect(message) if verification(message.from_user.id) else 0




bot.polling(True)