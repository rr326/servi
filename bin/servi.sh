#!/usr/bin/env bash
# Simple script to run servi from your working directory

if which -s python3
then
    python3 servi $*
else
    echo
    echo "**************************************************"
    echo "python3 not found on path (try: 'which python3')."
    echo "python3 must be installed for servi to work."
    echo "Aborting"
    echo "**************************************************"
    echo
fi

