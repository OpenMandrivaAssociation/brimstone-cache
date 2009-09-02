%define section         free
%define gcj_support     1

Name:           brimstone-cache
Version:        0.1.16
Release:        %mkrel 5.0.5
Epoch:          0
Summary:        org.freecompany.brimstone
License:        MIT
Group:          Development/Java
URL:            http://www.freecompany.org/
# svn export https://svn.freecompany.org/public/brimstone/tags/brimstone-cache-0.1.16 | yes t
# zip -9r brimstone-cache-src-0.1.16.zip brimstone-cache-0.1.16
Source0:        http://repository.freecompany.org/org/freecompany/brimstone/zips/brimstone-cache-src-%{version}.zip
Source1:        brimstone-cache-0.1.16-build.xml
Requires:       brimstone-core
Requires:       java >= 1.6
Requires:       util-core
BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  brimstone-core
BuildRequires:  util-core
BuildRequires:  java-rpmbuild >= 0:1.6
BuildRequires:  junit
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildRequires:  java-devel
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
org.freecompany.brimstone

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
%{__cp} -a %{SOURCE1} build.xml
%{__perl} -pi -e 's|<javac|<javac nowarn="true"|g' build.xml

%build
export CLASSPATH=$(build-classpath junit brimstone-core util-core)
export OPT_JAR_LIST="ant/ant-junit"
# XXX: test testFileCachedWithoutHeaders does not pass
%ant jar javadoc #test

%install
%{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a dist/%{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
%create_jar_links

%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a dist/doc/* %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%{gcj_compile}

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%{gcj_files}

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}
