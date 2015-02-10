Function Load-File([string] $filename)
{
    . $filename
}

Load-File('.\file-to-load.ps1')

Get-MyName
