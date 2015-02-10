# Will turn on extra output to help debug profile-loading.
# Don't check in as "true"
$verbose = $true

# A convenience function to get the directory the current script lives in
# - useful for importing from relative paths
function Get-ScriptDirectory
{
  $Invocation = (Get-Variable MyInvocation -Scope 1).Value
  Split-Path $Invocation.MyCommand.Path
}

function Include-ProfileDirectory([string] $directory)
{
    # Load every file in the Includes subdirectory -
    # hopefully they can be loaded in any order.
    # The Includes directory should contain files that define functions and
    # filters to be executed later, but not scripts that need to do
    # something when the file is sourced.
    #
    # It's probably not always going to be clear whether things should be in
    # Includes or Scripts
    if ( Test-Path ($directory + '\Includes') )
    {
            Get-ChildItem -Path:($directory + '\Includes') -Filter:*.ps1 | ForEach-Object {
            if ( $verbose )
            {
                Write-Output ("importing " + $_.PSPath)
            }
            . $_.PSPath
        }
    }

    # The Scripts directory should contain PowerShell scripts that someone
    # might want to be executed, so we'll add it to our path.
    if ( Test-Path "$directory\Scripts" )
    {
        $env:PATH = "$($env:PATH);$directory\Scripts"
    }
}

. Include-ProfileDirectory(Get-ScriptDirectory)
# Look for user-specfic customizations. If they're there, load them.
$userProfileDir = ((Get-ScriptDirectory) + '\' + $env:USERNAME)
if ( Test-Path $userProfileDir )
{
    if ( $verbose )
    {
        Write-Output "including $userProfileDir"
    }
    . Include-ProfileDirectory($userProfileDir)

    $userProfile = ($userProfileDir + '\profile.ps1')
    if ( Test-Path $userProfile )
    {
        . $userProfile
    }
}
else
{
    Write-Host -foregroundcolor yellow -backgroundColor darkblue @"

Welcome to the DayJob PowerShell Profile.  It looks like this is your
first time here, so I'll create a new profile for you. This profile
will be called

   $userProfile

If you want to customize your PowerShell experience, you can edit this
file. Eventually you may want to modify files in the containing directories,
but keep in mind that those changes will affect other users.

Have fun!

"@

    New-Item -path  $userProfile -itemType "file" -Force > Out-Null
}
