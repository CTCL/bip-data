sudo mkdir /var/bip
sudo chown $USER:$USER /var/bip
cd /var/bip
git clone git@github.com:neworganizing/bip-data.git src
ln -s src/deploy/manage.py ./manage.py
. src/deploy/scripts/commands.sh
mkdir data exports py vip
cd vip
git clone https://github.com/votinginfoproject/pythonvalidator.git
git clone https://github.com/votinginfoproject/scripts.git
git clone https://github.com/votinginfoproject/twitterbot.git
git clone https://github.com/votinginfoproject/tools.git
git clone https://github.com/votinginfoproject/VAVE.git
cd /var/bip
bip-compile-requirements
cd py
virtualenv --no-site-packages bipdata
. bipdata/bin/activate
cd /var/bip
pip install -r _compiledrequirements.txt
cd data
bip-download-vipfeeds
cd /var/bip
echo "All done!"
