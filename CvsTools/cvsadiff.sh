#!/bin/bash

version[0]=''
version[1]=''

next_version=0
delete_file_name_1="NO"

function do_diffs
{
    for file in "$*"
    do
        do_one_diff ${file} &
    done
}

function do_one_diff
{
    file_name=$1

    echo version=${version[0]} ${version[1]}
    echo $*


    if [ -n "${version[0]}" ]
    then
        file_name_0="${HOME}/.#$(basename ${file_name}).${version[0]}.${$}.tmp"
        echo file_name_0 = ${file_name_0}
        cvs update -p -r ${version[0]} ${file_name} > ${file_name_0}
    else
        file_name_0="${HOME}/.#`basename ${file_name}`.committed.${$}.tmp"
        cvs update -p ${file_name} > ${file_name_0}
    fi
    
    if [ -n "${version[1]}" ]
    then
        file_name_1=${HOME}/.\#$(basename ${file_name}).${version[1]}.${$}.tmp
        cvs update -p -r ${version[1]} ${file_name} > ${file_name_1}
        delete_file_name_1="YES"
    else
        file_name_1=${file_name}
    fi
    
    app_client amerge ${file_name_0} ${file_name_1}
    
    { sleep 5 && rm  ${file_name_0} ; } &
    
    if [ ${delete_file_name_1} == "YES" ]
    then
        { sleep 5 && rm ${file_name_1} ; } &
    fi
}

#
# If you put a ":" at the front of the "opt string", getopts doesn't
# report errors but if you miss a required argument to a parameter, it
# will put ":" in the o variable (or whatever you call it)
#
while getopts :r: o
do
    case $o in
    r)
        if [ ${next_version} == 2 ]
        then
            echo error! at most two \"-r\"s can be specified
            exit 1
        fi
        version[next_version]=${OPTARG}
        next_version=$((${next_version} + 1))
        ;;
    :) echo error! ${OPTARG} requires an argument; exit 1 ;;
    *) echo error! ${OPTARG} is not a valid option; exit 1 ;;
    esac 
done
 
#
# Shift past all the parameters that getopts used.  Then if you have
# extra arguments, you can still refer to them as $1
#
shift $((${OPTIND} - 1))

if  [ $# -eq 0 ]
then
    files=`cvs -n update $*| grep '^M' | cut -f2- -d' '`
else
    files="$*"
fi

do_diffs ${files} # cvsadiff ${f} &


