Name:    vmctl
Version: 1.83.0
Release: 1
Summary: VictoriaMetrics command-line tool

Group:   Development Tools
License: ASL 2.0
URL: https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/v%{version}/vmutils-linux-amd64-v%{version}.tar.gz

Source0: LICENSE
Requires(pre): /usr/sbin/useradd, /usr/bin/getent, /usr/bin/echo, /usr/bin/chown
Requires(postun): /usr/sbin/userdel

%description
VictoriaMetrics command-line tool

%prep
curl -L %{url} > vmutils.tar.gz
tar -zxf vmutils.tar.gz

%install
%{__install} -m 0755 -d %{buildroot}%{_bindir}
cp vmctl-prod %{buildroot}%{_bindir}/vmctl-prod

%pre
/usr/bin/getent group victoriametrics > /dev/null || /usr/sbin/groupadd -r victoriametrics
/usr/bin/getent passwd victoriametrics > /dev/null || /usr/sbin/useradd -r -m -d /home/victoriametrics -s /bin/bash -g victoriametrics victoriametrics

%files
%{_bindir}/vmctl-prod
