#!/bin/bash

force="FALSE"

function revert # file
{
    if [ -f "$1" ]
    then
        if [ "${force}" = "TRUE" ]
        then
            echo "Forcing removal of $1"
            rm $1
        else
            if cvs diff -b "$1" >/dev/null
            then
                echo "File $1 is unchanged. Removing."
                rm $1            
            else
                echo "File $1 has changed. Leaving."
                return 1
            fi
        fi
    else
        echo "\"$1\"" is not a regular file. Ignoring >&2
        return 2
    fi
}


if [ "$#" -gt 0 ]
then
    if [ "$1" = "-f" ]
    then
        force="TRUE"
        shift
    fi
fi

if [ "$#" -eq 0 ]
then
    cvs -q -n update | grep "^[CM]" | cut -b3- | while read file
    do
        revert "$file"
    done
    cvs -Q update
else
    while [ "$#" -gt 0 ]
    do
        revert "$1" && cvs -Q update "$1"
        shift
    done
fi
    