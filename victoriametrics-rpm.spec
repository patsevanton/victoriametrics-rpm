Name:    victoriametrics
Version: 1.65.0
Release: 1
Summary: The best long-term remote storage for Prometheus

Group:   Development Tools
License: ASL 2.0
URL: https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/v%{version}/victoria-metrics-amd64-v%{version}.tar.gz

Source0: %{name}.service
Source1: victoriametrics.conf
Source2: vmagent.conf
Source3: prometheus.yml
Source4: vmagent.service
Source5: vmalert.conf
Source6: alerts.yml
Source7: vmalert.service
Source8: vmauth.conf
Source9: config.yml
Source10: vmauth.service
Requires(pre): /usr/sbin/useradd, /usr/bin/getent, /usr/bin/echo, /usr/bin/chown
Requires(postun): /usr/sbin/userdel

# Use systemd for fedora >= 18, rhel >=7, SUSE >= 12 SP1 and openSUSE >= 42.1
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7) || (!0%{?is_opensuse} && 0%{?suse_version} >=1210) || (0%{?is_opensuse} && 0%{?sle_version} >= 120100)

%if %{use_systemd}
Requires: systemd
BuildRequires: systemd
%endif

%description
VictoriaMetrics - the best long-term remote storage for Prometheus

%prep
curl -L %{url} > victoria-metrics.tar.gz
tar -zxf victoria-metrics.tar.gz
curl -L https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/v%{version}/vmutils-amd64-v%{version}.tar.gz > vmutils.tar.gz
tar -zxf vmutils.tar.gz
curl -L https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/v%{version}/victoria-metrics-amd64-v%{version}-cluster.tar.gz > victoria-metrics-cluster.tar.gz
tar -zxf victoria-metrics-cluster.tar.gz

%install
%{__install} -m 0755 -d %{buildroot}%{_bindir}
%{__install} -m 0755 -d %{buildroot}/etc/default/
%{__install} -m 0755 -d %{buildroot}/etc/victoriametrics/vmagent
%{__install} -m 0755 -d %{buildroot}/etc/victoriametrics/vmalert
%{__install} -m 0755 -d %{buildroot}/etc/victoriametrics/vmauth
cp %{SOURCE1} %{buildroot}/etc/default/
cp %{SOURCE2} %{buildroot}/etc/victoriametrics/vmagent/
cp %{SOURCE3} %{buildroot}/etc/victoriametrics/vmagent/
cp %{SOURCE5} %{buildroot}/etc/victoriametrics/vmalert/
cp %{SOURCE6} %{buildroot}/etc/victoriametrics/vmalert/
cp %{SOURCE8} %{buildroot}/etc/victoriametrics/vmauth/
cp %{SOURCE9} %{buildroot}/etc/victoriametrics/vmauth/
cp victoria-metrics-prod %{buildroot}%{_bindir}/victoria-metrics-prod
%{__install} -m 0755 -d %{buildroot}/var/lib/victoria-metrics-data
%if %{use_systemd}
%{__mkdir} -p %{buildroot}%{_unitdir}
%{__install} -m644 %{SOURCE0} %{buildroot}%{_unitdir}/%{name}.service
%{__install} -m644 %{SOURCE4} %{buildroot}%{_unitdir}/vmagent.service
%{__install} -m644 %{SOURCE7} %{buildroot}%{_unitdir}/vmalert.service
%{__install} -m644 %{SOURCE10} %{buildroot}%{_unitdir}/vmauth.service
%endif
cp vmagent-prod %{buildroot}%{_bindir}/vmagent-prod
cp vmalert-prod %{buildroot}%{_bindir}/vmalert-prod
cp vmauth-prod %{buildroot}%{_bindir}/vmauth-prod
cp vmbackup-prod %{buildroot}%{_bindir}/vmbackup-prod
cp vmctl-prod %{buildroot}%{_bindir}/vmctl-prod
cp vmrestore-prod %{buildroot}%{_bindir}/vmrestore-prod
cp vminsert-prod %{buildroot}%{_bindir}/vminsert-prod
cp vmselect-prod %{buildroot}%{_bindir}/vmselect-prod
cp vmstorage-prod %{buildroot}%{_bindir}/vmstorage-prod

%pre
/usr/bin/getent group victoriametrics > /dev/null || /usr/sbin/groupadd -r victoriametrics
/usr/bin/getent passwd victoriametrics > /dev/null || /usr/sbin/useradd -r -d /var/lib/victoria-metrics-data -s /bin/bash -g victoriametrics victoriametrics
%{__mkdir} -p /var/lib/victoria-metrics-data
/usr/bin/echo "WARINING: chown -R victoriametrics:victoriametrics /var/lib/victoria-metrics-data"
/usr/bin/echo "THIS MAY TAKE SOME TIME"
/usr/bin/chown -R victoriametrics:victoriametrics /var/lib/victoria-metrics-data
/usr/bin/echo "WARINING: chown -R victoriametrics:victoriametrics /var/lib/vmagent-remotewrite-data"
/usr/bin/echo "THIS MAY TAKE SOME TIME"
/usr/bin/chown -R victoriametrics:victoriametrics /var/lib/vmagent-remotewrite-data

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
%config /etc/default/victoriametrics.conf
%{_bindir}/victoria-metrics-prod
%dir %attr(0775, victoriametrics, victoriametrics) /var/lib/victoria-metrics-data
%if %{use_systemd}
%{_unitdir}/%{name}.service
%endif

%package vmutils
Summary: Package for vmagent-prod  vmalert-prod  vmauth-prod  vmbackup-prod  vmctl-prod  vmrestore-prod

%description vmutils
Package for vmagent-prod  vmalert-prod  vmauth-prod  vmbackup-prod  vmctl-prod  vmrestore-prod

%files vmutils
%{_bindir}/vmagent-prod
%dir %attr(0775, victoriametrics, victoriametrics) /var/lib/vmagent-remotewrite-data
%{_bindir}/vmalert-prod
%{_bindir}/vmauth-prod
%{_bindir}/vmbackup-prod
%{_bindir}/vmctl-prod
%{_bindir}/vmrestore-prod
%dir %attr(0775, victoriametrics, victoriametrics) /etc/victoriametrics/vmagent
%dir %attr(0775, victoriametrics, victoriametrics) /etc/victoriametrics/vmalert
%dir %attr(0775, victoriametrics, victoriametrics) /etc/victoriametrics/vmauth
/etc/victoriametrics/vmagent/vmagent.conf
/etc/victoriametrics/vmagent/prometheus.yml
/etc/victoriametrics/vmalert/vmalert.conf
/etc/victoriametrics/vmalert/alerts.yml
/etc/victoriametrics/vmauth/vmauth.conf
/etc/victoriametrics/vmauth/config.yml
%if %{use_systemd}
%{_unitdir}/vmagent.service
%{_unitdir}/vmalert.service
%{_unitdir}/vmauth.service
%endif

%package cluster
Summary: Package for vminsert-prod vmselect-prod vmstorage-prod

%description cluster
Package for vminsert-prod vmselect-prod vmstorage-prod

%files cluster
%{_bindir}/vminsert-prod
%{_bindir}/vmselect-prod
%{_bindir}/vmstorage-prod
