#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

cmdname=$(basename $0)

if [[ ${#*} != 7 ]]
then
	echo "Usage is "
	echo "${cmdname} DeviceType."
	echo "DeviceType: 1 for device, 2 for IoT hub."
	exit 1
fi

LOCALFILE=/etc/rc.local
UDHCFILE=/etc/udhcpd.conf
DHCPCFILE=/etc/dhcpcd.conf

if [[ ${1} == 1 ]]
then
	echo "We are setting up a PlantCloud client device."
	cd ${HOME}/pkgs
	sudo dpkg -i *
	cd ${HOME}/whls
	sudo pip install tensorflow --no-index -f ${HOME}/whls
	echo "#!/bin/sh -e" > ${LOCALFILE}
	echo "#" >> ${LOCALFILE}
	echo "# rc.local" >> ${LOCALFILE}
	echo "#" >> ${LOCALFILE}
	echo "# This script is executed at the end of each multiuser runlevel." >> ${LOCALFILE}
	echo "# Make sure that the script will \"exit 0\" on success or any other" >> ${LOCALFILE}
	echo "# value on error. " >> ${LOCALFILE}
	echo " " >> ${LOCALFILE}
	echo "# Setup config for the ad-hoc network PlantCloud " >> ${LOCALFILE}
	echo "iwconfig wlan0 mode Ad-Hoc " >> ${LOCALFILE}
	echo "iwconfig wlan0 essid PlantCloud " >> ${LOCALFILE}
	echo " " >> ${LOCALFILE}
	echo "exit 0" >> ${LOCALFILE}

elif [[ ${1} == 2 ]]
then
	echo "We are setting up a PlantCloud IoT hub."
	cd ${HOME}/pkgs
	sudo dpkg -i *
	echo "#!/bin/sh -e" > ${LOCALFILE}
	echo "#" >> ${LOCALFILE}
	echo "# rc.local" >> ${LOCALFILE}
	echo "#" >> ${LOCALFILE}
	echo "# This script is executed at the end of each multiuser runlevel." >> ${LOCALFILE}
	echo "#" >> ${LOCALFILE}
	echo "# Make sure that the script will \"exit 0\" on success or any other" >> ${LOCALFILE}
	echo "# value on error." >> ${LOCALFILE}
	echo " " >> ${LOCALFILE}
	echo "ifconfig wlan0 down" >> ${LOCALFILE}
	echo "ifconfig wlan0 mode Ad-Hoc" >> ${LOCALFILE}
	echo "ifconfig wlan0 essid PlantCloud" >> ${LOCALFILE}
	echo "sleep 1" >> ${LOCALFILE}
	echo "ifconfig wlan0 10.2.2.2" >> ${LOCALFILE}
	echo "ifconfig wlan0 up" >> ${LOCALFILE}
	echo "udhcpd /etc/udhcpd.conf" >> ${LOCALFILE}
	echo " " >> ${LOCALFILE}
	echo "exit 0" >> ${LOCALFILE}
	echo "start      10.2.2.3" > ${UDHCFILE}
	echo "end        10.2.2.200" >> ${UDHCFILE}
	echo "interface  wlan0" >> ${UDHCFILE}
	echo "max_leases 128" >> ${UDHCFILE}
	echo "denyinterfaces    wlan0" > ${DHCPCFILE}

fi

echo "Please reboot for changes to take effect."
