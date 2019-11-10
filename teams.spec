%global         debug_package %{nil}
%global         __strip /bin/true

# Remove bundled libraries from requirements/provides
%if 0%{?rhel} == 7
%global         __requires_exclude ^(libffmpeg\\.so.*|libEGL\\.so.*|libGLESv2\\.so.*)$
%else
%global         __requires_exclude ^(libffmpeg\\.so.*|libEGL\\.so.*|libGLESv2\\.so.*)$
%endif
%global         __provides_exclude ^(lib.*\\.so.*)$

Name:           teams
Version:        1.2.00.29659
Release:        1%{?dist}
Summary:        Microsoft Teams
License:        Microsoft License
URL:            https://products.office.com/en-us/microsoft-teams/group-chat-software

Source0:        https://packages.microsoft.com/repos/ms-teams/pool/main/t/teams-insiders/teams-insiders_%{version}_amd64.deb
Source2:        %{name}-wrapper

BuildRequires:  desktop-file-utils
#Requires:       

%description
Microsoft Teams for Linux is your chat-centered work space in Office 365.
Instantly access all your team’s content from a single place where messages,
files, people and tools live together.

%prep
%setup -q -c -T

ar x %{SOURCE0}
tar -xJf data.tar.xz

sed -i -e 's|Exec=.*|Exec=/usr/bin/teams|g' usr/share/applications/teams-insiders.desktop

%build
# Nothing to build.

%install
mkdir -p %{buildroot}%{_libdir}
cp -fra usr/share/teams-insiders %{buildroot}%{_libdir}/%{name}

mkdir -p %{buildroot}%{_datadir}/applications
install -m 644 -p usr/share/applications/%{name}-insiders.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop

mkdir -p %{buildroot}%{_datadir}/pixmaps
ln -sf %{_libdir}/teams-insiders/icon.png %{buildroot}%{_datadir}/pixmaps/%{name}.png

# Wrapper script
mkdir -p %{buildroot}%{_bindir}
cat %{SOURCE2} | sed -e 's|INSTALL_DIR|%{_libdir}/%{name}|g' \
    > %{buildroot}%{_bindir}/%{name}
chmod +x %{buildroot}%{_bindir}/%{name}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%{_bindir}/%{name}
%{_libdir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png

%changelog
* Sat Nov 09 2019 Simone Caronni <negativo17@gmail.com> - 1.2.00.29659-1
- Update to 1.2.00.29659.

* Tue Sep 17 2019 Simone Caronni <negativo17@gmail.com> - 1.2.00.25951-1
- First build.
