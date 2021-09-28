# victoriametrics-rpm
RPM for VictoriaMetrics - the best long-term remote storage for Prometheus

[![Copr build status](https://copr.fedorainfracloud.org/coprs/antonpatsev/VictoriaMetrics/package/victoriametrics/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/antonpatsev/VictoriaMetrics/package/victoriametrics/)

Before install disable Selinux. Info https://github.com/patsevanton/victoriametrics-rpm/issues/10

## Installation with yum
Support CentOS 6, CentOS 7, Oraclelinux 7

```
sudo yum -y install yum-plugin-copr

sudo yum -y copr enable antonpatsev/VictoriaMetrics

sudo yum makecache

sudo yum -y install victoriametrics

sudo systemctl start victoriametrics

sudo yum -y install vmagent

sudo yum -y install vmalert

sudo yum -y install vmauth

sudo yum -y install vmbackup

sudo yum -y install vmrestore

sudo yum -y install vmctl
```

## Installation with dnf
Support CentOS 8, CentOS-stream 8, CentOS-stream 9, Oraclelinux 8, Fedora 33,34,35

```
sudo dnf -y install yum-plugin-copr

sudo dnf -y copr enable antonpatsev/VictoriaMetrics

sudo dnf makecache

sudo dnf -y install victoriametrics

sudo systemctl start victoriametrics

sudo dnf -y install vmagent

sudo dnf -y install vmalert

sudo dnf -y install vmauth

sudo dnf -y install vmbackup

sudo dnf -y install vmrestore

sudo dnf -y install vmctl
```
