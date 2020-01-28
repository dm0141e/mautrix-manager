#!/bin/sh

# Define functions.
fixperms() {
	chown -R $UID:$GID /data /opt/mautrix-manager
}

cd /opt/mautrix-manager/backend

if [ ! -f /data/config.yaml ]; then
	cp example-config.yaml /data/config.yaml
	echo "Didn't find a config file."
	echo "Copied default config file to /data/config.yaml"
	echo "Modify that config file to your liking."
	echo "Start the container again after that to generate the registration file."
	fixperms
	exit
fi

fixperms
exec su-exec $UID:$GID python3 -m mautrix_manager -c /data/config.yaml
