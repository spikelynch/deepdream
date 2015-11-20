#!/usr/bin/env bash


a="one"
b="one"
c="two"

if [ $a == $b ]; then
    echo "a = b"
fi

if [ $a == $c ]; then
    echo "a = c"
fi
