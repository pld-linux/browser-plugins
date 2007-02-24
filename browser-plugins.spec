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
Summary(pl.UTF-8):	Podstawowy pakiet dla wtyczek przeglądarek WWW
Name:		browser-plugins
Version:	2.0
Release:	2
License:	GPL
Group:		Base
BuildRequires:	rpmbuild(macros) >= 1.356
Source0:	%{name}.README
Source1:	%{name}-update.sh
Requires:	filesystem >= 2.0-1.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	%{_browserpluginsconfdir}

%description
This package provides base directory for browser plugins complying to
Netscape Plugin API (NPAPI).

Browsers known to support NPAPI:
- Netscape Communicator/Navigator
- Mozilla/Mozilla Firefox/Seamonkey
- Opera
- Konqueror

%description -l pl.UTF-8
Ten pakiet dostarcza podstawowy katalog dla wtyczek przeglądarek
zgodnych z Netscape Plugin API (NPAPI).

Przeglądarki obsługujące NPAPI to:
- Netscape Communicator/Navigator
- Mozilla/Mozilla Firefox/Seamonkey
- Opera
- Konqueror

%prep
%setup -qcT
cp -a %{SOURCE0} README
cp -a %{SOURCE1} update-browser-plugins

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/{blacklist,browsers}.d,%{_sbindir}}
install update-browser-plugins $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_browser_plugins

# we don't need postin script as all browsers depend on this package and
# therefore this package should be last one to go from system.

%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}
%dir %{_sysconfdir}/browsers.d
%dir %{_sysconfdir}/blacklist.d
%attr(755,root,root) %{_sbindir}/update-browser-plugins
