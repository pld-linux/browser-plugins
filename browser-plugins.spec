# TODO
# - convert all plugin packages to store their plugins in this base
#   directory.
Summary:	Base package for web browser plugins
Summary(pl):	Podstawowy pakiet dla wtyczek przeglądarek WWW
Name:		browser-plugins
Version:	1.0
Release:	2
License:	GPL
Group:		Base
Provides:	%{name}(%{_target_cpu}) = %{version}-%{release}
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
Ten pakiet dostarcza podstawowy katalog dla wtyczek przeglądarek
zgodnych z Netscape Plugin API (NPAPI).

Przeglądarki obsługujące NPAPI to:
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
