Name:    vmauth
Version: 1.79.4
Release: 1
Summary: vmauth executes a list of the given alerting or recording rules against configured address. It is heavily inspired by Prometheus implementation and aims to be compatible with its syntax.

Group:   Development Tools
License: ASL 2.0
URL: https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/v%{version}/vmutils-linux-amd64-v%{version}.tar.gz

Source0: %{name}.service
Source1: %{name}.conf
Source2: config.yml

BuildRequires: curl
Requires(pre): /usr/sbin/useradd, /usr/bin/getent, /usr/bin/echo, /usr/bin/chown
Requires(postun): /usr/sbin/userdel

# Use systemd for fedora >= 18, rhel >=7, SUSE >= 12 SP1 and openSUSE >= 42.1
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7) || (!0%{?is_opensuse} && 0%{?suse_version} >=1210) || (0%{?is_opensuse} && 0%{?sle_version} >= 120100)

%if %{use_systemd}
Requires: systemd
BuildRequires: systemd
%endif

%description
vmauth executes a list of the given alerting or recording rules against configured address. It is heavily inspired by Prometheus implementation and aims to be compatible with its syntax.

%prep
BuildRequires: curl
curl -L %{url} > vmutils.tar.gz
tar -zxf vmutils.tar.gz

%install
%{__install} -m 0755 -d %{buildroot}%{_bindir}
%{__install} -m 0755 -d %{buildroot}/etc/victoriametrics/vmauth
cp %{SOURCE1} %{buildroot}/etc/victoriametrics/vmauth/
cp %{SOURCE2} %{buildroot}/etc/victoriametrics/vmauth/
%if %{use_systemd}
%{__mkdir} -p %{buildroot}%{_unitdir}
%{__install} -m644 %{SOURCE0} %{buildroot}%{_unitdir}/%{name}.service
%endif
cp vmauth-prod %{buildroot}%{_bindir}/vmauth-prod

%pre
/usr/bin/getent group victoriametrics > /dev/null || /usr/sbin/groupadd -r victoriametrics
/usr/bin/getent passwd victoriametrics > /dev/null || /usr/sbin/useradd -r -m -d /home/victoriametrics -s /bin/bash -g victoriametrics victoriametrics

%post
%if %use_systemd
/usr/bin/echo "Note: /etc/victoriametrics/vmauth/config contains examples. You should change this default config up to your needs and then start systemd service."
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
%{_bindir}/vmauth-prod
%dir %attr(0775, victoriametrics, victoriametrics) /etc/victoriametrics/vmauth
%config /etc/victoriametrics/vmauth/vmauth.conf
%config /etc/victoriametrics/vmauth/config.yml
%if %{use_systemd}
%{_unitdir}/vmauth.service
%endif
