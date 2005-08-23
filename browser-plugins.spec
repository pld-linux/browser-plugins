# TODO
# - convert all plugin packages to store their plugins in this base
#   directory.
Summary:	Base package for web browser plugins
Summary(pl):	Podstawowy pakiet dla wtyczek przegl±darek WWW
Name:		browser-plugins
Version:	1.0
Release:	1.1
License:	GPL
Group:		Base
URL:		http://www.mozilla.org/projects/plugins/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides base directory for browser plugins complying to
Netscape Plugin API (NPAPI).

Browsers known to support NPAPI:
- Netscape Communicator/Navigator
- Mozilla/Mozilla Firefox
- Opera
- Konqueror

%description -l pl
Ten pakiet dostarcza podstawowy katalog dla wtyczek przegl±darek
zgodnych z Netscape Plugin API (NPAPI).

Przegl±darki obs³uguj±ce NPAPI to:
- Netscape Communicator/Navigator
- Mozilla/Mozilla Firefox
- Opera
- Konqueror

%prep

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/browser-plugins

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_libdir}/browser-plugins
