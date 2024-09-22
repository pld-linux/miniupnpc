#
# Conditional build:
%bcond_without	python2	# CPython 2.x module
%bcond_without	python3	# CPython 3.x module

Summary:	MiniUPnP client and a library
Summary(pl.UTF-8):	Program i biblioteka kliencka MiniUPnP
Name:		miniupnpc
Version:	2.2.8
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://miniupnp.tuxfamily.org/files/%{name}-%{version}.tar.gz
# Source0-md5:	e0ef02aecfa0de558c6f4579b6c5205c
URL:		http://miniupnp.tuxfamily.org/
%if %{with python2}
BuildRequires:	python-devel >= 1:2.5
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-setuptools
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MiniUPnP client and a library.

%description -l pl.UTF-8
Program i biblioteka kliencka MiniUPnP.

%package devel
Summary:	Header files for miniupnpc library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki miniupnpc
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for miniupnpc library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki miniupnpc.

%package static
Summary:	Static miniupnpc library
Summary(pl.UTF-8):	Statyczna biblioteka miniupnpc
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static miniupnpc library.

%description static -l pl.UTF-8
Statyczna biblioteka miniupnpc.

%package -n python-miniupnpc
Summary:	Python 2 binding for miniupnpc library
Summary(pl.UTF-8):	Wiązanie Pythona 2 do biblioteki miniupnpc
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-libs

%description -n python-miniupnpc
Python 2 binding for miniupnpc library.

%description -n python-miniupnpc -l pl.UTF-8
Wiązanie Pythona 2 do biblioteki miniupnpc.

%package -n python3-miniupnpc
Summary:	Python 3 binding for miniupnpc library
Summary(pl.UTF-8):	Wiązanie Pythona 3 do biblioteki miniupnpc
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python3-libs >= 1:3.2

%description -n python3-miniupnpc
Python 3 binding for miniupnpc library.

%description -n python3-miniupnpc -l pl.UTF-8
Wiązanie Pythona 3 do biblioteki miniupnpc.

%prep
%setup -q

%build
# there is also cmake support, but also not up to date (see cmake patch in Fedora)'
CFLAGS="%{rpmcflags}" \
CPPFLAGS="%{rpmcppflags}" \
LDFLAGS="%{rpmldflags}" \
%{__make} \
	CC="%{__cc}" \
	LIBDIR=%{_lib}

%if %{with python2}
%py_build
%endif

%if %{with python3}
%py3_build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	LIBDIR=%{_lib}

%if %{with python2}
%py_install
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc Changelog.txt LICENSE README apiversions.txt
%attr(755,root,root) %{_bindir}/external-ip
%attr(755,root,root) %{_bindir}/upnp-listdevices
%attr(755,root,root) %{_bindir}/upnpc
%attr(755,root,root) %{_libdir}/libminiupnpc.so.18

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libminiupnpc.so
%{_includedir}/miniupnpc
%{_pkgconfigdir}/miniupnpc.pc
%{_mandir}/man3/miniupnpc.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libminiupnpc.a

%if %{with python2}
%files -n python-miniupnpc
%defattr(644,root,root,755)
%doc pymoduletest.py testupnpigd.py
%attr(755,root,root) %{py_sitedir}/miniupnpc.so
%{py_sitedir}/miniupnpc-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-miniupnpc
%defattr(644,root,root,755)
%doc pymoduletest.py testupnpigd.py
%attr(755,root,root) %{py3_sitedir}/miniupnpc.cpython-*.so
%{py3_sitedir}/miniupnpc-%{version}-py*.egg-info
%endif
