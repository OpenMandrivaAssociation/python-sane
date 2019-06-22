%global name2 python2-sane
%global py2dir ../py2

# Refer to the comment for Source0 below on how to obtain the source tarball
# The saved file has format python-pillow-Sane-$version-$ahead-g$shortcommit.tar.gz
%global commit 8c4d40d85a915f0dcc6b3177d4d3d70466188d8c
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global ahead 0

# If ahead is 0, the tarball corresponds to a release version, otherwise to a git snapshot
%if %{ahead} > 0
%global snap .git%{shortcommit}
%endif
%bcond_with python2

Name:           python-sane
Version:	2.8.3
Release:        3
Summary:        Python SANE interface

License:        MIT
URL:            https://github.com/python-pillow/Sane

# Obtain the tarball for a certain commit via:
#  wget --content-disposition https://github.com/python-pillow/Sane/tarball/$commit
Source0:        https://github.com/python-pillow/Sane/tarball/%{commit}/python-pillow-Sane-v%{version}-%{ahead}-g%{shortcommit}.tar.gz

BuildRequires:  sane-devel

%if %{with python2}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-sphinx
%endif

BuildRequires:  python3-devel
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx

Obsoletes:      python-pillow-sane < 2.7.0-1
Provides:       python-pillow-sane = %{version}-%{release}

Requires:       python-imaging

%description
This package contains the sane module for Python which provides access to
various raster scanning devices such as flatbed scanners and digital cameras.


%if %{with python2}
%package -n %{name2}
Summary:        Python module for using scanners
Provides:       python2-pillow-sane = %{version}-%{release}
Requires:       python2-numpy

%description -n %{name2}
This package contains the sane module for Python which provides access to
various raster scanning devices such as flatbed scanners and digital cameras.
%endif


%prep
%setup -q -n python-pillow-Sane-%{shortcommit}

# Create Python 3 source tree
rm -rf %{py2dir}
mkdir %{py2dir}
cp -a . %{py2dir}


%build
# Build Python 3 modules
find -name '*.py' | xargs sed -i '1s|^#!.*python|#!%{__python}|'
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

pushd doc
make html
rm -f _build/html/.buildinfo
popd

%if %{with python2}
# Build Python 2 modules
pushd %{py2dir}
find -name '*.py' | xargs sed -i '1s|^#!.*python|#!%{__python2}|'
CFLAGS="$RPM_OPT_FLAGS" %{__python2} setup.py build

pushd doc
make html SPHINXBUILD=sphinx-build-%py2_ver
rm -f _build/html/.buildinfo
popd
%endif

%install
# Install Python 3 modules
%{__python} setup.py install --skip-build --root %{buildroot}

# Fix non-standard-executable-perm
chmod 0755 %{buildroot}%{python_sitearch}/*.so

%if %{with python2}
# Install Python 2 modules
pushd %{py2dir}
%{__python2} setup.py install --skip-build --root %{buildroot}
popd

# Fix non-standard-executable-perm
chmod 0755 %{buildroot}%{python3_sitearch}/*.so
%endif

%if 0%{?with_docs}
pushd doc
make html SPHINXBUILD=sphinx-build-%python3_version
rm -f _build/html/.buildinfo
popd
%endif


%files
%doc CHANGES.rst sanedoc.txt example.py doc/_build/html COPYING
%{python3_sitearch}/*

%if %{with python2}
%files -n %{name2}
%doc CHANGES.rst sanedoc.txt example.py doc/_build/html COPYING
%{python2_sitearch}/*
%endif
