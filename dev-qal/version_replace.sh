#!/bin/bash

function version_replace {
  if [ "$#" -lt 3 ] ; then echo $0 '<file_name> <app_name> <version>'; return 99; fi
  _TARGET=$1
  _APP=$2
  _VER=$3
  _TMP=__$$.txt
  cat $_TARGET | tr '\n' '\r' | sed -e "s|  $_APP\:\r    version\: \"snapshot[-0-9]*\"|  $_APP\:\r    version\: \"$_VER\"|g" | tr '\r' '\n' > $_TMP
  rm $_TARGET
  mv $_TMP $_TARGET
}
version_replace $*
