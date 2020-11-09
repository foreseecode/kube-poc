#!/bin/bash

function version_replace {
  if [ "$#" -lt 3 ] ; then echo $0 '<env> <app_name> <version>'; return 99; fi
  _TARGET="$1/$2/version.conf"
  _VER=$3
  echo -n $_VER > $_TARGET
}
version_replace $*
