#
# Conditional build:
%bcond_without	sn	# startup-notification support
%bcond_without	acpi	# battery applet using ACPI
%bcond_with	apm	# battery applet using APM
#
%if %{with apm}
%undefine	with_acpi
%endif
Summary:	Matchbox Panel
Summary(pl.UTF-8):	Panel dla środowiska Matchbox
Name:		matchbox-panel
Version:	2.0
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://downloads.yoctoproject.org/releases/matchbox/matchbox-panel/2.0/%{name}-%{version}.tar.bz2
# Source0-md5:	87faf3b9299a9d04056904e6f311ec80
Patch0:		%{name}-format.patch
Patch1:		%{name}-no-Werror.patch
Patch2:		%{name}-conflicting.patch
URL:		https://www.yoctoproject.org/software-item/matchbox/
%{?with_apm:BuildRequires:	apmd-devel}
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	dbus-glib-devel
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	gtk+2-devel >= 2:2.6
%{?with_acpi:BuildRequires:	libacpi-devel}
BuildRequires:	pkgconfig
%{?with_sn:BuildRequires:	startup-notification-devel}
Requires:	gtk+2 >= 2:2.6
Obsoletes:	matchbox-panel-wireless < 2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Matchbox Panel.

%description -l pl.UTF-8
Panel dla środowiska Matchbox.

%package devel
Summary:	Header files for Matchbox Panel applets development
Summary(pl.UTF-8):	Pliki nagłówkowe do tworzenia apletów panelu środowiska Matchbox
Group:		X11/Development/Libraries
Requires:	glib2-devel >= 2.0
Requires:	gtk+2-devel >= 2:2.6
# doesn't require base

%description devel
Header files for Matchbox Panel applets development.

%description devel -l pl.UTF-8
Pliki nagłówkowe do tworzenia apletów panelu środowiska Matchbox.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-nls \
	%{?with_sn:--enable-startup-notification} \
%if %{with acpi} || %{with apm}
	--with-battery=%{?with_acpi:acpi}%{?with_apm:apm}
%endif
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/matchbox-panel/*.la

# no translations included in 2.0
#find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
# -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/matchbox-panel
%dir %{_libdir}/matchbox-panel
%attr(755,root,root) %{_libdir}/matchbox-panel/libbattery.so
%attr(755,root,root) %{_libdir}/matchbox-panel/libbrightness.so
%attr(755,root,root) %{_libdir}/matchbox-panel/libclock.so
%attr(755,root,root) %{_libdir}/matchbox-panel/liblauncher.so
%attr(755,root,root) %{_libdir}/matchbox-panel/libnotify.so
%attr(755,root,root) %{_libdir}/matchbox-panel/libshowdesktop.so
%if %{with sn}
%attr(755,root,root) %{_libdir}/matchbox-panel/libstartup.so
%attr(755,root,root) %{_libdir}/matchbox-panel/libstartup-notify.so
%endif
%attr(755,root,root) %{_libdir}/matchbox-panel/libsystray.so
%attr(755,root,root) %{_libdir}/matchbox-panel/libwindowselector.so
%dir %{_datadir}/matchbox-panel
%{_datadir}/matchbox-panel/brightness
%{_datadir}/matchbox-panel/startup

%files devel
%defattr(644,root,root,755)
%{_includedir}/matchbox-panel
%{_pkgconfigdir}/matchbox-panel.pc
