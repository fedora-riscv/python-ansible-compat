%global srcname ansible-compat
%global pkgname python-ansible-compat

%bcond_without tests

Name:    %{pkgname}
Version: 2.2.7
Release: %autorelease
Summary: Ansible python helper functions

URL:       https://github.com/ansible/ansible-compat
Source0:   %{pypi_source ansible-compat}
License:   MIT
BuildArch: noarch

BuildRequires: pyproject-rpm-macros
BuildRequires: ansible-core
BuildRequires: python3dist(flaky)
BuildRequires: python3dist(pytest)
BuildRequires: python3dist(pytest-mock)


%global common_description %{expand:
A python package containing functions that help interacting with
various versions of Ansible}

%description %{common_description}

%package -n python-%{srcname}-doc
Summary: %summary

%description -n python-%{srcname}-doc
Documentation for python-ansible-compat

%package -n python3-%{srcname}
Summary: %summary

%py_provides python3-%{srcname}

%description -n python3-%{srcname} %{common_description}

%prep
%autosetup -p1 -n %{srcname}-%{version}

%generate_buildrequires
%pyproject_buildrequires -r %{?with_tests:-x testing}

%build
%pyproject_wheel

%if %{with doc}
PYTHONPATH=src sphinx-build-3 docs html
rm -rf html/.{doctrees,buildinfo}
%endif

%install
%pyproject_install

%if %{with tests}
%check
%pytest -vv test -k \
    %{shrink:
        '
        not test_prepare_environment_with_collections
        and not test_prerun_reqs_v1
        and not test_prerun_reqs_v2
        and not test_require_collection_wrong_version
        and not test_require_collection
        and not test_install_collection
        and not test_install_collection_dest
        and not test_upgrade_collection
        and not test_require_collection_no_cache_dir
        and not test_runtime_run
        '
    }
%endif

%files -n python3-%{srcname}
%{python3_sitelib}/ansible_compat/
%{python3_sitelib}/ansible_compat-*.dist-info/
%license LICENSE

%if %{with doc}
%files -n python-%{srcname}-doc
%license LICENSE
%doc *.rst
%doc html/
%endif

%changelog
%autochangelog
