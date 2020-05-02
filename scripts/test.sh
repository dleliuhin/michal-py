#!/bin/bash

if [ -d "test_michal-py/build_test" ];
then
	rm -rf test_michal-py/build_test/*
else
	mkdir -p test_michal-py/build_test
fi

cd test_michal-py/build_test

python3 -m unittest test.py