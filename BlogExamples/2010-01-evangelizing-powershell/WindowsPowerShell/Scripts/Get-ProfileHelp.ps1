#<#
#.Synopsis
#  Get help for the PowerShellProfile scripts
##>
Get-ScriptDirectory | Get-ChildItem -include "*.ps1" -recurse
 | ForEach-Object {
    $name = $_.Name; $name = $name.Remove($name.Length-4)
    $synopsis = ""
    $content = (Get-Content $_.PSPath)
    for ($i = 0; $i -le ($content.length - 1); $i += 1)
    {
       if ( $content[$i] -like '*.Synopsis*' )
       {
           $synopsis = $content[$i+1].Substring(1).Trim()
           break
       }
    }
    $o = New-Object Object
    $o | Add-Member NoteProperty Name $name
    $o | Add-Member NoteProperty Synopsis $synopsis
    $o
} | Format-Table -AutoSize
