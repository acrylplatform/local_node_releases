#!/usr/bin/env bash

if [[ $# -eq 0 ]] ; then
    echo 'No data address supplied'
    exit 1
fi

ADDRESS=$1
echo "Checking updates in $ADDRESS data..."
UPDATE_DATA=($(/usr/bin/python3.6 /opt/acryl/get_update_urls.py $ADDRESS | jq -r '.rpm_package_url,.sha256_checksum'))
RPM_URL=${UPDATE_DATA[0]}
RPM_SHA256_CHECKSUM=${UPDATE_DATA[1]}
echo "Checking versions and checksums..."
PACKAGE_CHECKSUM=$(yumdb get checksum_data acryl-node-binary | tr " " '\n' | tail -n 1)

if [[ ${RPM_SHA256_CHECKSUM} == ${PACKAGE_CHECKSUM} ]];
then
    echo "Latest version is installed"
    exit 1
fi

echo "Downloading rpm..."
TMP_DIR=$(mktemp -d -t $(date +%d-%m-%Y-%H-%M-%S)-XXXXXXXX)
trap "rm -rf ${TMP_DIR}" EXIT
curl -L -o ${TMP_DIR}/acryl_latest.rpm $RPM_URL
echo "Checking downloaded rpm checksum"
echo "$RPM_SHA256_CHECKSUM  $TMP_DIR/acryl_latest.rpm" > ${TMP_DIR}/RPM_SHA256
sha256sum -c ${TMP_DIR}/RPM_SHA256

if [[ $? -ne 0 ]];
then
    FILE_CHECKSUM=$(sha256sum ${TMP_DIR}/acryl_latest.rpm | cut -d " " -f 1)
    echo "Checksum is not matching"
    exit 1
fi

echo "Installing rpm..."
yum -y localinstall ${TMP_DIR}/acryl_latest.rpm
