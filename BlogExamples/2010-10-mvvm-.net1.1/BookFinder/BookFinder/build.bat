copy ..\BookFinder.Core\BookFinder.Core.dll .
%windir%\Microsoft.NET\Framework\v1.1.4322\csc /reference:BookFinder.Core.dll /out:BookFinder.exe *.cs