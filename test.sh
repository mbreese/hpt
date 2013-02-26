#!/bin/bash
REAL=`python -c 'import os,sys;print os.path.realpath(sys.argv[1])' "$0"`
DIR=`dirname "$REAL"`

. "$DIR"/env/bin/activate
export PYTHONPATH=$PYTHONPATH:"$DIR"
export HIDE_ETA="1"

if [ "$1" == "" ]; then
    # run all tests...
    cd $DIR
    if [ "`which unit2`" != "" ]; then
        unit2 discover t 'test_*py' -v
    else
        python -m unittest discover t 'test_*py' -v
    fi
else
    while [ "$1" != "" ]; do
        echo "$1"
        exec $1
        # if [ $? -eq 0 ]; then
        #     coverage report
        # fi
        shift
    done
fi
