# TODO
# - convert all plugin packages to store their plugins in this base
#   directory.
# known NPAPI compatible browsers from PLD CVS:
# - mozilla
# - mozilla-firefox
# - konqueror
# - opera (ix86 only)
# - galeon
# - skipstone
# - kazehakase
# - netscape (trigger on netscape-common)
# - seamonkey
Summary:	Base package for web browser plugins
Summary(pl):	Podstawowy pakiet dla wtyczek przegl±darek WWW
Name:		browser-plugins2
Version:	2.0
Release:	0.7
License:	GPL
Group:		Base
Source0:	browser-plugins.README
Source1:	browser-plugins-update.sh
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/browser-plugins
# temporarily for testing
%define		update_browser_plugins /usr/sbin/update-browser-plugins

%description
This package provides base directory for browser plugins complying to
Netscape Plugin API (NPAPI).

Browsers known to support NPAPI:
- Netscape Communicator/Navigator
- Mozilla/Mozilla Firefox/Seamonkey
- Opera
- Konqueror

%description -l pl
Ten pakiet dostarcza podstawowy katalog dla wtyczek przegl±darek
zgodnych z Netscape Plugin API (NPAPI).

Przegl±darki obs³uguj±ce NPAPI to:
- Netscape Communicator/Navigator
- Mozilla/Mozilla Firefox/Seamonkey
- Opera
- Konqueror

%prep
%setup -qcT
cp -a %{SOURCE0} README
cp -a %{SOURCE1} update-browser-plugins

cat > blacklist.local <<'EOF'
# list your local overrides here
# the format is shell globs at base dir of plugindir
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/{blacklist,browsers}.d,%{_sbindir}}
install update-browser-plugins $RPM_BUILD_ROOT%{_sbindir}
for browser in opera firefox mozilla mozilla-firefox; do
	for arch in i386 x86_64; do
		cp -a blacklist.local $RPM_BUILD_ROOT%{_sysconfdir}/blacklist.d/local.$browser.$arch.blacklist
	done
done

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_browser_plugins

%preun
if [ "$1" = 0 ]; then
	%update_browser_plugins uninstall
fi

%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}
%dir %{_sysconfdir}/browsers.d
%dir %{_sysconfdir}/blacklist.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/blacklist.d/*.blacklist
%attr(755,root,root) %{_sbindir}/update-browser-plugins
