# victoriametrics-rpm
RPM for VictoriaMetrics - the best long-term remote storage for Prometheus

[![Copr build status](https://copr.fedorainfracloud.org/coprs/antonpatsev/VictoriaMetrics/package/victoriametrics/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/antonpatsev/VictoriaMetrics/package/victoriametrics/)

## Installation with yum

```
yum -y install yum-plugin-copr

yum copr enable antonpatsev/VictoriaMetrics

yum makecache

yum -y install victoriametrics

systemctl start victoriametrics
```

## Installation with dnf

```
dnf -y install yum-plugin-copr

dnf copr enable antonpatsev/VictoriaMetrics

dnf makecache

dnf -y install victoriametrics

systemctl start victoriametrics
```

