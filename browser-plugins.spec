# TODO
# - convert all plugin packages to store their plugins in this base
#   directory.
# known NPAPI compatible browsers from PLD Linux CVS:
# - galeon
# - kazehakase
# - konqueror
# - mozilla
# - mozilla-firefox
# - mozilla-firefox-bin
# - netscape (trigger on netscape-common)
# - opera (ix86, ppc, sparc* only)
# - seamonkey
# - skipstone
Summary:	Base package for web browser plugins
Summary(pl):	Podstawowy pakiet dla wtyczek przegl±darek WWW
# TODO: to be renamed to actual package name when package is finished
Name:		browser-plugins2
Version:	2.0
Release:	0.11
License:	GPL
Group:		Base
Source0:	browser-plugins.README
Source1:	browser-plugins-update.sh
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/browser-plugins
# TODO: to be moved to rpm-build-macros
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

cat > blacklist <<'EOF'
# The format is shell globs at base dir of plugindir
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/{blacklist,browsers}.d,%{_sbindir}}
install update-browser-plugins $RPM_BUILD_ROOT%{_sbindir}

# TODO: to be moved to browser packages
for browser in opera firefox mozilla mozilla-firefox mozilla-firefox-bin; do
	for arch in i386 x86_64; do
		cp -a blacklist $RPM_BUILD_ROOT%{_sysconfdir}/blacklist.d/$browser.$arch.blacklist
	done
done
cat <<'EOF'>> $RPM_BUILD_ROOT%{_sysconfdir}/blacklist.d/opera.i386.blacklist
# opera has no use of .xpt files.
*.xpt
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%if 0
# TODO: to be enabled if tested enough
%post
%update_browser_plugins
%endif

%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}
%dir %{_sysconfdir}/browsers.d
%dir %{_sysconfdir}/blacklist.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/blacklist.d/*.blacklist
%attr(755,root,root) %{_sbindir}/update-browser-plugins
