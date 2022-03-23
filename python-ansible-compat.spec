%global srcname ansible-compat
%global pkgname python-ansible-compat

Name:    %{pkgname}
Version: 2.0.2
Release: 1%{?dist}
Summary: Ansible python helper functions

URL:       https://github.com/ansible/ansible-compat
Source0:   %{pypi_source}
License:   MIT
BuildArch: noarch
BuildRequires:  pyproject-rpm-macros

# This patch skips the tests requiring a connection to
# ansible galaxy
Patch0: 0001_skip_tests_requiring_network_connectivity.patch

Requires: python3dist(pyyaml)
Requires: python3dist(subprocess-tee)

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

%generate_buildrequires
%pyproject_buildrequires -r

%build
%pyproject_wheel

%if %{with doc}
PYTHONPATH=src sphinx-build-3 docs html
rm -rf html/.{doctrees,buildinfo}
%endif

%install
%pyproject_install

%check
# Disable tests as pip-tools, pytest-markdown 
# and pytest-plus not in Fedora yet
#PYTHONPATH=src %{python3} -m pytest -vv

%files -n python3-%{srcname}
%license LICENSE
%{python3_sitelib}/ansible_compat-%{version}.dist-info/
%{python3_sitelib}/ansible_compat/

%if %{with doc}
%files -n python-%{srcname}-doc
%license LICENSE
%doc *.rst
%doc html/
%endif

%changelog
* Wed Mar 23 2022 Parag Nemade <pnemade AT redhat DOT com> - 2.0.2-1
- Update to 2.0.2 version

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Sep 01 2021 Chedi Toueiti <chedi.toueiti@gmail.com> - 0.5.0-1
- Initial commit version 0.5.0
