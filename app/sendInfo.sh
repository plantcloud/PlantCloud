#!/bin/bash
set -x
## Code to send info to the server
MACHINEID=$(cat /var/lib/dbus/machine-id)
REMOTEFOLDER=$(cat ~/.folderadd)
IPADD=$(cat ~/.ipadd)
CWD=$(pwd)
JPGFILE=$1
YESNO=$2
PLANTTYPE=$3
DISEASE=$4
LAT=$5
LON=$6
DATETIME=$(date +"%y%m%d%k%M%S")
DEST_FOLDER=$REMOTEFOLDER/$MACHINEID/$PLANTTYPE/$DISEASE
DEST_NAME=$DEST_FOLDER/${DATETIME}_$YESNO.jpg
DEST_GPSINFO=${REMOTEFOLDER}/${MACHINEID}/latlon.txt
ssh $IPADD mkdir -p $DEST_FOLDER
scp -C $JPGFILE $IPADD:$DEST_NAME
ssh $IPADD "echo ${LAT},${LON},${DATETIME} >> ${DEST_GPSINFO}"
