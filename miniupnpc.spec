Summary:	MiniUPnP client and a library
Name:		miniupnpc
Version:	1.5
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://miniupnp.tuxfamily.org/files/%{name}-%{version}.tar.gz
# Source0-md5:	0efa7498d27c82a56a0300b0c05c4f58
URL:		http://miniupnp.tuxfamily.org/
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MiniUPnP client and a library

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
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-miniupnpc
Python binding for miniupnpc library.

%prep
%setup -q

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -fPIC -Wall -DNDEBUG"

export CFLAGS="%{rpmcflags}"
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mandir}/man3
%{__make} install \
	INSTALLPREFIX=$RPM_BUILD_ROOT%{_prefix} \
	INSTALLDIRLIB=$RPM_BUILD_ROOT%{_libdir}

# let SONAME be the symlink
mv $RPM_BUILD_ROOT%{_libdir}/libminiupnpc.so.{5,5.0.0}
/sbin/ldconfig -n $RPM_BUILD_ROOT%{_libdir}

cp -a man3/miniupnpc.3 $RPM_BUILD_ROOT%{_mandir}/man3

%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc Changelog.txt README LICENSE
%attr(755,root,root) %{_bindir}/upnpc
%attr(755,root,root) %{_bindir}/external-ip
%attr(755,root,root) %{_libdir}/libminiupnpc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libminiupnpc.so.5

%files devel
%defattr(644,root,root,755)
%doc upnpc.c
%{_libdir}/libminiupnpc.so
%{_includedir}/miniupnpc
%{_mandir}/man3/miniupnpc.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libminiupnpc.a

%files -n python-miniupnpc
%defattr(644,root,root,755)
%doc pymoduletest.py testupnpigd.py
%{py_sitedir}/miniupnpc.so
%if "%{py_ver}" > "2.4"
%{py_sitedir}/miniupnpc-*.egg-info
%endif
