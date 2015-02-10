cls
pushd ..\BookFinder.Core
call build.bat
popd

copy ..\BookFinder.Core\BookFinder.Core.dll .
copy ..\libs\nunit.core.dll .
copy ..\libs\nunit.framework.dll .
%windir%\Microsoft.NET\Framework\v1.1.4322\csc /debug /reference:nunit.framework.dll /reference:BookFinder.Core.dll /target:library /out:BookFinder.Tests.dll *.cs