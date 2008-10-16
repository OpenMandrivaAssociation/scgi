#Module-Specific definitions
%define mod_conf B14_mod_scgi.conf
%define mod_so %{mod_name}.so

Summary:	Simple Common Gateway Interface
Name:		scgi
Version:	1.13
Release:	%mkrel 1
Group:		System/Servers
License:	BSD-style
URL:		http://python.ca/scgi/
Source0:	http://quixote.python.ca/releases/scgi-%{version}.tar.gz
Source1:	B14_mod_scgi.conf
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	file
BuildRequires:	pcre-devel
BuildRequires:	python-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
SCGI: Simple Common Gateway Interface.

The SCGI protocol is a replacement for the Common Gateway Interface (CGI)
protocol. It is a standard for applications to interface with HTTP servers. It
is similar to FastCGI but is designed to be easier to implement. 

%package -n	python-scgi
Summary:        Python implementation of the SCGI protocol
Group:          Development/Python

%description -n	python-scgi
The SCGI protocol is a replacement for the Common Gateway Interface
(CGI) protocol. It is a standard for applications to interface with
HTTP servers. It is similar to FastCGI but is designed to be easier to
implement.

This package contains the python bindings.

%package -n	apache-mod_scgi
Summary:        Apache module named mod_scgi that implements the client side of the protocol
Group:		System/Servers
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache-mpm-prefork >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0

%description -n	apache-mod_scgi
The SCGI protocol is a replacement for the Common Gateway Interface
(CGI) protocol. It is a standard for applications to interface with
HTTP servers. It is similar to FastCGI but is designed to be easier to
implement.

This package contains the apache module.

%prep

%setup -q -n scgi-%{version}

cp %{SOURCE1} B14_mod_scgi.conf

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type d -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

for i in `find . -type d -name CVS` `find . -type d -name .svn` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -r $i; fi >&/dev/null
done

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build
%serverbuild

%{_sbindir}/apxs -c apache2/mod_scgi.c

python setup.py build

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_libdir}/apache-extramodules

install -m0755 apache2/.libs/mod_scgi.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 B14_mod_scgi.conf %{buildroot}%{_sysconfdir}/httpd/modules.d/

python setup.py install --prefix=%{_prefix} --root=%{buildroot} --record=INSTALLED_FILES

cp apache2/README.txt README.apache2.txt

%post -n apache-mod_scgi
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun -n apache-mod_scgi
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
rm -rf %{buildroot}

%files -n python-scgi -f INSTALLED_FILES
%defattr(-,root,root)
%doc README.txt CHANGES.txt LICENSE.txt

%files -n apache-mod_scgi
%defattr(-,root,root,-)
%doc README.txt cgi2scgi.c CHANGES.txt LICENSE.txt README.apache2.txt doc/*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/B14_mod_scgi.conf
%attr(0755,root,root) %{_libdir}/apache-extramodules/mod_scgi.so
