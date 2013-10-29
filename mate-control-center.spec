Summary:	MATE Control Center
Name:		mate-control-center
Version:	1.6.1
Release:	5
License:	GPL v2+
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.6/%{name}-%{version}.tar.xz
# Source0-md5:	a5f5b3c6070f3dafacaf68f6d896ef50
Patch0:		%{name}-desktop-update.patch
Patch1:		%{name}-no-about-me.patch
URL:		http://wiki.mate-desktop.org/mate-control-center
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	dbus-glib-devel
BuildRequires:	dconf-devel
BuildRequires:	flex
BuildRequires:	gettext-devel
BuildRequires:	gnome-doc-utils
BuildRequires:	intltool
BuildRequires:	libmatekbd-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	mate-desktop-devel
BuildRequires:	mate-doc-utils
BuildRequires:	mate-file-manager-devel
BuildRequires:	mate-menus-devel
BuildRequires:	mate-panel-devel
BuildRequires:	mate-settings-daemon-devel
BuildRequires:	mate-window-manager-devel
BuildRequires:	xorg-libXxf86misc-devel
BuildRequires:	xorg-libxkbfile-devel
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib-gio-gsettings
Requires(post,postun):	rarian
Requires(post,postun):	shared-mime-info
Requires:	libmatekbd-runtime
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A Configuration tool for easily setting up your MATE environment.

%package libs
Summary:	MATE Control Center gnome-window-settings library
Group:		Development/Libraries

%description libs
This package contains gnome-window-settings library.

%package devel
Summary:	MATE Control Center header files
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

%description devel
MATE Control-Center header files.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

# kill mate-common deps
%{__sed} -i -e '/MATE_COMPILE_WARNINGS.*/d'	\
    -i -e '/MATE_MAINTAINER_MODE_DEFINES/d'	\
    -i -e '/MATE_COMMON_INIT/d'			\
    -i -e '/MATE_DEBUG_CHECK/d' configure.ac

%build
%{__gnome_doc_prepare}
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--disable-schemas-compile	\
	--disable-scrollkeeper		\
	--disable-silent-rules		\
	--disable-static		\
	--disable-update-desktop	\
	--disable-update-mimedb
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/mate-background-properties \
	$RPM_BUILD_ROOT%{_datadir}/mate/wm-properties

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/*.convert
%{__rm} $RPM_BUILD_ROOT%{_desktopdir}/matecc.desktop
%{__rm} $RPM_BUILD_ROOT%{_libdir}/{*,*/*}.la
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,en@shaw}

%find_lang %{name} --with-mate --with-omf --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%scrollkeeper_update_post
%update_mime_database
%update_desktop_database
%update_icon_cache hicolor
%update_gsettings_cache

%postun
%scrollkeeper_update_postun
%update_desktop_database
%update_mime_database
%update_icon_cache hicolor
%update_gsettings_cache

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/mate-appearance-properties
%attr(755,root,root) %{_bindir}/mate-at-properties
%attr(755,root,root) %{_bindir}/mate-control-center
%attr(755,root,root) %{_bindir}/mate-default-applications-properties
%attr(755,root,root) %{_bindir}/mate-display-properties
%attr(755,root,root) %{_bindir}/mate-font-viewer
%attr(755,root,root) %{_bindir}/mate-keybinding-properties
%attr(755,root,root) %{_bindir}/mate-keyboard-properties
%attr(755,root,root) %{_bindir}/mate-mouse-properties
%attr(755,root,root) %{_bindir}/mate-network-properties
%attr(755,root,root) %{_bindir}/mate-thumbnail-font
%attr(755,root,root) %{_bindir}/mate-typing-monitor
%attr(755,root,root) %{_bindir}/mate-window-properties
%attr(755,root,root) %{_sbindir}/mate-display-properties-install-systemwide
%attr(755,root,root) %{_libdir}/window-manager-settings/libmarco.so

%dir %{_datadir}/mate-background-properties
%dir %{_datadir}/mate-control-center
%dir %{_datadir}/mate-control-center/keybindings
%dir %{_datadir}/mate/wm-properties
%dir %{_libdir}/window-manager-settings

%{_datadir}/desktop-directories/matecc.directory
%{_datadir}/mate-control-center/keybindings/*.xml
%{_datadir}/mate-control-center/pixmaps
%{_datadir}/mate-control-center/ui
%{_datadir}/mate/cursor-fonts

%{_datadir}/glib-2.0/schemas/org.mate.*.xml
%{_datadir}/polkit-1/actions/org.mate.randr.policy
%{_datadir}/thumbnailers/mate-font-viewer.thumbnailer

%{_datadir}/mime/packages/*.xml
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/apps/*.png
%{_iconsdir}/hicolor/scalable/apps/*.svg
%{_sysconfdir}/xdg/menus/matecc.menu

%{_mandir}/man1/mate-appearance-properties.1*
%{_mandir}/man1/mate-default-applications-properties.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/lib*.so.?
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/libslab
%{_includedir}/mate-window-settings-2.0
%{_pkgconfigdir}/*.pc

