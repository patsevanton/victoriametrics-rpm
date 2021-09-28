Name:    vmrestore
Version: 1.66.1
Release: 1
Summary: vmrestore restores data from backups created by vmbackup. VictoriaMetrics v1.29.0 and newer versions must be used for working with the restored data.

Group:   Development Tools
License: ASL 2.0
URL:     https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/v%{version}/vmutils-amd64-v%{version}.tar.gz

Source0: LICENSE
Requires(pre): /usr/sbin/useradd, /usr/bin/getent, /usr/bin/echo, /usr/bin/chown
Requires(postun): /usr/sbin/userdel

%description
vmrestore restores data from backups created by vmbackup. VictoriaMetrics v1.29.0 and newer versions must be used for working with the restored data.

%prep
curl -L %{url} > vmutils.tar.gz
tar -zxf vmutils.tar.gz

%install
%{__install} -m 0755 -d %{buildroot}%{_bindir}
cp vmrestore-prod %{buildroot}%{_bindir}/vmrestore-prod

%pre
/usr/bin/getent group victoriametrics > /dev/null || /usr/sbin/groupadd -r victoriametrics
/usr/bin/getent passwd victoriametrics > /dev/null || /usr/sbin/useradd -r -m -d /home/victoriametrics -s /bin/bash -g victoriametrics victoriametrics

%files
%{_bindir}/vmrestore-prod
