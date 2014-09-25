%define release_name Rawhide
%define dist_version 2
%define bug_version Rawhide

Summary:        IprediaOS release files
Name:           iprediaos-release
Version:        2
Release:        0.5
License:        MIT
Group:          System Environment/Base
URL:            http://ipredia.org
Source:         %{name}-%{version}.tar.bz2
Obsoletes:      redhat-release
Provides:       redhat-release
Provides:       system-release
Provides:       system-release(%{version})
Requires:       iprediaos-repos(%{version})
BuildArch:      noarch

%description
IprediaOS release files such as various /etc/ files that define the release.

%package standard
Summary:        Base package for non-product-specific default configurations
Provides:       system-release-standard
Provides:       system-release-standard(%{version})
Requires:       iprediaos-release = %{version}-%{release}
Conflicts:      iprediaos-release-cloud
Conflicts:      iprediaos-release-server
Conflicts:      iprediaos-release-workstation

%description standard
Provides a base package for non-product-specific configuration files to
depend on.

%package cloud
Summary:        Base package for IprediaOS Cloud-specific default configurations
Provides:       system-release-cloud
Provides:       system-release-cloud(%{version})
Requires:       iprediaos-release = %{version}-%{release}
Conflicts:      iprediaos-release-server
Conflicts:      iprediaos-release-standard
Conflicts:      iprediaos-release-workstation

%description cloud
Provides a base package for IprediaOS Cloud-specific configuration files to
depend on.

%package server
Summary:        Base package for IprediaOS Server-specific default configurations
Provides:       system-release-server
Provides:       system-release-server(%{version})
Requires:       iprediaos-release = %{version}-%{release}
Requires:       systemd
Requires:       cockpit
Requires:       rolekit
Requires(post):	sed
Requires(post):	systemd
Conflicts:      iprediaos-release-cloud
Conflicts:      iprediaos-release-standard
Conflicts:      iprediaos-release-workstation

%description server
Provides a base package for IprediaOS Server-specific configuration files to
depend on.

%package workstation
Summary:        Base package for IprediaOS Workstation-specific default configurations
Provides:       system-release-workstation
Provides:       system-release-workstation(%{version})
Requires:       iprediaos-release = %{version}-%{release}
Conflicts:      iprediaos-release-cloud
Conflicts:      iprediaos-release-server
Conflicts:      iprediaos-release-standard

%description workstation
Provides a base package for IprediaOS Workstation-specific configuration files to
depend on.

%prep
%setup -q
sed -i 's|@@VERSION@@|%{dist_version}|g' IprediaOS-Legal-README.txt

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc
echo "IprediaOS release %{version} (%{release_name})" > $RPM_BUILD_ROOT/etc/iprediaos-release
echo "cpe:/o:ipredia:iprediaos:%{version}" > $RPM_BUILD_ROOT/etc/system-release-cpe
cp -p $RPM_BUILD_ROOT/etc/iprediaos-release $RPM_BUILD_ROOT/etc/issue
echo "Kernel \r on an \m (\l)" >> $RPM_BUILD_ROOT/etc/issue
cp -p $RPM_BUILD_ROOT/etc/issue $RPM_BUILD_ROOT/etc/issue.net
echo >> $RPM_BUILD_ROOT/etc/issue
ln -s iprediaos-release $RPM_BUILD_ROOT/etc/redhat-release
ln -s iprediaos-release $RPM_BUILD_ROOT/etc/system-release

cat << EOF >>$RPM_BUILD_ROOT/etc/os-release
NAME=IprediaOS
VERSION="%{dist_version} (%{release_name})"
ID=iprediaos
VERSION_ID=%{dist_version}
PRETTY_NAME="IprediaOS %{dist_version} (%{release_name})"
ANSI_COLOR="0;34"
CPE_NAME="cpe:/o:ipredia:iprediaos:%{dist_version}"
HOME_URL="http://ipredia.org/"
BUG_REPORT_URL="http://bugzilla.ipredia.org/"
IPREDIA_BUGZILLA_PRODUCT="IprediaOS"
IPREDIA_BUGZILLA_PRODUCT_VERSION=%{bug_version}
IPREDIA_SUPPORT_PRODUCT="IprediaOS"
IPREDIA_SUPPORT_PRODUCT_VERSION=%{bug_version}
EOF

# Set up the dist tag macros
install -d -m 755 $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d
cat >> $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d/macros.dist << EOF
# dist macros.

%%ipredia                %{dist_version}
%%dist                .ipos%{dist_version}
%%ipos%{dist_version}                1
EOF

# Add Product-specific presets
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system-preset/
# IprediaOS Server
install -m 0644 80-server.preset %{buildroot}%{_prefix}/lib/systemd/system-preset/

%post server
if [ $1 -eq 1 ] ; then
        # Initial installation; fix up after %%systemd_post in packages
	# possibly installed before our preset file was added
	units=$(sed -n 's/^enable//p' \
		< %{_prefix}/lib/systemd/system-preset/80-server.preset)
        /usr/bin/systemctl preset $units >/dev/null 2>&1 || :
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE IprediaOS-Legal-README.txt
%config %attr(0644,root,root) /etc/os-release
%config %attr(0644,root,root) /etc/iprediaos-release
/etc/redhat-release
/etc/system-release
%config %attr(0644,root,root) /etc/system-release-cpe
%config(noreplace) %attr(0644,root,root) /etc/issue
%config(noreplace) %attr(0644,root,root) /etc/issue.net
%attr(0644,root,root) %{_rpmconfigdir}/macros.d/macros.dist

%files standard
%{!?_licensedir:%global license %%doc}
%license LICENSE

%files cloud
%{!?_licensedir:%global license %%doc}
%license LICENSE

%files server
%{!?_licensedir:%global license %%doc}
%license LICENSE
%{_prefix}/lib/systemd/system-preset/80-server.preset

%files workstation
%{!?_licensedir:%global license %%doc}
%license LICENSE

%changelog
* Fre Jun 25 2014 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 2-0.5
- Update for IprediaOS 2 Rawhide.

* Mon Jun 18 2012 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 1-1
- rebrand for iprediaos
