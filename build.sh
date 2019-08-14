#!/usr/bin/env bash

rpmbuild -bb SPECS/acryl_node.spec || exit 1

rm /result/files -rf
cp -a rpmbuild/RPMS/noarch /result/files