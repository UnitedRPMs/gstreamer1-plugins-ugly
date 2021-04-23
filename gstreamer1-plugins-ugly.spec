%global gitdate 20191204
%global commit0 bb3f9de20025820fb1c913f96e31cf0a27528bcc
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}
%global         majorminor 1.0

Summary:        GStreamer 1.0 streaming media framework "ugly" plug-ins
Name:           gstreamer1-plugins-ugly
Version:        1.18.4
Release:        7%{?gver}%{dist}
License:        LGPLv2+
Group:          Applications/Multimedia
URL:            http://gstreamer.freedesktop.org/
Source0: 	https://github.com/GStreamer/gst-plugins-ugly/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
BuildRequires:  gstreamer1-devel >= %{version}
BuildRequires:  gstreamer1-plugins-base-devel >= %{version}
BuildRequires:  gcc-c++
BuildRequires:  gettext-devel 
BuildRequires:  a52dec-devel >= 0.7.3
BuildRequires:  libdvdread-devel >= 0.9.0
BuildRequires:  lame-devel >= 3.89
BuildRequires:  libid3tag-devel >= 0.15.0
BuildRequires:  libmad-devel >= 0.15.0
BuildRequires:  libmpeg2-devel >= 0.4.0
BuildRequires:  orc-devel >= 0.4.5
BuildRequires:  libcdio-devel >= 0.82
BuildRequires:  twolame-devel
BuildRequires:  x264-devel >= 1:0.161
BuildRequires:  opencore-amr-devel
BuildRequires:	mpg123-devel
BuildRequires:	check-devel
BuildRequires:	git
BuildRequires:	autoconf-archive
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	meson
BuildRequires:	cmake
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
rm -rf common && git clone https://github.com/GStreamer/common.git  

meson build --prefix=/usr --libdir=%{_libdir} --libexecdir=/usr/libexec --bindir=/usr/bin --sbindir=/usr/sbin --includedir=/usr/include --datadir=/usr/share --mandir=/usr/share/man --infodir=/usr/share/info --localedir=/usr/share/locale --sysconfdir=/etc  \
    -D package-name="gst-plugins-bad 1.0 unitedrpms rpm" \
    -D package-origin="https://unitedrpms.github.io" \
    -D doc=disabled -D sidplay=disabled

%meson_build -C build


%install
%meson_install -C build


# Register as an AppStream component to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.

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

%find_lang gst-plugins-ugly-%{majorminor}
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%files 
%doc AUTHORS README REQUIREMENTS COPYING
%{_datadir}/gstreamer-1.0
# Plugins without external dependencies
%{_libdir}/gstreamer-1.0/libgstasf.so
%{_libdir}/gstreamer-1.0/libgstdvdlpcmdec.so
%{_libdir}/gstreamer-1.0/libgstdvdsub.so
# {_libdir}/gstreamer-1.0/libgstrmdemux.so
# Plugins with external dependencies
%{_libdir}/gstreamer-1.0/libgstamrnb.so
%{_libdir}/gstreamer-1.0/libgstamrwbdec.so
# {_libdir}/gstreamer-1.0/libgstmad.so
%{_libdir}/gstreamer-1.0/libgstx264.so
%{_libdir}/gstreamer-1.0/libgstrealmedia.so

%files devel-docs
# Take the dir and everything below it for proper dir ownership
%doc AUTHORS README REQUIREMENTS COPYING

%files -n gstreamer1-plugins-ugly-free -f gst-plugins-ugly-%{majorminor}.lang
%{_datadir}/appdata/gstreamer-ugly-free.appdata.xml
# Plugins without external dependencies
%{_libdir}/gstreamer-1.0/libgstxingmux.so
# Plugins with external dependencies
%{_libdir}/gstreamer-1.0/libgstcdio.so
%{_libdir}/gstreamer-1.0/libgstdvdread.so
#{_libdir}/gstreamer-1.0/libgstlame.so
#{_libdir}/gstreamer-1.0/libgstmpg123.so
%{_libdir}/gstreamer-1.0/libgsta52dec.so
#{_libdir}/gstreamer-1.0/libgsttwolame.so
%{_libdir}/gstreamer-1.0/libgstmpeg2dec.so

%changelog

* Mon Apr 19 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.18.4-7.gitbb3f9de
- Updated to 1.18.4

* Mon Jan 25 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.18.3-7.gitad60e54
- Updated to 1.18.3

* Mon Dec 07 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.18.2-7.git720672e
- Updated 1.18.2

* Mon Nov 23 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.18.1-8.git720672e
- Rebuilt for x264

* Thu Oct 29 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.18.1-7.git720672e
- Updated 1.18.1

* Mon Sep 28 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.18.0-7.gitae91a81
- Updated 1.18.0

* Tue Aug 25 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.17.90-7.gitbb76cbd
- Updated to 1.17.90

* Fri Jul 10 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.17.2-7.gite1e53da
- Updated to 1.17.2

* Sat Jul 04 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.16.2-9.git4b2943e
- Rebuilt for x264

* Fri Feb 28 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.16.2-8.git4b2943e
- Rebuilt

* Wed Dec 04 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.16.2-7.git4b2943e
- Updated to 1.16.2


* Wed Oct 02 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.16.1-7.git34c7d2b
- Updated to 1.16.1

* Thu May 16 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.16.0-8.git6cbac8d
- mpeg2dec changed to gstreamer1-plugins-ugly-free

* Fri Apr 19 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.16.0-7.git6cbac8d
- Updated to 1.16.0-7.git6cbac8d

* Fri Mar 22 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.15.2-8.git19b7446
- Rebuilt for x264

* Wed Feb 27 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.15.2-7.git19b7446
- Updated to 1.15.2-7.git19b7446

* Fri Jan 18 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.15.1-7.git2365d2b
- Updated to 1.15.1-7.git2365d2b

* Wed Oct 03 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.14.4-7.gite1bf2aa
- Updated to 1.14.4-7.gite1bf2aa

* Mon Sep 17 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.14.3-7.gite6e2707
- Updated to 1.14.3-7.gite6e2707

* Fri Jul 20 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.14.2-7.gitdf1bcfa 
- Updated to 1.14.2-7.gitdf1bcfa

* Mon May 21 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.14.1-7.git005effc 
- Updated to 1.14.1-7.git005effc

* Wed Mar 21 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.14.0-7.git3d6b928 
- Updated to 1.14.0-7.git3d6b928

* Fri Mar 16 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.13.91-7.gitf16550f 
- Updated to 1.13.91-7.gitf16550f

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
