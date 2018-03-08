%global gitdate 20180307
%global commit0 7593095967896d6df68b607126c029d1afd8fee0
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}

Summary:        GStreamer 1.0 streaming media framework "ugly" plug-ins
Name:           gstreamer1-plugins-ugly
Version:        1.13.90
Release:        7%{?gver}%{dist}
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
BuildRequires:	mpg123-devel
BuildRequires:	check-devel
BuildRequires:	git
BuildRequires:	autoconf-archive
BuildRequires:	intltool
BuildRequires:	libtool
Recommends:	gstreamer1-plugins-ugly-free >= %{version}

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
Provides: gstreamer1-plugins-ugly-free-devel >= %{version}
BuildArch: noarch

%description devel-docs
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains the development documentation for the plug-ins that can't
be shipped in gstreamer-plugins-good because:
- the license is not LGPL
- the license of the library is not LGPL
- there are possible licensing issues with the code.


%package -n gstreamer1-plugins-ugly-free
Summary: GStreamer streaming media framework "ugly" plugins
Group: Applications/Multimedia
Obsoletes: gstreamer1-plugin-mpg123 
Obsoletes: gstreamer1-plugin-a52dec

%description -n gstreamer1-plugins-ugly-free
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains plug-ins whose license is not fully compatible with LGPL.


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
    --enable-silent-rules \
    --enable-mpg123

make %{?_smp_mflags} V=0

%install
%make_install
%find_lang gst-plugins-ugly-1.0
rm $RPM_BUILD_ROOT%{_libdir}/gstreamer-1.0/*.la

# Register as an AppStream component to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/gstreamer-ugly-free.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2013 Richard Hughes <richard@hughsie.com> -->
<component type="codec">
  <id>gstreamer-ugly-free</id>
  <metadata_license>CC0-1.0</metadata_license>
  <name>GStreamer Multimedia Codecs - Extra</name>
  <summary>Multimedia playback for CD, DVD, and MP3</summary>
  <description>
    <p>
      This addon includes several additional codecs that have good quality and
      correct functionality, but whose license is not fully compatible with LGPL.
    </p>
    <p>
      These codecs can be used to encode and decode media files where the
      format is not patent encumbered.
    </p>
    <p>
      A codec decodes audio and video for for playback or editing and is also
      used for transmission or storage.
      Different codecs are used in video-conferencing, streaming media and
      video editing applications.
    </p>
  </description>
  <keywords>
    <keyword>CD</keyword>
    <keyword>DVD</keyword>
    <keyword>MP3</keyword>
  </keywords>
  <url type="homepage">http://gstreamer.freedesktop.org/</url>
  <url type="bugtracker">https://bugzilla.gnome.org/enter_bug.cgi?product=GStreamer</url>
  <url type="help">http://gstreamer.freedesktop.org/documentation/</url>
  <url type="donation">http://www.gnome.org/friends/</url>
  <update_contact><!-- upstream-contact_at_email.com --></update_contact>
</component>
EOF


%files 
%doc AUTHORS README REQUIREMENTS COPYING
%{_datadir}/gstreamer-1.0
# Plugins without external dependencies
%{_libdir}/gstreamer-1.0/libgstasf.so
%{_libdir}/gstreamer-1.0/libgstdvdlpcmdec.so
%{_libdir}/gstreamer-1.0/libgstdvdsub.so
# %{_libdir}/gstreamer-1.0/libgstrmdemux.so
# Plugins with external dependencies
%{_libdir}/gstreamer-1.0/libgstamrnb.so
%{_libdir}/gstreamer-1.0/libgstamrwbdec.so
# %{_libdir}/gstreamer-1.0/libgstmad.so
%{_libdir}/gstreamer-1.0/libgstmpeg2dec.so
%{_libdir}/gstreamer-1.0/libgstx264.so
%{_libdir}/gstreamer-1.0/libgstrealmedia.so

%files devel-docs
# Take the dir and everything below it for proper dir ownership
%doc %{_datadir}/gtk-doc

%files -n gstreamer1-plugins-ugly-free -f gst-plugins-ugly-1.0.lang
%{_datadir}/appdata/gstreamer-ugly-free.appdata.xml
# Plugins without external dependencies
%{_libdir}/gstreamer-1.0/libgstxingmux.so
# Plugins with external dependencies
%{_libdir}/gstreamer-1.0/libgstcdio.so
%{_libdir}/gstreamer-1.0/libgstdvdread.so
%{_libdir}/gstreamer-1.0/libgstlame.so
%{_libdir}/gstreamer-1.0/libgstmpg123.so
%{_libdir}/gstreamer-1.0/libgsta52dec.so
%{_libdir}/gstreamer-1.0/libgsttwolame.so

%changelog

* Wed Mar 07 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.13.90-7.git7593095 
- Updated to 1.13.90-7.git7593095

* Sun Jan 21 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.12.4-8.git46fab99
- Twolame plugins now in gstreamer1-plugins-ugly-free

* Fri Dec 08 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.12.4-7.git46fab99 
- Updated to 1.12.4-7.git46fab99 

* Sat Sep 30 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.12.3-8.gitffbf076  
- Automatic Mass Rebuild

* Tue Sep 26 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 1.12.3-7-gitffbf076
- Rebuilt for mpg123

* Mon Sep 18 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 1.12.3-6-gitffbf076
- Updated to 1.12.3-6-gitffbf076

* Mon Sep 18 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 1.12.2-7.git2ac3776
- Rebuilt for mpg123

* Thu Jul 20 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 1.12.2-5.git2ac3776
- Updated to 1.12.2-5.git2ac3776

* Sat Jun 24 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 1.12.1-5.git53e1450
- Updated to 1.12.1-5.git53e1450

* Thu May 25 2017 David Vásquez <davidva AT tutanota DOT com> 1.12.0-5
- Mitigation of https://bugzilla.redhat.com/show_bug.cgi?id=1449884

* Thu May 25 2017 David Vásquez <davidva AT tutanota DOT com> 1.12.0-2
- Updated to 1.12.0-2

* Sat Apr 29 2017 David Vásquez <davidva AT tutanota DOT com> 1.11.91-2.gitcbcf4a3
- Updated to 1.11.91-2.gitcbcf4a3

* Thu Apr 20 2017 David Vásquez <davidva AT tutanota DOT com> 1.11.90-2
- Updated to 1.11.90-2

* Tue Mar 28 2017 David Vásquez <davidva AT tutanota DOT com> 1.11.2-3.20170224git1f13399
- Compatibility for new changes in a52dec

* Sun Mar 05 2017 David Vásquez <davidva AT tutanota DOT com> 1.11.2-2.20170224git1f13399
- Changed "build requires" to new name of mpg123-devel

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
