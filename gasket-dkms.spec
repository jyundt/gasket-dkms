%define module gasket
%define version 1.0.0
%define build_id 5
Name:           gasket-dkms
Version:        %{version}
Release:        %{build_id}%{?dist}
Summary:        DKMS source for the gasket driver

License:        GPLv2
URL:            https://coral.ai/     
Group:          System Environment/Kernel
BuildArch:      noarch
Source0:        https://github.com/jyundt/%{name}/archive/%{name}-%{version}-%{build_id}.tar.gz

Provides:       kmod(gasket.ko) = %{version}-%{release}
Provides:       kmod(apex.ko) = %{version}-%{release}

Requires:       dkms
Requires:       kernel-devel
Requires:       make

%description
The Gasket (Google ASIC Software, Kernel Extensions, and Tools) kernel
framework is a generic, flexible system that supports thin kernel
drivers. Gasket kernel drivers are expected to handle opening and
closing devices, mmap'ing BAR space as requested, a small selection of
ioctls, and handling page table translation (covered below). Any other
functions should be handled by userspace code.

The Gasket common module is not enough to run a device. In order to
customize the Gasket code for a given piece of hardware, a device
specific module must be created. At a minimum, this module must define a
struct gasket_driver_desc containing the device-specific data for use by
the framework; in addition, the module must declare an __init function
that calls gasket_register_device with the module's gasket_driver_desc
struct. Finally, the driver must define an exit function that calls
gasket_unregister_device with the module's gasket_driver_desc struct.

One of the core assumptions of the Gasket framework is that precisely
one process is allowed to have an open write handle to the device node
at any given time. (That process may, once it has one write handle, open
any number of additional write handles.) This is accomplished by
tracking open and close data for each driver instance.

%prep
%setup -n %{name}-%{name}-%{version}-%{build_id}

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_usrsrc}/%{module}-%{version}
cp -r src/* %{buildroot}%{_usrsrc}/%{module}-%{version}

%post
dkms add -m %{module} -v %{version} -q --rpm_safe_upgrade
dkms build -m %{module} -v %{version} -q 
dkms install -m %{module} -v %{version} -q --force

%files
%{_usrsrc}/%{module}-%{version}

%preun
dkms remove -m %{module} -v %{version} --all --rpm_safe_upgrade


%changelog
* Thu Sep 24 2020 Jacob Yundt <jyundt@gmail.com> 1.0.0-5
- Removing patch that modifies upstream driver (jyundt@gmail.com)

* Thu Sep 24 2020 Jacob Yundt <jyundt@gmail.com> 1.0.0-4
- Fixup for Patch0 URL (jyundt@gmail.com)

* Thu Sep 24 2020 Jacob Yundt <jyundt@gmail.com> 1.0.0-3
- Fixup for GitHub release tarball structure (jyundt@gmail.com)

* Thu Sep 24 2020 Jacob Yundt <jyundt@gmail.com> 1.0.0-2
- Fixup for GitHub source URL (jyundt@gmail.com)
- Adding github release workflow (jyundt@gmail.com)

* Thu Sep 24 2020 Jacob Yundt <jyundt@gmail.com> 1.0.0-1
- Initial build based on in-tree 5.4.67 driver (3468bca1)

