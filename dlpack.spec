#
# Conditional build:
%bcond_without	apidocs		# API documentation
#
Summary:	DLPack: Open In Memory Tensor Structure
Summary(pl.UTF-8):	DLPack - otwarta struktura tensorów w pamięci
Name:		dlpack
Version:	1.3
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/dmlc/dlpack/releases
Source0:	https://github.com/dmlc/dlpack/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	69dc180a9197ab9b1b134e93f4de3130
URL:		https://github.com/dmlc/dlpack
BuildRequires:	cmake >= 3.16
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	rpmbuild(macros) >= 1.605
%if %{with apidocs}
BuildRequires:	python3 >= 1:3
BuildRequires:	python3-breathe >= 4.31.0
BuildRequires:	python3-pydata_sphinx_theme >= 0.7.1
BuildRequires:	sphinx-pdg >= 5
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DLPack is an open in-memory tensor structure for sharing tensors among
frameworks. DLPack enables:
- Easier sharing of operators between deep learning frameworks.
- Easier wrapping of vendor level operator implementations, allowing
  collaboration when introducing new devices/ops.
- Quick swapping of backend implementations, like different version of
  BLAS.
- For final users, this could bring more operators, and possibility of
  mixing usage between frameworks.

We do not intend to implement Tensor and Ops, but instead use this as
common bridge to reuse tensor and ops across frameworks.

%description -l pl.UTF-8
DLPack to otwarta struktura tensorów w pamięci przeznaczona do
współdzielenia tensorów między szkieletami. DLPack umożliwia:
- łatwiejsze współdzielenie operatorów między szkieletami głębokiego
  uczenia maszynowego
- łatwiejsze obudowywanie poszczególnych implementacji operatorów,
  pozwalające na współprace przy wprowadzaniu nowych urządzeń/operacji
- szybką podmianę implementacji backendu, jak np. różnych wersji BLAS
- dla użytkowników końcowych - może dostarczyć więcej operatorów i
  możliwość użycia mieszanego między szkieletami.

Celem nie jest implementacja tensorów i operacji, ale użycie jako
wspólnego pomostu do używania tensorów i operacji między szkieletami.

%package devel
Summary:	DLPack: Open In Memory Tensor Structure
Summary(pl.UTF-8):	DLPack - otwarta struktura tensorów w pamięci
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel >= 6:4.7

%description devel
DLPack is an open in-memory tensor structure for sharing tensors among
frameworks. DLPack enables:
- Easier sharing of operators between deep learning frameworks.
- Easier wrapping of vendor level operator implementations, allowing
  collaboration when introducing new devices/ops.
- Quick swapping of backend implementations, like different version of
  BLAS.
- For final users, this could bring more operators, and possibility of
  mixing usage between frameworks.

We do not intend to implement Tensor and Ops, but instead use this as
common bridge to reuse tensor and ops across frameworks.

%description devel -l pl.UTF-8
DLPack to otwarta struktura tensorów w pamięci przeznaczona do
współdzielenia tensorów między szkieletami. DLPack umożliwia:
- łatwiejsze współdzielenie operatorów między szkieletami głębokiego
  uczenia maszynowego
- łatwiejsze obudowywanie poszczególnych implementacji operatorów,
  pozwalające na współprace przy wprowadzaniu nowych urządzeń/operacji
- szybką podmianę implementacji backendu, jak np. różnych wersji BLAS
- dla użytkowników końcowych - może dostarczyć więcej operatorów i
  możliwość użycia mieszanego między szkieletami.

Celem nie jest implementacja tensorów i operacji, ale użycie jako
wspólnego pomostu do używania tensorów i operacji między szkieletami.

%package apidocs
Summary:	API documentation for DLPack library
Summary(pl.UTF-8):	Dokumentacja API biblioteki DLPack
Group:		Documentation

%description apidocs
API documentation for DLPack library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki DLPack.

%prep
%setup -q

%build
# fake CMAKE_INSTALL_LIBDIR to install cmake configs in arch-independent dir
# for noarch header-only library
%cmake -B build \
	%{?with_apidocs:-DBUILD_DOCS=ON} \
	-DCMAKE_INSTALL_LIBDIR=%{_datadir}

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_docdir}
%{__mv} $RPM_BUILD_ROOT%{_datadir}/dlpack/docs/latest $RPM_BUILD_ROOT%{_docdir}/dlpack
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/dlpack/{.doctrees,_sources,.buildinfo,objects.inv}

%clean
rm -rf $RPM_BUILD_ROOT

%files devel
%defattr(644,root,root,755)
%doc NEWS.md README.md
%{_includedir}/dlpack
%{_datadir}/cmake/dlpack

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_docdir}/dlpack
%endif
