#!/bin/bash

printf "\33[1;35mWELCOME TO UKNOWIT INSTALLATION!!\r"

sleep 1

printf "Creating the environment for you......\t :)\r"

sleep 1

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

if ! printf "python $SCRIPT_DIR/uknowit.py \$1 \$2 \$3 \$4" > /usr/bin/uknowit; then
    printf "There's something wrong.. Did you run this with 'sudo'? If not please use it :)\n"
else
    chmod +x /usr/bin/uknowit
    sleep 1
    printf "DONE! Yeahh, Just it! Easy right?....\t :)\n"
fi

