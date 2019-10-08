FROM centos:7
COPY *.rpm .
RUN yum install -y epel-release
CMD yum localinstall -y *.rpm