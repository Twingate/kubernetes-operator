#!/bin/bash

# Check if there are any staged changes in the Git repository
if [ -n "$(git diff --cached --name-status)" ]; then
	echo "Error: There are staged changes in the Git repository."
	exit 1
fi

# Make sure s installed
if type "semantic-release" &>/dev/null; then
	echo "semantic-release exists."
else
	poetry install --with build -n
fi

echo "🧠 Running semantic-release..."
if ! semantic-release --strict version --no-vcs-release; then
	echo "🚀 Pushing release commit and tag to GitHub... "
	git push --no-verify
fi
