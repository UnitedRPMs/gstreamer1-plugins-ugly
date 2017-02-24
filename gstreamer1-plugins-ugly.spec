%global gitdate 20170224
%global commit0 1f1339913fb88f061899633105ab21745791ca6b
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .%{gitdate}git%{shortcommit0}

Summary:        GStreamer 1.0 streaming media framework "ugly" plug-ins
Name:           gstreamer1-plugins-ugly
Version:        1.11.2
Release:        1%{?gver}%{dist}
License:        LGPLv2+
Group:          Applications/Multimedia
URL:            http://gstreamer.freedesktop.org/
Source0: 	https://github.com/GStreamer/gst-plugins-ugly/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
BuildRequires:  gstreamer1-devel >= %{version}
BuildRequires:  gstreamer1-plugins-base-devel >= %{version}
BuildRequires:  gettext-devel gtk-doc
BuildRequires:  a52dec-devel >= 0.7.3
BuildRequires:  libdvdread-devel >= 0.9.0
BuildRequires:  lame-devel >= 3.89
BuildRequires:  libid3tag-devel >= 0.15.0
BuildRequires:  libmad-devel >= 0.15.0
BuildRequires:  mpeg2dec-devel >= 0.4.0
BuildRequires:  orc-devel >= 0.4.5
BuildRequires:  libcdio-devel >= 0.82
BuildRequires:  twolame-devel
BuildRequires:  x264-devel >= 0.0.0-0.28
BuildRequires:  opencore-amr-devel
BuildRequires:	libmpg123-devel
BuildRequires:	check-devel
BuildRequires:	git
BuildRequires:	autoconf-archive
BuildRequires:	intltool
BuildRequires:	libtool

%description
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains well-written plug-ins that can't be shipped in
gstreamer-plugins-good because:
- the license is not LGPL
- the license of the library is not LGPL
- there are possible licensing issues with the code.


%package devel-docs
Summary: Development documentation for the GStreamer "ugly" plug-ins
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description devel-docs
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains the development documentation for the plug-ins that can't
be shipped in gstreamer-plugins-good because:
- the license is not LGPL
- the license of the library is not LGPL
- there are possible licensing issues with the code.


%prep
%autosetup -n gst-plugins-ugly-%{commit0} 
rm -rf common && git clone git://anongit.freedesktop.org/gstreamer/common  

%build

NOCONFIGURE=1 ./autogen.sh

%if 0%{?fedora} >= 26
CFLAGS="-g -O2 -fstack-protector-strong -Wformat -Werror=format-security -Wall -Wno-error" CXXFLAGS="-g -O2 -fstack-protector-strong -Wformat -Werror=format-security -Wall -Wno-error" CPPFLAGS="-Wdate-time -D_FORTIFY_SOURCE=2" LDFLAGS="-Wl,-z,relro -Wl,-z,defs -Wl,-O1 -Wl,--as-needed"
%endif

%configure --disable-static \
    --with-package-name="gst-plugins-ugly 1.0 rpmfusion rpm" \
    --with-package-origin="http://rpmfusion.org/" \
    --enable-debug \
    --enable-gtk-doc \
    --disable-mpg123
make %{?_smp_mflags}


