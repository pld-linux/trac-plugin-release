%define		trac_ver	0.11
%define		plugin		release
Summary:	Software Release Control for Trac
Name:		trac-plugin-%{plugin}
Version:	0.1
Release:	0.1
License:	BSD
Group:		Applications/WWW
# Source0Download: http://trac-hacks.org/changeset/latest/tracreleaseplugin?old_path=/&filename=tracreleaseplugin&format=zip
Source0:	trac%{plugin}plugin.zip
# Source0-md5:	ed17f11d226b1aa97dd2eaf2da7a2fe8
URL:		http://trac-hacks.org/wiki/TracReleasePlugin
Patch0:		%{name}.patch
BuildRequires:	python-devel
Requires:	trac >= %{trac_ver}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A Trac plugin where you fill the version, the Release description and
the user names of those people who should approve it.

%prep
%setup -q -n trac%{plugin}plugin
%patch0 -p1

%build
cd %{trac_ver}/trunk
%{__python} setup.py build
%{__python} setup.py egg_info

%install
rm -rf $RPM_BUILD_ROOT
cd %{trac_ver}/trunk
%{__python} setup.py install \
	--single-version-externally-managed \
	--optimize 2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = "1" ]; then
	%banner -e %{name} <<-'EOF'
	To enable the %{plugin} plugin, add to conf/trac.ini:

	[components]
	trac%{plugin}.* = enabled

	Run trac-admin <env> upgrade on your Trac environment.

	Restart your web server.
EOF
fi

%files
%defattr(644,root,root,755)
%{py_sitescriptdir}/trac%{plugin}
%{py_sitescriptdir}/*-*.egg-info
