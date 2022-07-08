Name:    vmbackup
Version: 1.78.1
Release: 1
Summary: vmbackup creates VictoriaMetrics data backups from instant snapshots.

Group:   Development Tools
License: ASL 2.0
URL: https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/v%{version}/vmutils-amd64-v%{version}.tar.gz

Source0: LICENSE
Requires(pre): /usr/sbin/useradd, /usr/bin/getent, /usr/bin/echo, /usr/bin/chown
Requires(postun): /usr/sbin/userdel

%description
vmbackup creates VictoriaMetrics data backups from instant snapshots.

%prep
curl -L %{url} > vmutils.tar.gz
tar -zxf vmutils.tar.gz

%install
%{__install} -m 0755 -d %{buildroot}%{_bindir}
cp vmbackup-prod %{buildroot}%{_bindir}/vmbackup-prod

%pre
/usr/bin/getent group victoriametrics > /dev/null || /usr/sbin/groupadd -r victoriametrics
/usr/bin/getent passwd victoriametrics > /dev/null || /usr/sbin/useradd -r -m -d /home/victoriametrics -s /bin/bash -g victoriametrics victoriametrics

%files
%{_bindir}/vmbackup-prod