%install
%make_install
%find_lang gst-plugins-ugly-1.0
rm $RPM_BUILD_ROOT%{_libdir}/gstreamer-1.0/*.la


%files -f gst-plugins-ugly-1.0.lang
%doc AUTHORS README REQUIREMENTS
%license COPYING
%{_datadir}/gstreamer-1.0
# Plugins without external dependencies
%{_libdir}/gstreamer-1.0/libgstasf.so
%{_libdir}/gstreamer-1.0/libgstdvdlpcmdec.so
%{_libdir}/gstreamer-1.0/libgstdvdsub.so
%{_libdir}/gstreamer-1.0/libgstrmdemux.so
%{_libdir}/gstreamer-1.0/libgstxingmux.so
# Plugins with external dependencies
%{_libdir}/gstreamer-1.0/libgsta52dec.so
%{_libdir}/gstreamer-1.0/libgstamrnb.so
%{_libdir}/gstreamer-1.0/libgstamrwbdec.so
%{_libdir}/gstreamer-1.0/libgstcdio.so
%{_libdir}/gstreamer-1.0/libgstdvdread.so
%{_libdir}/gstreamer-1.0/libgstlame.so
# %{_libdir}/gstreamer-1.0/libgstmad.so
%{_libdir}/gstreamer-1.0/libgstmpeg2dec.so
%{_libdir}/gstreamer-1.0/libgsttwolame.so
%{_libdir}/gstreamer-1.0/libgstx264.so

%files devel-docs
# Take the dir and everything below it for proper dir ownership
%doc %{_datadir}/gtk-doc


%changelog

* Fri Feb 24 2017 David Vásquez <davidva AT tutanota DOT com> 1.11.2-1.20170224git1f13399
- Updated to 1.11.2-1.20170224git1f13399

* Fri Jan 27 2017 David Vásquez <davidjeremias82 AT gmail DOT com> 1.11.1-1
- Updated to 1.11.1

* Sat Dec 10 2016 Pavlo Rudyi <paulcarroty@riseup.net> - 1.10.2-1
- Updated to 1.10.2

* Tue Nov 15 2016 Pavlo Rudyi <paulcarroty@riseup.net> - 1.10.0-1
- Updated to 1.10

* Thu Oct 06 2016 David Vásquez <davidjeremias82 AT gmail DOT com> 1.9.2-1
- Updated to 1.9.2

* Fri Jul 08 2016 David Vásquez <davidjeremias82 AT gmail DOT com> 1.9.1-1
- Updated to 1.9.1

* Thu Jun 23 2016 David Vásquez <davidjeremias82 AT gmail DOT com> 1.8.2-1
- Updated to 1.8.2-1

* Sat Apr 23 2016 David Vásquez <davidjeremias82 AT gmail DOT com> 1.8.1-2
- Added -Wno-deprecated-declarations

* Thu Apr 21 2016 David Vásquez <davidjeremias82 AT gmail DOT com> 1.8.1-1
- Updated to 1.8.1

* Sat Jan 23 2016 Hans de Goede <j.w.r.degoede@gmail.com> - 1.6.3-1
- Rebase to new upstream release 1.6.3

* Thu Dec 24 2015 Hans de Goede <j.w.r.degoede@gmail.com> - 1.6.2-1
- Rebase to new upstream release 1.6.2

* Sat Oct 31 2015 Hans de Goede <j.w.r.degoede@gmail.com> - 1.6.1-1
- Rebase to new upstream release 1.6.1

* Sat May 16 2015 Hans de Goede <j.w.r.degoede@gmail.com> - 1.4.5-1
- Rebase to new upstream release 1.4.5

* Wed Oct  1 2014 Hans de Goede <j.w.r.degoede@gmail.com> - 1.4.3-1
- Rebase to new upstream release 1.4.3

* Fri Aug 29 2014 Hans de Goede <j.w.r.degoede@gmail.com> - 1.4.1-1
- Rebase to new upstream release 1.4.1 (rf#3343)

* Sun Jun 15 2014 Hans de Goede <j.w.r.degoede@gmail.com> - 1.2.4-1
- Rebase to new upstream release 1.2.4

* Sat Mar 22 2014 Sérgio Basto <sergio@serjux.com> - 1.2.3-3
- Rebuilt for x264

* Thu Mar 06 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.2.3-2
- Rebuilt for x264

* Sun Feb 23 2014 Hans de Goede <j.w.r.degoede@gmail.com> - 1.2.3-1
- Rebase to new upstream release 1.2.3

* Fri Feb 21 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.2.1-2
- Rebuilt

* Sat Nov 16 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.2.1-1
- Rebase to new upstream release 1.2.1

* Tue Nov 05 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.2.0-3
- Rebuilt for x264/FFmpeg

* Tue Oct 22 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.2.0-2
- Rebuilt for x264

* Sun Oct 13 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.2.0-1
- Rebase to new upstream release 1.2.0

* Thu Aug 08 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.1.3-1
- Rebase to new upstream release 1.1.3

* Wed Aug 07 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.0.9-1
- New upstream release 1.0.9

* Tue May 07 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.0.6-2
- Rebuilt for x264

* Mon Mar 25 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.0.6-1
- New upstream release 1.0.6

* Sat Mar  2 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.0.5-1
- New upstream release 1.0.5
- Drop no longer needed PyXML BuildRequires (rf#2572)

* Sun Jan 20 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.0.2-3
- Rebuilt for FFmpeg/x264

* Fri Nov 23 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.0.2-2
- Rebuilt for x264

* Sun Oct 28 2012 Hans de Goede <j.w.r.degoede@gmail.com> - 1.0.2-1
- New upstream release 1.0.2

* Sun Sep 23 2012 Hans de Goede <j.w.r.degoede@gmail.com> - 0.11.99-1
- New upstream release 0.11.99

* Sun Sep 16 2012 Hans de Goede <j.w.r.degoede@gmail.com> - 0.11.93-2
- Fix gtk-doc dir ownership (rf#2474)

* Sun Sep  9 2012 Hans de Goede <j.w.r.degoede@gmail.com> - 0.11.93-1
- First version of gstreamer1-plugins-ugly for rpmfusion
