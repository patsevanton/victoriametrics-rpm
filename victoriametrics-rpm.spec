%global _prefix /usr/local

Name:    victoriametrics
Version: 1.15.2
Release: 1
Summary: The best long-term remote storage for Prometheus

Group:   Development Tools
License: ASL 2.0
URL: https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/v%{version}/victoria-metrics-v%{version}.tar.gz

%description
VictoriaMetrics - the best long-term remote storage for Prometheus

%prep
curl -L %{url} > victoria-metrics.tar.gz
tar -zxf victoria-metrics.tar.gz

%install
%{__install} -m 0755 -d %{buildroot}%{_bindir}
cp victoria-metrics-prod %{buildroot}%{_bindir}/%{name}

%files
%{_bindir}/%{name}
