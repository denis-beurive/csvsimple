#!/bin/bash

#
# Usage:
#
#         . ENV.SH
#

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ] ; do SOURCE="$(readlink "$SOURCE")"; done
PWD="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

echo "Adding $PWD to PYTHONPATH"

export PYTHONPATH=$PWD:$PYTHONPATH
