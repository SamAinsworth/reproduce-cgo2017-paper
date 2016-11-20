#! /bin/bash


. /home/ubuntu/CK/local/env/447c0a0b5fb205c1/env.sh
. /home/ubuntu/CK/local/env/da79d802e89822fa/env.sh 1
. /home/ubuntu/CK/local/env/ed9c4cfc42ed96d3/env.sh 1

. /home/ubuntu/CK/local/env/447c0a0b5fb205c1/env.sh 1

export CK_COMPILE_TYPE=auto


echo    executing code ...
 ./a.out > tmp-output1.tmp 2> tmp-output2.tmp
