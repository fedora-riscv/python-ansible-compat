%global srcname ansible-compat
%global pkgname python-ansible-compat

Name:    %{pkgname}
Version: 0.5.0
Release: 2%{?dist}
Summary: Ansible python helper functions

URL:       https://github.com/ansible-community/ansible-compat
Source0:   %{pypi_source}
License:   MIT
BuildArch: noarch

# This patch skips the tests requiring a connection to
# ansible galaxy
Patch0: 0001_skip_tests_requiring_network_connectivity.patch

BuildRequires: ansible
BuildRequires: python3-devel
BuildRequires: python3dist(flaky)
BuildRequires: python3dist(pyyaml)
BuildRequires: python3dist(pytest)
BuildRequires: python3dist(setuptools)
BuildRequires: python3dist(pytest-mock)
BuildRequires: python3-setuptools_scm+toml

Requires: python3dist(pyyaml)
Requires: python3dist(cached_property)

%description
A python package containing functions that help interacting with
various versions of Ansible

%package -n python-%{srcname}-doc
Summary: %summary

%description -n python-%{srcname}-doc
Documentation for python-ansible-compat


%package -n python3-%{srcname}
Summary: %summary

%{?python_disable_dependency_generator}
%py_provides python3-%{srcname}

%description -n python3-%{srcname}
A python package containing functions that help interacting with
various versions of Ansible


%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%{py3_build}

%if %{with doc}
PYTHONPATH=src sphinx-build-3 docs html
rm -rf html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}

%check
PYTHONPATH=src pytest-3 test


%files -n python3-%{srcname}
%license LICENSE
%{python3_sitelib}/ansible_compat-%{version}-py%{python3_version}.egg-info
%{python3_sitelib}/ansible_compat/

%if %{with doc}
%files -n python-%{srcname}-doc
%license LICENSE
%doc *.rst
%doc html/
%endif

%changelog
* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Sep 01 2021 Chedi Toueiti <chedi.toueiti@gmail.com> - 0.5.0-1
- Initial commit version 0.5.0