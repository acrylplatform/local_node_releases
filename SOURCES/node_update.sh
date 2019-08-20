#!/usr/bin/env bash
echo "Checking for updates..."
ADDRESS="3EGzmk5hjzjin649kzmLM7B5mBx4vTyRSuy"
UPDATE_DATA=($(/usr/bin/python3.6 /opt/acryl/get_update_urls.py $ADDRESS | jq -r '.rpm_package_url,.sha256_checksum'))
RPM_URL=${UPDATE_DATA[0]}
RPM_SHA256_CHECKSUM=${UPDATE_DATA[1]}
echo "Checking versions and checksums..."
PACKAGE_CHECKSUM=$(yumdb get checksum_data acryl-node-binary | tr " " '\n' | tail -n 1)
if [ $RPM_SHA256_CHECKSUM == $PACKAGE_CHECKSUM ];
then
    echo "Latest version is installed"
    exit 1
fi
echo "Downloading rpm..."
curl -L -o /tmp/acryl_latest.rpm $RPM_URL
echo "Checking downloaded rpm checksum"
echo "$RPM_SHA256_CHECKSUM  /tmp/acryl_latest.rpm" > /tmp/RPM_SHA256
sha256sum -c /tmp/RPM_SHA256
if [ $? -ne 0 ]; 
then
    echo "Checksum is not matching"
    exit 1
fi

echo "Installing rpm..."
yum localinstall /tmp/acryl_latest.rpm
rm /tmp/acryl_latest.rpm
