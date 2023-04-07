Name:    vmalert
Version: 1.90.0
Release: 1
Summary: vmalert executes a list of the given alerting or recording rules against configured address. It is heavily inspired by Prometheus implementation and aims to be compatible with its syntax.

Group:   Development Tools
License: ASL 2.0
URL: https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/v%{version}/vmutils-linux-amd64-v%{version}.tar.gz

Source0: %{name}.service
Source1: %{name}.conf
Source2: alerts.yml

Requires(pre): /usr/sbin/useradd, /usr/bin/getent, /usr/bin/echo, /usr/bin/chown
Requires(postun): /usr/sbin/userdel

# Use systemd for fedora >= 18, rhel >=7, SUSE >= 12 SP1 and openSUSE >= 42.1
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7) || (!0%{?is_opensuse} && 0%{?suse_version} >=1210) || (0%{?is_opensuse} && 0%{?sle_version} >= 120100)

%if %{use_systemd}
Requires: systemd
BuildRequires: systemd
%endif

%description
vmalert executes a list of the given alerting or recording rules against configured address. It is heavily inspired by Prometheus implementation and aims to be compatible with its syntax.

%prep
curl -L %{url} > vmutils.tar.gz
tar -zxf vmutils.tar.gz

%install
%{__install} -m 0755 -d %{buildroot}%{_bindir}
%{__install} -m 0755 -d %{buildroot}/etc/victoriametrics/vmalert
cp %{SOURCE1} %{buildroot}/etc/victoriametrics/vmalert/
cp %{SOURCE2} %{buildroot}/etc/victoriametrics/vmalert/
%if %{use_systemd}
%{__mkdir} -p %{buildroot}%{_unitdir}
%{__install} -m644 %{SOURCE0} %{buildroot}%{_unitdir}/%{name}.service
%endif
cp vmalert-prod %{buildroot}%{_bindir}/vmalert-prod

%pre
/usr/bin/getent group victoriametrics > /dev/null || /usr/sbin/groupadd -r victoriametrics
/usr/bin/getent passwd victoriametrics > /dev/null || /usr/sbin/useradd -r -m -d /home/victoriametrics -s /bin/bash -g victoriametrics victoriametrics

%post
%if %use_systemd
/usr/bin/systemctl daemon-reload
%endif

%preun
%if %use_systemd
/usr/bin/systemctl stop %{name}
%endif

%postun
%if %use_systemd
/usr/bin/systemctl daemon-reload
%endif

%files
%{_bindir}/vmalert-prod
%dir %attr(0775, victoriametrics, victoriametrics) /etc/victoriametrics/vmalert
%config /etc/victoriametrics/vmalert/vmalert.conf
%config /etc/victoriametrics/vmalert/alerts.yml
%if %{use_systemd}
%{_unitdir}/vmalert.service
%endif
