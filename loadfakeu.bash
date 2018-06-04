#!/bin/bash
echo "asdghsfsd"
if [ $# -eq 0 ]
  then
    dir=.
  else
    dir=$1
fi
'${1:-.}'
chmod +x prob2.py $dir
python3 prob2.py