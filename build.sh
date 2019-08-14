#!/usr/bin/env bash

rpmbuild -bb SPECS/acryl_node.spec || exit 1

rm /result/files/ -rf
cp -a /root/rpmbuild/RPMS/noarch/ /result/files