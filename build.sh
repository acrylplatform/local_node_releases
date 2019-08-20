#!/usr/bin/env bash
export RPM_SPEC_FILE="SPECS/acryl_node.spec"

echo "Checking rpm spec file..."
rpmlint $RPM_SPEC_FILE || exit 1
echo "Building rpm binary file..."
rpmbuild -bb $RPM_SPEC_FILE || exit 1

rm /result/files/ -rf
cp -a /root/rpmbuild/RPMS/noarch/ /result/files