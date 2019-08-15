%global __os_install_post %(echo '%{__os_install_post}' | sed -e 
's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%define service_user acryl_runner
%define service_group acryl_runner
%define service_home /opt/acryl
%define release_date %(date "+%a %b %e %Y")

Name:       acryl-local-node
Version:    1
Release:    1%{?dist}
Summary:    Acryl Local Node binary and configuration files
License:    MIT
Requires:   java-1.8.0-openjdk, python36, nginx
URL: 	    https://github.com/acrylplatform/
Vendor:     Acryl
BuildRequires: systemd
Requires(pre): shadow-utils
BuildArch: noarch

Source0: acryl.jar
Source1: acryl_node.service
Source2: acryl_node_update.service
Source3: get_update_urls.py
Source4: node_update.sh
Source5: acryl_node_update.timer
Source6: acryl_node.conf

%define __jar_repack 0

%description
Acryl Local Node files: excecutable, config files, scripts etc.

%pre
getent group %{service_group} >/dev/null || groupadd -r %{service_group}
getent passwd %{service_user} >/dev/null || \
    useradd -r -g %{service_group} -s /sbin/nologin \
    -d %{service_home} -c "acryl service user"  %{service_user}
exit 0

%build

%install
%{__mkdir} -p %{buildroot}%{_unitdir}
%{__mkdir} -p %{buildroot}%{service_home}
%{__install} -m755 %SOURCE0 %{buildroot}%{service_home}/acryl.jar
%{__install} -m644 %SOURCE1 %{buildroot}%{_unitdir}/acryl_node.service
%{__install} -m644 %SOURCE2 %{buildroot}%{_unitdir}/acryl_node_update.service
%{__install} -m755 %SOURCE3 %{buildroot}%{service_home}/get_update_urls.py
%{__install} -m755 %SOURCE4 %{buildroot}%{service_home}/node_update.sh
%{__install} -m644 %SOURCE5 %{buildroot}%{_unitdir}/acryl_node_update.timer
%{__install} -m755 %SOURCE6 %{buildroot}%{service_home}/acryl_node.conf

%files
%dir %attr(0744, %service_user,%service_group) %{service_home}
%attr(0755,%service_user,%service_group) %{service_home}/acryl.jar
%attr(0755,%service_user,%service_group) %{service_home}/get_update_urls.py
%attr(0755,%service_user,%service_group) %{service_home}/node_update.sh
%attr(0644,%service_user,%service_group) %{service_home}/acryl_node.conf
%{_unitdir}/acryl_node.service
%{_unitdir}/acryl_node_update.service
%{_unitdir}/acryl_node_update.timer


%post
if [ $1 -eq 1 ]; then
    /usr/bin/systemctl preset acryl_node.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl preset acryl_node_update.service >/dev/null 2>&1 ||:
fi

%changelog
