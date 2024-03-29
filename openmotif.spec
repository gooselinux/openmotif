Summary: Open Motif runtime libraries and executables
Name: openmotif
Version: 2.3.3
Release: 1%{?dist}
License: Open Group Public License
Group: System Environment/Libraries
Source: http://www.motifzone.net/files/public_downloads/openmotif/2.3/%{version}/openmotif-%{version}.tar.gz
Source1: xmbind
URL: http://www.motifzone.net/
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires: /usr/share/X11/XKeysymDB

BuildRequires: automake, libtool, autoconf, flex
BuildRequires: byacc, pkgconfig
BuildRequires: libjpeg-devel libpng-devel
BuildRequires: libXft-devel libXmu-devel libXp-devel libXt-devel libXext-devel
BuildRequires: xorg-x11-xbitmaps
BuildRequires: perl

Patch22: openmotif-2.3.3-no_demos.patch
Patch23: openMotif-2.2.3-uil_lib.patch
Patch43: openMotif-2.3.0-rgbtxt.patch
Patch45: openmotif-2.3.3-mwmrc_dir.patch
Patch46: openmotif-2.3.3-bindings.patch
Patch47: openMotif-2.3.0-no_X11R6.patch
Patch50: openmotif-2.3.3-missing_deps.patch

Conflicts: lesstif <= 0.92.32-6

%description
This is the Open Motif %{version} runtime environment. It includes the
Motif shared libraries, needed to run applications which are dynamically
linked against Motif and the Motif Window Manager "mwm".

%package devel
Summary: Open Motif development libraries and header files
Group: Development/Libraries
Conflicts: lesstif-devel <= 0.92.32-6
Requires: openmotif = %{version}-%{release}
Requires: libjpeg-devel libpng-devel
Requires: libXft-devel libXmu-devel libXp-devel libXt-devel libXext-devel

%description devel
This is the Open Motif %{version} development environment. It includes the
header files and also static libraries necessary to build Motif applications.

%prep
%setup -q
%patch22 -p1 -b .no_demos
%patch23 -p1 -b .uil_lib
%patch43 -p1 -b .rgbtxt
%patch45 -p1 -b .mwmrc_dir
%patch46 -p1 -b .bindings
%patch47 -p1 -b .no_X11R6
%patch50 -p1 -b .missing_deps

%build
aclocal -I .
libtoolize --force --copy
autoconf

CFLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64" \
./configure \
   --libdir=%{_libdir} \
   --enable-static \
   --enable-xft \
   --enable-jpeg \
   --enable-png

make clean %{?_smp_mflags}
make -C include
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

install -d %{buildroot}/etc/X11/xinit/xinitrc.d
install -m 755 %{SOURCE1} %{buildroot}/etc/X11/xinit/xinitrc.d/xmbind.sh

