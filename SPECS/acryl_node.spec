%global __python %{__python36}
%define __jar_repack 0
%define service_user acryl_runner
%define service_group acryl_runner
%define service_home /opt/acryl
%define nginx_data_basedir /opt/acryl_nginx
%define release_date %(date "+%a %b %e %Y")

Name:       acryl-local-node
Version:    3.0
Release:    1%{?dist}
Summary:    Acryl Local Node binary and configuration files
License:    MIT
Requires:   java-1.8.0-openjdk, python36, nginx, jq
URL:        https://github.com/acrylplatform/
Vendor:     Acryl
BuildRequires: systemd, python36
Requires(pre): shadow-utils
BuildArch: noarch

Source0: acryl.jar
Source1: acryl_node.service
Source2: acryl_node_update.service
Source3: get_update_urls.py
Source4: node_update.sh
Source5: acryl_node_update.timer
Source6: acryl_node.conf
Source7: acryl_nginx.conf
Source8: acryl_nginx.service

%description
Acryl Local Node files: executable, config files, scripts etc.

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
%{__mkdir} -p %{buildroot}%{_sharedstatedir}/acryl_nginx/tmp/client_body
%{__mkdir} -p %{buildroot}%{_sharedstatedir}/acryl_nginx/tmp/proxy_temp
%{__install} -m755 %SOURCE0 %{buildroot}%{service_home}/acryl.jar
%{__install} -m644 %SOURCE1 %{buildroot}%{_unitdir}/acryl_node.service
%{__install} -m644 %SOURCE2 %{buildroot}%{_unitdir}/acryl_node_update.service
%{__install} -m755 %SOURCE3 %{buildroot}%{service_home}/get_update_urls.py
%{__install} -m755 %SOURCE4 %{buildroot}%{service_home}/node_update.sh
%{__install} -m644 %SOURCE5 %{buildroot}%{_unitdir}/acryl_node_update.timer
%{__install} -m755 %SOURCE6 %{buildroot}%{service_home}/acryl_node.conf
%{__install} -m644 %SOURCE7 %{buildroot}%{service_home}/acryl_nginx.conf
%{__install} -m644 %SOURCE8 %{buildroot}%{_unitdir}/acryl_nginx.service

%files
%dir %attr(0744, %service_user,%service_group) %{service_home}
%dir %attr(0744, %service_user,%service_group) %{service_home}/nginx.conf.d
%dir %attr(0744, %service_user,%service_group) %{_sharedstatedir}/acryl_nginx/tmp/client_body
%dir %attr(0744, %service_user,%service_group) %{_sharedstatedir}/acryl_nginx/tmp/proxy_temp
%attr(0755,%service_user,%service_group) %{service_home}/acryl.jar
%attr(0755,%service_user,%service_group) %{service_home}/get_update_urls.py
%attr(0755,%service_user,%service_group) %{service_home}/node_update.sh
%attr(0644,%service_user,%service_group) %{service_home}/acryl_node.conf
%attr(0644,%service_user,%service_group) %{service_home}/acryl_nginx.conf
%{_unitdir}/acryl_node.service
%{_unitdir}/acryl_node_update.service
%{_unitdir}/acryl_node_update.timer
%{_unitdir}/acryl_nginx.service


%post
if [ $1 -eq 1 ]; then
    /usr/bin/systemctl preset acryl_node.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl preset acryl_node_update.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl preset acryl_nginx.service >/dev/null 2>&1 ||:
fi

%changelog
* Mon Oct 28 2019 Dmitriy Peregudov <dima@acrylplatform.com> - 3.0-1
- New jar version (1.0.1-acrylplatform)

* Tue Aug 27 2019 Dmitriy Peregudov <dima@acrylplatform.com> - 2.0-11
- Removed travis update data blockchain publication

* Mon Aug 26 2019 Dmitriy Peregudov <dima@acrylplatform.com> - 2.0-10
- Set correct package name in update script

* Mon Aug 26 2019 Dmitriy Peregudov <dima@acrylplatform.com> - 2.0-7
- Release bump

* Mon Aug 26 2019 Dmitriy Peregudov <dima@acrylplatform.com> - 2.0-6
- Added release data blockchain publishing
- Changed update data address
- Fixed update service

* Thu Aug 22 2019 Dmitriy Peregudov <dima@acrylplatform.com> - 2.0-5
- Changelog file update
- Release bump

* Wed Aug 21 2019 Dmitriy Peregudov <dima@acrylplatform.com> - 2.0-4
- Added nginx temp directories for runner user
- Various spec file fixes

* Tue Aug 20 2019 Dmitriy Peregudov <dima@acrylplatform.com> - 2.0-3
- Added nginx config and service file
- Added CHANGELOG and LICENSE file
- Added lint for rpm spec file
- Various spec file fixes
