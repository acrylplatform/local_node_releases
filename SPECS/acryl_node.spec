%global __python %{__python36}
%define __jar_repack 0
%define service_user acryl_runner
%define service_group acryl_runner
%define service_home /opt/acryl
%define nginx_data_basedir /opt/acryl_nginx_testnet
%define release_date %(date "+%a %b %e %Y")

Name:       acryl-local-node-testnet
Version:    1.0.0
Release:    3%{?dist}
Summary:    Acryl Local Node binary and configuration files for testnet
License:    MIT
Requires:   java-1.8.0-openjdk, python36, nginx, jq
URL:        https://github.com/acrylplatform/
Vendor:     Acryl
BuildRequires: systemd, python36
Requires(pre): shadow-utils
BuildArch: noarch

Source0: acryl_testnet.jar
Source1: acryl_node_testnet.service
Source2: acryl_node_update_testnet.service
Source3: get_update_urls_testnet.py
Source4: node_update_testnet.sh
Source5: acryl_node_update_testnet.timer
Source6: acryl_node_testnet.conf
Source7: acryl_nginx_testnet.conf
Source8: acryl_nginx_testnet.service

%description
Acryl Local Node files: executable, config files, scripts etc. for testnet

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
%{__mkdir} -p %{buildroot}%{service_home}/nginx.conf.d
%{__mkdir} -p %{buildroot}%{_sharedstatedir}/acryl_nginx_testnet/tmp/client_body
%{__mkdir} -p %{buildroot}%{_sharedstatedir}/acryl_nginx_testnet/tmp/proxy_temp
%{__install} -m755 %SOURCE0 %{buildroot}%{service_home}/acryl_testnet.jar
%{__install} -m644 %SOURCE1 %{buildroot}%{_unitdir}/acryl_node_testnet.service
%{__install} -m644 %SOURCE2 %{buildroot}%{_unitdir}/acryl_node_update_testnet.service
%{__install} -m755 %SOURCE3 %{buildroot}%{service_home}/get_update_urls_testnet.py
%{__install} -m755 %SOURCE4 %{buildroot}%{service_home}/node_update_testnet.sh
%{__install} -m644 %SOURCE5 %{buildroot}%{_unitdir}/acryl_node_update_testnet.timer
%{__install} -m755 %SOURCE6 %{buildroot}%{service_home}/acryl_node_testnet.conf
%{__install} -m644 %SOURCE7 %{buildroot}%{service_home}/acryl_nginx_testnet.conf
%{__install} -m644 %SOURCE8 %{buildroot}%{_unitdir}/acryl_nginx_testnet.service

%files
%dir %attr(0744, %service_user,%service_group) %{service_home}
%dir %attr(0744, %service_user,%service_group) %{service_home}/nginx.conf.d
%dir %attr(0744, %service_user,%service_group) %{_sharedstatedir}/acryl_nginx_testnet/tmp/client_body
%dir %attr(0744, %service_user,%service_group) %{_sharedstatedir}/acryl_nginx_testnet/tmp/proxy_temp
%attr(0755,%service_user,%service_group) %{service_home}/acryl_testnet.jar
%attr(0755,%service_user,%service_group) %{service_home}/get_update_urls_testnet.py
%attr(0755,%service_user,%service_group) %{service_home}/node_update_testnet.sh
%attr(0644,%service_user,%service_group) %{service_home}/acryl_node_testnet.conf
%attr(0644,%service_user,%service_group) %{service_home}/acryl_nginx_testnet.conf
%{_unitdir}/acryl_node_testnet.service
%{_unitdir}/acryl_node_update_testnet.service
%{_unitdir}/acryl_node_update_testnet.timer
%{_unitdir}/acryl_nginx_testnet.service


%post
if [ $1 -eq 1 ]; then
    /usr/bin/systemctl preset acryl_node_testnet.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl preset acryl_node_update_testnet.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl preset acryl_nginx_testnet.service >/dev/null 2>&1 ||:
fi

%changelog
* Mon Oct 7 2019 Dmitriy Peregudov <dima@acrylplatform.com> - 1.0.0-3
- New jar version
- Updated config: new fetures, feature approval and activation period, matcher

* Mon Sep 2 2019 Dmitriy Peregudov <dima@acrylplatform.com> - 1.0-1
- First testnet node

