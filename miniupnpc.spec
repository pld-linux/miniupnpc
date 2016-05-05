Summary:	MiniUPnP client and a library
Summary(pl.UTF-8):	Program i biblioteka kliencka MiniUPnP
Name:		miniupnpc
Version:	1.7
Release:	4
License:	BSD
Group:		Libraries
Source0:	http://miniupnp.tuxfamily.org/files/%{name}-%{version}.tar.gz
# Source0-md5:	297bee441b56af87c6622fc4002179fd
URL:		http://miniupnp.tuxfamily.org/
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
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
Summary:	Python binding for miniupnpc library
Summary(pl.UTF-8):	Wiązanie Pythona do biblioteki miniupnpc
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-miniupnpc
Python binding for miniupnpc library.

%description -n python-miniupnpc -l pl.UTF-8
Wiązanie Pythona do biblioteki miniupnpc.

%prep
%setup -q

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -fPIC -Wall -DNDEBUG -DMINIUPNPC_SET_SOCKET_TIMEOUT -D_BSD_SOURCE -D_POSIX_C_SOURCE=1"

export CFLAGS="%{rpmcflags}"
%py_build

%install
rm -rf $RPM_BUILD_ROOT
#install -d $RPM_BUILD_ROOT%{_mandir}/man3

%{__make} install \
	INSTALLPREFIX=$RPM_BUILD_ROOT%{_prefix} \
	INSTALLDIRLIB=$RPM_BUILD_ROOT%{_libdir}

# let SONAME be the symlink
mv $RPM_BUILD_ROOT%{_libdir}/libminiupnpc.so.{8,8.0.0}
/sbin/ldconfig -n $RPM_BUILD_ROOT%{_libdir}

#cp -a man3/miniupnpc.3 $RPM_BUILD_ROOT%{_mandir}/man3

%py_install

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc Changelog.txt README LICENSE
%attr(755,root,root) %{_bindir}/external-ip
%attr(755,root,root) %{_bindir}/upnpc
%attr(755,root,root) %{_libdir}/libminiupnpc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libminiupnpc.so.8

%files devel
%defattr(644,root,root,755)
%doc upnpc.c
%attr(755,root,root) %{_libdir}/libminiupnpc.so
%{_includedir}/miniupnpc
%{_mandir}/man3/miniupnpc.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libminiupnpc.a

%files -n python-miniupnpc
%defattr(644,root,root,755)
%doc pymoduletest.py testupnpigd.py
%attr(755,root,root) %{py_sitedir}/miniupnpc.so
%if "%{py_ver}" > "2.4"
%{py_sitedir}/miniupnpc-*.egg-info
%endif
