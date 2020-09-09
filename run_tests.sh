#!/usr/bin/env bash

GREEN=$(tput setaf 2)
RED=$(tput setaf 1)
NC=$(tput sgr0)

if [ "$#" -eq "0" ]
then
	printf "${RED}\u2717 Please enter a project directory to test with.${NC}\n"
	exit 1
fi

# generate a makefile for the binary executable on the test dir
python makepy.py test_binary $1

# compile the test files
cd tests && make

if [ "$?" -eq "0" ]
then
	# no error occurred; all tests passed
	printf "\n${GREEN}\u2713 Build test passed.${NC}\n"
	else
		printf "\n${RED}\u2717 An error occurred${NC}\n"
fi

# clean up test folder
make clean && rm Makefile
