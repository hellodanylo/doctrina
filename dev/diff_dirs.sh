#!/usr/bin/env bash

tree_a=$(mktemp)
tree_b=$(mktemp)

tree -L $1 $2 >"$tree_a"
tree -L $1 $3 >"$tree_b"

diff --color "$tree_a" "$tree_b"
