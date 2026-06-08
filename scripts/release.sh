#!/bin/bash

# Check if there are any staged changes in the Git repository
if [ -n "$(git diff --cached --name-status)" ]; then
	echo "Error: There are staged changes in the Git repository."
	exit 1
fi

# Make sure pipx is installed (used to run semantic-release in isolation)
if ! type "pipx" &>/dev/null; then
	echo "Error: pipx is not installed. Install it with 'brew install pipx' or 'python -m pip install --user pipx'."
	exit 1
fi

echo "🧠 Running semantic-release..."
if ! pipx run --spec python-semantic-release==10.5.3 semantic-release --strict version --no-vcs-release; then
	echo "🚀 Pushing release commit and tag to GitHub... "
	git push --no-verify
fi
