##need to make sure requirements.txt files end in a newline for now
alias bip-compile-requirements="find . -name 'requirements.txt' -exec cat {} \; > _compiledrequirements.txt"
alias bip-compile-commands="find . -name 'commands.sh' -exec cat {} \; > _compiled1commands.sh"
alias bip-download-vipfeeds="wget -r http://data.votinginfoproject.org/feeds/"
alias bip-init="cd /var/bip && source /var/bip/py/bipdata/bin/activate"
alias bip-build-ohio="bip-init && bip cleandb && time bip buildstates oh"
alias bip-build-test="bip-init && bip cleandb && time bip buildstates testcsv"