rm -f %{buildroot}%{_libdir}/*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYRIGHT.MOTIF README RELEASE RELNOTES
/etc/X11/xinit/xinitrc.d/xmbind.sh
/etc/X11/mwm/system.mwmrc
%{_bindir}/mwm
%{_bindir}/xmbind
%{_includedir}/X11/bitmaps/*
%{_libdir}/libMrm.so.*
%{_libdir}/libUil.so.*
%{_libdir}/libXm.so.*
%{_datadir}/X11/bindings
%{_mandir}/man1/mwm*
%{_mandir}/man1/xmbind*
%{_mandir}/man4/mwmrc*

%files devel
%defattr(-,root,root)
%{_bindir}/uil
%{_includedir}/Mrm
%{_includedir}/Xm
%{_includedir}/uil
%{_libdir}/lib*.a
%{_libdir}/lib*.so
%{_mandir}/man1/uil.1*
%{_mandir}/man3/*
%{_mandir}/man5/*

%changelog
* Tue Mar 23 2010 Thomas Woerner <twoerner@redhat.com> 2.3.3-1
- new version 2.3.3 (bugfix release)
  see RELNOTES file for the list of the bug fixes

* Fri Feb 26 2010 Thomas Woerner <twoerner@redhat.com> 2.3.2-1.1
- fixes according to review:
- fixed buildroot
- removed dot from summary
- removed dist tag from changelog
- added source download link

* Wed Jan 13 2010 Thomas Woerner <twoerner@redhat.com> 2.3.2-1
- new version 2.3.2 with upstream bug fixes: #1212, #1277, #1473, #1476
- spec file cleanup
- make build work with libtool
- all man pages are utf-8, no need to convert them anymore
- enabled EditRes support with upstream fix
- fixed parallel build
- fixed patches for fuzz 0
  Related: rhbz#543948

* Tue Dec 08 2009 Dennis Gregorovic <dgregor@redhat.com> - 2.3.1-3.1
- Rebuilt for RHEL 6

* Wed Sep 23 2009 Dennis Gregorovic <dgregor@redhat.com> - 2.3.1-3
- update the bindings patch

* Wed Nov 12 2008 Thomas Woerner <twoerner@redhat.com> 2.3.1-2
- more fixes for unreliable pasting into XmTextField (MotifZone bug #1321)
  Resolves: rhbz#405941
- the fix for MotifZone bug #1400 is not working for remote displays

* Thu Oct  2 2008 Thomas Woerner <twoerner@redhat.com> 2.3.1-1
- using final 2.3.1 dist archive

* Wed Sep 17 2008 Thomas Woerner <twoerner@redhat.com> 2.3.1-0
- rebase to 2.3.1 (CVS dist release)
  Resolves: rhbz#455736
- fixes OpenMotif XmList problem
  Resolves: rhbz#405801
- fixes List.c/ReplaceItem() segfaults when item selected
  Resolves: rhbz#431460
- fixes [motifzone 1400 ] openmotif/ BadFont on multiple display application
  Resolves: rhbz#438910
- fixes applications dump core in non-UTF8 environment
  Resolves: rhbz#453722
- fixes lots of additional bugs: see release notes

* Tue Apr  1 2008 Thomas Woerner <twoerner@redhat.com> 2.3.0-0.5
- fixed SEGV error moving mouse over window related to XmToolTipGetLabel
  (MotifZone bug fix #1388)
  Resolves: rhbz#277381

* Thu Nov  8 2007 Thomas Woerner <twoerner@redhat.com> 2.3.0-0.4
- fixed title bar problem using XmNdialogTitle (MotifZone bug fix #1380)
  Resolves: rhbz#353251

* Fri Dec  1 2006 Thomas Woerner <twoerner@redhat.com> 2.3.0-0.3
- fixed path to xmbind in /etc/X11/xinit/xinitrc.d/xmbind.sh
  Resolves: rhbz#218032

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.3.0-0.2.1
- rebuild

* Tue Jun  6 2006 Thomas Woerner <twoerner@redhat.com> 2.3.0-0.2
- new CVS version 2006-06-06
- new buildprereq for pkgconfig

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.3.0-0.1.9.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.3.0-0.1.9.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Feb  2 2006 Thomas Woerner <twoerner@redhat.com> 2.3.0-0.1.9
- new CVS version 2006-02-02
- fixed CVE-2005-3964: libUil buffer overflows (#174814)
- fixed XmList out of bound accesses (#167701)
- fixed pasting into TextField (#179549)

* Tue Jan  3 2006 Jesse Keating <jkeating@redhat.coM> 2.3.0-0.1.2
- Rebuilt on new gcc

* Fri Dec  9 2005 Thomas Woerner <twoerner@redhat.com> 2.3.0-0.1.1
- moved mwmrc to /etc/X11/mwm
- moved bindings to /usr/share/X11
- fixed paths in man pages containing /usr/X11R6

* Thu Dec  8 2005 Thomas Woerner <twoerner@redhat.com> 2.3.0-0.1.1
- enabled Xft, jpeg and png support
- patch for missing xft-config
- dropped duplicate include path in devel package

* Fri Dec  2 2005 Thomas Woerner <twoerner@redhat.com> 2.3.0-0.1
- new 2.3.0 (beta1)
- patch for new rgb.txt location (#174210)
  Thanks to Ville Skyttä for the patch

* Fri Nov 18 2005 Thomas Woerner <twoerner@redhat.com> 2.2.3-15
- moved man pages to /usr/share/man (#173604)

* Wed Nov 16 2005 Jeremy Katz <katzj@redhat.com> - 2.2.3-14
- X11R6 stuff is gone

* Wed Nov 16 2005 Jeremy Katz <katzj@redhat.com> - 2.2.3-13
- also buildrequire xbitmaps

* Wed Nov 16 2005 Thomas Woerner <twoerner@redhat.com> 2.2.3-12
- rebuild for modular X

* Fri Sep  2 2005 Thomas Woerner <twoerner@redhat.com> 2.2.3-11
- fixed mrm initialization error in MrmOpenHierarchyPerDisplay (#167094)
  Thanks to Arjan van de Ven for the patch.

* Mon Apr  4 2005 Thomas Woerner <twoerner@redhat.com> 2.2.3-10
- fixed possible libXpm overflows (#151642)

* Mon Feb 28 2005 Thomas Woerner <twoerner@redhat.com> 2.2.3-9
- Upstream Fix: Multiscreen mode
- Upstream Fix: Crash when restarting by a session manager (motifzone#1193)
- Upstream Fix: Crash when duplicating a window menu containing f.circle_up
  (motifzone#1202)
- fixed divide by zero error in ComputeVizCount() (#144420)
- Xpmcreate: define LONG64 on 64 bit architectures (#143689)

* Mon Nov 29 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-8.1
- allow to write XPM files with absolute path names again (#140815)

* Wed Nov 24 2004 Miloslav Trmac <mitr@redhat.com> 2.2.3-8
- Convert man pages to UTF-8

* Mon Nov 22 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-7
- latest Xpm patches: CAN-2004-0914 (#134631)
- new patch for tmpnam in imake (only used for build)

* Thu Sep 30 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-6
- fixed CAN-2004-0687 (integer overflows) and CAN-2004-0688 (stack overflows)
  in embedded Xpm library

* Wed Sep 29 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-5.2
- replaced libtoolize and autofoo* calls with a patch (autofoo)

* Wed Sep 29 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-5.1
- use new autofoo

* Wed Sep  1 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-5
- libXp now moved to xorg-x11-deprecated-libs, therefore no compatibility 
  with XFree86 packages anymore.

* Mon Aug 30 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-4.3
- devel package: added requires for XFree86-devel (#131202)

* Thu Jun 17 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-4.2
- rebuilt for fc3

* Wed Jun 16 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-4.1
- renamed xmbind script to xmbind.sh (#126116)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  8 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-3
- fixed popup menus fail on Tarantella/VNC (#123027)
- fixed character not supported problem (#124960)
- fixed data out of bounds bug (#124961)

* Wed Apr 14 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-2
- 2.2.3 final version

* Tue Mar 23 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-1.9.2
- final CVS version

* Wed Mar 17 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-1.9.1
- new openmotif 2.2.3 beta version

* Mon Mar  8 2004 Thomas Woerner <twoerner@redhat.com> 2.2.2-17
- fixed popdown problem in ToolTip (#75730)

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 19 2004 Thomas Woerner <twoerner@redhat.com> 2.2.2-16.3
- rebuilt

* Thu Dec 18 2003 Thomas Woerner <twoerner@redhat.com>
- added missing BuildRequires for XFree86-devel

* Thu Nov 27 2003 Thomas Woerner <twoerner@redhat.com> 2.2.2-16.2
- removed rpath

* Mon Aug 27 2003 Thomas Woerner <twoerner@redhat.com> 2.2.2-16
- fixed ToggleBG (#101159)

* Thu Jul 31 2003  <timp@redhat.com> 2.2.2-15.2
- rebuild for RHEL

* Wed Jul 30 2003 Thomas Woerner <twoerner@redhat.com> 2.2.2-15
- fixed ToggleB (#101159)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan 21 2003 Thomas Woerner <twoerner@redhat.com> 2.2.2-13
- fix for Xmu/EditRes conflict (bug #80777)
- fix for wml and utf-8 (bug #80271)
- fix for Ext18List (bug #74502)

* Thu Nov 14 2002 Than Ngo <than@redhat.com> 2.2.2-12.2
- add buildprereq byacc and flex (bug #77860)

* Fri Nov  8 2002 Than Ngo <than@redhat.com> 2.2.2-12.1
- fix some build problem

* Mon Aug 27 2002 Than Ngo <than@redhat.com> 2.2.2-12
- Fixed a segmentation fault in mkcatdefs (bug #71955)

* Wed Jul 24 2002 Than Ngo <than@redhat.com> 2.2.2-11
- Added missing symlinks (bug #69117)

* Tue Jul 23 2002 Tim Powers <timp@redhat.com> 2.2.2-10
- build using gcc-3.2-0.1

* Tue Jun 25 2002 Than Ngo <than@redhat.com> 2.2.2-9
- fix to build openmotif (bug #64176)

* Thu Jun 13 2002 Than Ngo <than@redhat.com> 2.2.2-8
- rebuild in new enviroment

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Harald Hoyer <harald@redhat.de> 2.2.2-6
- patched ltmain.sh to link properly

* Wed May 22 2002 Harald Hoyer <harald@redhat.de> 2.2.2-6
- specified libraries by full name in files section 
  (libMrm was missing on alpha)

* Tue Mar 26 2002 Than Ngo <than@redhat.com> 2.2.2-5
- update new 2.2.2 from ICS

* Sun Mar 24 2002 Than Ngo <than@redhat.com> 2.2.2-4
- add missing uil

* Fri Mar 22 2002 Tim Powers <timp@redhat.com>
- rebuilt to try and shake some broken deps in the devel package

* Thu Mar 21 2002 Than Ngo <than@redhat.com> 2.2.2-2
- rebuild

* Thu Mar 21 2002 Than Ngo <than@redhat.com> 2.2.2-1
- update to 2.2.2 release

* Mon Feb 22 2002 Than Ngo <than@redhat.com> 2.2.1-3
- conflict with older lesstif

* Mon Feb 22 2002 Than Ngo <than@redhat.com> 2.2.1-2
- fix bug #60816

* Fri Feb 22 2002 Than Ngo <than@redhat.com> 2.2.1-1
- update to 2.2.1 release
- remove somme patches, which are included in 2.2.1

* Fri Feb 22 2002 Tim Powers <timp@redhat.com>
- rebuilt in new environment

* Fri Jan 25 2002 Tim Powers <timp@redhat.com>
- don't obsolete lesstif anymore, play nicely together
- rebuild against new toolchain

* Wed Jan 21 2002 Than Ngo <than@redhat.com> 2.1.30-11
- add some patches from Darrell Commander (supporting largefile)
- fix to build on s390

* Thu Jan 17 2002 Than Ngo <than@redhat.com> 2.1.30-10
- rebuild in 8.0

* Wed Sep  6 2001 Than Ngo <than@redhat.com>
- rebuild for ExtraBinge 7.2

* Thu May 03 2001 Than Ngo <than@redhat.com>
- add 3 official motif patches 
- add rm -rf $RPM_BUILD_ROOT in install section
- remove some old patches which are now in official patches

* Fri Dec 29 2000 Than Ngo <than@redhat.com>
- don't build static debug libraries

* Mon Dec 18 2000 Than Ngo <than@redhat.com>
- bzip2 source

* Mon Jul 24 2000 Than Ngo <than@redhat.de>
- rebuilt against gcc-2.96-44

* Wed Jul 12 2000 Than Ngo <than@redhat.de>
- rebuilt

* Sun Jun 11 2000 Than Ngo <than@redhat.de>
- fix imake to built with gcc-2.96 (thanks Jakup)
- put bitmaps in /usr/X11R6/include/X11/bitmaps
- put bindings in /usr/X11R6/lib/Xm/bindings
- add define -D_GNU_SOURCE to build Motif
- gzip man pages
- cleanup specfile

* Mon May 29 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Update to patchlevel 2
- remove bindings patch, it's included in pl2

* Tue May 16 2000 Matt Wilson <msw@redhat.com>
- use -fPIC on sparc
- fixed Ngo's "fixes"

* Mon May 15 2000 Ngo Than <than@redhat.de>
- added description.
- fixed spec, added uil stuff.

* Mon May 15 2000 Matt Wilson <msw@redhat.com>
- initialization of spec file.
