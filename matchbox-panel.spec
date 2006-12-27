#
# Conditional build:
%bcond_with	sn	# startup-notification support
%bcond_without	wifi	# wireless applet
#
Summary:	Matchbox Panel
Summary(pl):	Panel dla ¶rodowiska Matchbox
Name:		matchbox-panel
Version:	0.9.3
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://projects.o-hand.com/matchbox/sources/matchbox-panel/0.9/%{name}-%{version}.tar.bz2
# Source0-md5:	56d1807636f3919e22e51896ab7ccd2e
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-gcc4.patch
URL:		http://projects.o-hand.com/matchbox/
BuildRequires:	gettext-devel
%{?with_wifi:BuildRequires:	libiw-devel}
BuildRequires:	libmatchbox-devel >= 1.6
BuildRequires:	pkgconfig
%{?with_sn:BuildRequires:	startup-notification-devel}
Requires:	libmatchbox >= 1.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Matchbox Panel.

%description -l pl
Panel dla ¶rodowiska Matchbox.

%package wireless
Summary:	Panel based wireless monitor
Summary(pl):	Siedz±cy w panelu monitor sieci bezprzewodowej
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description wireless
Panel based wireless monitor.

%description wireless -l pl
Siedz±cy w panelu monitor sieci bezprzewodowej.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure \
	--enable-acpi-linux \
	--enable-dnotify \
	--enable-nls \
	%{?with_sn:--enable-startup-notification}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# not installed if built with acpi instead of apm
install applets/dotdesktop/mb-applet-battery.desktop $RPM_BUILD_ROOT%{_desktopdir}

mv -f $RPM_BUILD_ROOT%{_datadir}/locale/{es_ES,es}
mv -f $RPM_BUILD_ROOT%{_datadir}/locale/{fi_FI,fi}
mv -f $RPM_BUILD_ROOT%{_datadir}/locale/{fr_FR,fr}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/matchbox-panel
%attr(755,root,root) %{_bindir}/mb-applet-xterm-wrapper.sh
%attr(755,root,root) %{_bindir}/mb-applet-battery
%attr(755,root,root) %{_bindir}/mb-applet-clock
%attr(755,root,root) %{_bindir}/mb-applet-menu-launcher
%attr(755,root,root) %{_bindir}/mb-applet-launcher
%attr(755,root,root) %{_bindir}/mb-applet-system-monitor
%{_desktopdir}/mb-applet-battery.desktop
%{_desktopdir}/mb-applet-clock.desktop
%{_desktopdir}/mb-applet-menu-launcher.desktop
%{_desktopdir}/mb-applet-system-monitor.desktop
%{_desktopdir}/mb-launcher-term.desktop
%{_pixmapsdir}/*.png

%if %{with wifi}
%files wireless
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mb-applet-wireless
%{_desktopdir}/mb-applet-wireless.desktop
%endif
