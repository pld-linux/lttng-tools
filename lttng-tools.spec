Summary:	LTTng Trace Control
Summary(pl.UTF-8):	Sterowanie śledzeniem LTTng
Name:		lttng-tools
Version:	2.10.1
Release:	2
License:	LGPL v2.1+ (library), GPL v2 (tools)
Group:		Libraries
Source0:	http://lttng.org/files/lttng-tools/%{name}-%{version}.tar.bz2
# Source0-md5:	fd80fa64dffd8017fb30836eb30532cc
Patch0:		%{name}-python.patch
Patch1:		x32.patch
URL:		http://lttng.org/
BuildRequires:	asciidoc
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.10
# for builds from git
#BuildRequires:	bison >= 2.4
#BuildRequires:	flex >= 2.5.35
BuildRequires:	kmod-devel
BuildRequires:	libtool >= 2:2.2
BuildRequires:	libuuid-devel
BuildRequires:	libxml2-devel >= 1:2.7.6
BuildRequires:	lttng-ust-devel >= 2.10.0
BuildRequires:	popt-devel >= 1.13
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	swig-python >= 2.0.0
BuildRequires:	userspace-rcu-devel >= 0.8.0
BuildRequires:	xmlto
#BuildRequires:	jdk java-lttng-ust # used for tests only
Requires:	libxml2 >= 1:2.7.6
Requires:	lttng-ust >= 2.10.0
Requires:	popt >= 1.13
Requires:	userspace-rcu >= 0.8.0
Requires:	uname(release) >= 2.6.27
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# non-function symbol rcu_reader_memb
%define		skip_post_check_so	liblttng-ctl.so.*

%description
LTTng Trace Control library and utilities.

%description -l pl.UTF-8
Biblioteka i narzędzia do sterowania śledzeniem LTTng.

%package devel
Summary:	Header files for LTTng control library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki sterującej LTTng
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	kmod-devel
Requires:	libuuid-devel
Requires:	libxml2-devel >= 1:2.7.6
Requires:	popt-devel >= 1.13
Requires:	userspace-rcu-devel >= 0.8.0

%description devel
Header files for LTTng control library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki sterującej LTTng.

%package static
Summary:	Static LTTng control library
Summary(pl.UTF-8):	Statyczna biblioteka sterująca LTTng
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static LTTng control library.

%description static -l pl.UTF-8
Statyczna biblioteka sterująca LTTng.

%package -n python3-lttng
Summary:	Python 3 binding for LTTng
Summary(pl.UTF-8):	Wiązanie Pythona 3 do LTTng
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Obsoletes:	python-lttng < 2.7.0

%description -n python3-lttng
Python 3 binding for LTTng.

%description -n python3-lttng -l pl.UTF-8
Wiązanie Pythona 3 do LTTng.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal} -I config
%{__autoconf}
%{__autoheader}
%{__automake}
# NOTE: DON'T replace /usr/lib* with %{_libdir} in configure options!
%configure \
	am_cv_python_pyexecdir=%{py3_sitedir} \
	am_cv_python_pythondir=%{py3_sitescriptdir} \
	--disable-silent-rules \
	--enable-python-bindings \
	--with-babeltrace-bin=/usr/bin/babeltrace \
%ifnarch x32
	--with-consumerd32-bin=/usr/libx32/lttng/libexec/lttng-consumerd \
	--with-consumerd32-libdir=/usr/libx32 \
%endif
%ifnarch alpha ia64 x32
	--with-consumerd32-bin=/usr/lib/lttng/libexec/lttng-consumerd \
	--with-consumerd32-libdir=/usr/lib \
%endif
%ifarch %{ix86} %{x8664} ppc ppc64 s390 s390x sparc sparcv9 sparc64
	--with-consumerd64-bin=/usr/lib64/lttng/libexec/lttng-consumerd \
	--with-consumerd64-libdir=/usr/lib64 \
%endif
	--with-lttv-gui-bin=/usr/bin/lttv-gui

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# library *.la kept - missing Requires.private

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/_lttng.{la,a}
%py_postclean

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/lttng-tools

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog LICENSE README.md doc/{live-reading-{howto,protocol},quickstart,relayd-architecture,snapshot-howto,streaming-howto}.txt
%attr(755,root,root) %{_bindir}/lttng
%attr(755,root,root) %{_bindir}/lttng-crash
%attr(755,root,root) %{_bindir}/lttng-relayd
%attr(755,root,root) %{_bindir}/lttng-sessiond
%attr(755,root,root) %{_libdir}/liblttng-ctl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblttng-ctl.so.0
%dir %{_libdir}/lttng
%dir %{_libdir}/lttng/libexec
%attr(755,root,root) %{_libdir}/lttng/libexec/lttng-consumerd
%{_datadir}/xml/lttng
%{_mandir}/man1/lttng.1*
%{_mandir}/man1/lttng-add-context.1*
%{_mandir}/man1/lttng-crash.1*
%{_mandir}/man1/lttng-create.1*
%{_mandir}/man1/lttng-destroy.1*
%{_mandir}/man1/lttng-disable-channel.1*
%{_mandir}/man1/lttng-disable-event.1*
%{_mandir}/man1/lttng-enable-channel.1*
%{_mandir}/man1/lttng-enable-event.1*
%{_mandir}/man1/lttng-help.1*
%{_mandir}/man1/lttng-list.1*
%{_mandir}/man1/lttng-load.1*
%{_mandir}/man1/lttng-metadata.1*
%{_mandir}/man1/lttng-regenerate.1*
%{_mandir}/man1/lttng-save.1*
%{_mandir}/man1/lttng-set-session.1*
%{_mandir}/man1/lttng-snapshot.1*
%{_mandir}/man1/lttng-start.1*
%{_mandir}/man1/lttng-status.1*
%{_mandir}/man1/lttng-stop.1*
%{_mandir}/man1/lttng-track.1*
%{_mandir}/man1/lttng-untrack.1*
%{_mandir}/man1/lttng-version.1*
%{_mandir}/man1/lttng-view.1*
%{_mandir}/man8/lttng-relayd.8*
%{_mandir}/man8/lttng-sessiond.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblttng-ctl.so
%{_libdir}/liblttng-ctl.la
%{_includedir}/lttng/action
%{_includedir}/lttng/condition
%{_includedir}/lttng/notification
%{_includedir}/lttng/trigger
%{_includedir}/lttng/channel.h
%{_includedir}/lttng/constant.h
%{_includedir}/lttng/domain.h
%{_includedir}/lttng/endpoint.h
%{_includedir}/lttng/event.h
%{_includedir}/lttng/handle.h
%{_includedir}/lttng/health.h
%{_includedir}/lttng/load.h
%{_includedir}/lttng/lttng.h
%{_includedir}/lttng/lttng-error.h
%{_includedir}/lttng/save.h
%{_includedir}/lttng/session.h
%{_includedir}/lttng/snapshot.h
%{_includedir}/lttng/version.h.tmpl
%{_pkgconfigdir}/lttng-ctl.pc
%{_mandir}/man3/lttng-health-check.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/liblttng-ctl.a

%files -n python3-lttng
%defattr(644,root,root,755)
%doc doc/python-howto.txt
%attr(755,root,root) %{py3_sitedir}/_lttng.so
%{py3_sitescriptdir}/lttng.py
%{py3_sitescriptdir}/__pycache__/lttng.cpython-*.py[co]
