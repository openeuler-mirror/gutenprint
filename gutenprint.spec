%bcond_with gimp

Name:          gutenprint
Version:       5.2.14
Release:       6
Summary:       A suite of printer drivers
License:       GPLv2+ and MIT
URL:           http://gimp-print.sourceforge.net/
Source0:       http://downloads.sourceforge.net/gimp-print/%{name}-%{version}.tar.bz2
Source1:       cups-genppdupdate.py.in
Patch0:        gutenprint-menu.patch
Patch1:        gutenprint-O6.patch
Patch2:        gutenprint-postscriptdriver.patch
Patch3:        gutenprint-yyin.patch
Patch4:        gutenprint-manpage.patch
Patch5:        gutenprint-python36syntax.patch

%if %{with gimp}
BuildRequires: pkgconfig(gimpui-2.0), gimp
Requires:      gimp
Provides:      %{name}-plugin%{?_isa} %{name}-plugin
Obsoletes:     %{name}-plugin
%endif

BuildRequires: cups-libs, cups-devel, cups, gettext-devel, pkgconfig, libtiff-devel, libjpeg-devel, libpng-devel
BuildRequires: pkgconfig(libusb-1.0), pkgconfig(gtk+-2.0), chrpath, python3-cups
BuildRequires: autoconf, automake, libtool, python3-devel
Requires:      cups
Provides:      %{name}-doc%{?_isa} %{name}-doc
Obsoletes:     %{name}-doc
Provides:      %{name}-libs%{?_isa} %{name}-libs
Obsoletes:     %{name}-libs
Provides:      %{name}-libs-ui%{?_isa} %{name}-libs-ui
Obsoletes:     %{name}-libs-ui
Provides:      %{name}-extras%{?_isa} %{name}-extras
Obsoletes:     %{name}-extras
Provides:      %{name}-cups%{?_isa} %{name}-cups
Obsoletes:     %{name}-cups

%description
Gutenprint, formerly named Gimp-Print, is a suite of printer drivers that may be used with CUPS,
the Common UNIX Printing System. CUPS is the printing system used by all modern Linux and UNIX systems.
These drivers provide high quality printing for UNIX (including Macintosh OS X 10.2 and later)
and Linux systems that in many cases equal or exceed proprietary vendor-supplied drivers in quality
and functionality, and can be used for demanding printing tasks requiring flexibility and high quality.
This software package include an enhanced Print plugin for the GIMP that replaces the plugin packaged
with the GIMP in addition to the CUPS driver.
Gutenprint has been renamed in order to clearly distinguish it from the GIMP. While this package
started out as the original Print plugin for the GIMP, it has expanded into a collection of general
purpose printer drivers, and the new, enhanced Print plugin for the GIMP is now only a small part of
the package. Furthermore, the name Gutenprint recognizes Johannes Gutenberg, the inventor of the movable
type printing press. Finally, the word guten is the German word for good.
Gutenprint 5.2 incorporates extensive feedback from the beta and release candidate programs.
Gutenprint supports only the printer portion of multi-function devices (devices that typically include
scanning, copying, and fax capabilities).
Gutenprint currently supports over 700 printer models.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}, gtk2-devel

%description devel
This package includes development files for %{name}.

%package        help
Summary:        man files for %{name}
Requires:       man

%description    help
This package includes man files for %{name}.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
cp %{SOURCE1} src/cups/cups-genppdupdate.in
sed -i -e 's,^#!/usr/bin/python3,#!%{__python3},' src/cups/cups-genppdupdate.in
%patch5 -p1

%build
sed -i -e 's,^\(TESTS *=.*\) run-weavetest,\1,' test/Makefile.in

%configure --disable-dependency-tracking --disable-static --enable-samples --enable-escputil --enable-test \
           --disable-rpath --enable-cups-1_2-enhancements --disable-cups-ppds --enable-simplified-cups-ppds

%make_build

%install
%make_install

install -d $RPM_BUILD_ROOT%{_sbindir}

rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/doc
rm -rf $RPM_BUILD_ROOT%{_datadir}/foomatic/kitload.log
rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/5.2/modules/*.la
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/cups/command.types

%find_lang %{name}
sed 's!%{_datadir}/locale/\([^/]*\)/LC_MESSAGES/gutenprint.mo!%{_datadir}/locale/\1/gutenprint_\1.po!g' %{name}.lang >%{name}-po.lang
rm -rf %{name}.lang
%find_lang %{name} --all-name
cat %{name}-po.lang >>%{name}.lang

echo .so man8/cups-genppd.8 > $RPM_BUILD_ROOT%{_mandir}/man8/cups-genppd.5.2.8

chrpath -d $RPM_BUILD_ROOT%{_sbindir}/cups-genppd.5.2
%if %{with gimp}
chrpath -d $RPM_BUILD_ROOT%{_libdir}/gimp/*/plug-ins/*
%endif
chrpath -d $RPM_BUILD_ROOT%{_libdir}/*.so.*
chrpath -d $RPM_BUILD_ROOT%{_cups_serverbin}/driver/*
chrpath -d $RPM_BUILD_ROOT%{_cups_serverbin}/filter/*
chrpath -d $RPM_BUILD_ROOT%{_bindir}/*

%post 
/sbin/ldconfig
/usr/sbin/cups-genppdupdate &>/dev/null || :
/sbin/service cups reload &>/dev/null || :
exit 0

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%license COPYING
%doc AUTHORS NEWS README doc/FAQ.html doc/%{name}-users-manual.odt doc/%{name}-users-manual.pdf
%{_bindir}/escputil
%{_bindir}/testpattern
%{_bindir}/cups-calibrate
%{_sbindir}/cups-genppd*
%{_datadir}/%{name}
%{_datadir}/%{name}/samples/*
%{_datadir}/cups/calibrate.ppm
%{_datadir}/cups/usb/net.sf.gimp-print.usb-quirks
%{_libdir}/%{name}
%{_libdir}/*.so.*
%if %{with gimp}
%{_libdir}/gimp/*/plug-ins/%{name}
%endif
%{_cups_serverbin}/filter/*
%{_cups_serverbin}/driver/*
%{_cups_serverbin}/backend/*

%files devel
%doc doc/developer/reference-html doc/developer/%{name}.pdf doc/%{name}*
%{_includedir}/%{name}*/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%exclude %{_libdir}/*.la

%files help
%{_mandir}/man*/*

%changelog
* Sat Feb 20 2021 lingsheng <lingsheng@huawei.com> - 5.2.14-6
- Disable gimp plugins build

* Thu Nov 26 2020 liuweibo <liuweibo10@hauwei.com> - 5.2.14-5
- Fix install warning

* Sat Nov 30 2019 openEuler Buildteam <buildteam@openeuler.org> - 5.2.14-4
- Package init
