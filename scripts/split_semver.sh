#!/bin/bash

# Check if an argument is provided
if [ $# -ne 1 ]; then
	echo "Usage: $0 <semver>"
	exit 1
fi

# Input semver version
input_semver="$1"

# Split the input by periods (.)
IFS='.' read -ra parts <<<"$input_semver"

# Loop through the parts and generate permutations
result=()
for ((i = 0; i < ${#parts[@]}; i++)); do
	version=""
	for ((j = 0; j <= i; j++)); do
		if [ -z "$version" ]; then
			version="${parts[j]}"
		else
			version="$version.${parts[j]}"
		fi
	done
	result+=("$version")
done

# Print the permutations
for perm in "${result[@]}"; do
	echo "$perm"
done
