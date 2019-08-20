FROM centos:7
MAINTAINER Dmitriy Peregudov <dima@acrylplatform.com>

RUN rpm --import http://download.fedoraproject.org/pub/epel/RPM-GPG-KEY-EPEL-7 \
 && yum -y install epel-release \
 && yum -y install rpm-build rpmdevtools patch curl less scl-utils scl-utils-build rpmlint

RUN yum -y install python36

RUN rpmdev-setuptree
WORKDIR /root/rpmbuild

ADD SPECS/ ./SPECS/
ADD SOURCES/ ./SOURCES/
ADD build.sh ./build.sh
RUN chmod +x ./build.sh

CMD ["./build.sh"]