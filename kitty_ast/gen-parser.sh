#!/bin/bash

srcs="grammar/Solidity.g4"
target_dir=solidity_antlr4

antlr -Dlanguage=Python3 "$srcs" \
    -Xexact-output-dir -visitor \
    -o "$target_dir"

# make the $target_dir a python module (for older Python versions)
touch "$target_dir/__init__.py"
