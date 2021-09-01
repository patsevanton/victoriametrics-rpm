Name:    victoriametrics
Version: 1.64.1
Release: 4
Summary: The best long-term remote storage for Prometheus

Group:   Development Tools
License: ASL 2.0
URL: https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/v%{version}/victoria-metrics-amd64-v%{version}.tar.gz

Source0: %{name}.service
Source1: victoriametrics.conf
Source2: vmagent/vmagent.conf
Source3: vmagent/prometheus.yml
Source4: vmagent/vmagent.service
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
cp %{SOURCE1} %{buildroot}/etc/default/
cp %{SOURCE2} %{buildroot}/etc/victoriametrics/vmagent/
cp %{SOURCE3} %{buildroot}/etc/victoriametrics/vmagent/
cp victoria-metrics-prod %{buildroot}%{_bindir}/victoria-metrics-prod
%{__install} -m 0755 -d %{buildroot}/var/lib/victoria-metrics-data
%if %{use_systemd}
%{__mkdir} -p %{buildroot}%{_unitdir}
%{__install} -m644 %{SOURCE0} \
    %{buildroot}%{_unitdir}/%{name}.service
%{__install} -m644 %{SOURCE4} \
    %{buildroot}%{_unitdir}/vmagent.service
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
%{_bindir}/vmalert-prod
%{_bindir}/vmauth-prod
%{_bindir}/vmbackup-prod
%{_bindir}/vmctl-prod
%{_bindir}/vmrestore-prod
%dir %attr(0775, victoriametrics, victoriametrics) /etc/victoriametrics/vmagent
%{_bindir}/etc/victoriametrics/vmagent/vmagent.conf
%{_bindir}/etc/victoriametrics/vmagent/prometheus.yml
%if %{use_systemd}
%{_unitdir}/vmagent.service
%endif

%package cluster
Summary: Package for vminsert-prod vmselect-prod vmstorage-prod

%description cluster
Package for vminsert-prod vmselect-prod vmstorage-prod

%files cluster
%{_bindir}/vminsert-prod
%{_bindir}/vmselect-prod
%{_bindir}/vmstorage-prod
