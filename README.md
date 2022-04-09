# Wireguard-keys-from-telegram
wireguard key generator using telegram bot
To work, you must fill in the data on top of the code. and move it to the /etc/wireguard folder by creating the /etc/wireguard/config_files folder


#INSTALL#

git clone
cd ./Wireguard-keys-from-telegram
sudo mv ./bot.py /etc/wireguard
sudo mkdir config_files
nano bot.py 

Fill in the fields with your details

sudo python3 ./bot.py
