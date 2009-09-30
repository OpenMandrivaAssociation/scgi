Summary:	Simple Common Gateway Interface
Name:		scgi
Version:	1.13
Release:	%mkrel 4
Group:		System/Servers
License:	BSD-style
URL:		http://python.ca/scgi/
Source0:	http://python.ca/scgi/releases/scgi-%{version}.tar.gz
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

%prep

%setup -q -n scgi-%{version}

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

python setup.py build

%install
rm -rf %{buildroot}

python setup.py install --prefix=%{_prefix} --root=%{buildroot} --record=INSTALLED_FILES

%clean
rm -rf %{buildroot}

%files -n python-scgi -f INSTALLED_FILES
%defattr(-,root,root)
%doc README.txt CHANGES.txt LICENSE.txt
