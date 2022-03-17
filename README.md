# GitHub Actions Workflow Manager

## Compatibility:

## Usage:

First install the project dependencies:

1. Install homebrew, using the command: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`.
2. Install jq and gh tools using the command: `brew install jq gh`.

NOTE: This project has been written in Python 3.9, and tested against MacOS 12.

Then, run using the command: `python3.9 main.py`.

## Capabilities:

    1. List all workflows in the selected repository.
    2. List all run IDs for a given workflow.
    3. Delete all run IDs for a given workflow.
