sudo mkdir /var/bip
sudo chown $USER:$USER /var/bip
. ./commands.sh
mkdir /var/bip/src
cp -r ../../ /var/bip/src
touch /var/bip/src/__init__.py
cd /var/bip
#git clone https://github.com/neworganizing/bip-data.git src
ln -s src/deploy/manage.py ./manage.py
ln src/deploy/manage.py /usr/bin/bip
. src/deploy/scripts/commands.sh
mkdir data exports py vip
cd vip
git clone https://github.com/votinginfoproject/pythonvalidator.git
git clone https://github.com/votinginfoproject/scripts.git
git clone https://github.com/votinginfoproject/twitterbot.git
git clone https://github.com/votinginfoproject/tools.git
git clone https://github.com/ballotinfo/VAVE.git vave
touch __init__.py
cd /var/bip/py
virtualenv --no-site-packages bipdata
#not sure if this block is necessary
virtualenv --no-site-packages vave
. /var/bip/py/vave/bin/activate
cd /var/bip/vip/vave
pip install -r requirements.txt
####################################
. /var/bip/py/bipdata/bin/activate
cd /var/bip
bip-compile-requirements
pip install -r _compiledrequirements.txt
cd data
bip-download-vipfeeds
find . -name '*.html*' -exec rm {} \;
cd /var/bip
echo "All done!"
