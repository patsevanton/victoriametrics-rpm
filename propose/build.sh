#!/bin/bash

list_dependencies=(rpm-build rpmdevtools)

for i in ${list_dependencies[*]}
do
    if ! rpm -qa | grep -qw $i; then
        echo "__________Dont installed '$i'__________"
        #yum -y install $i
    fi
done

rm -rf {RPMS,SRPMS,BUILD,SOURCES,SPECS}
mkdir {RPMS,SRPMS,BUILD,SOURCES,SPECS}

cp victoriametrics.* SOURCES

rpmbuild -bb --define "_topdir $PWD" victoriametrics-rpm.spec
