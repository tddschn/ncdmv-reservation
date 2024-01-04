#!/usr/bin/env bash

# Default office name
office_name="Raleigh West"

# Display help information
display_help() {
    echo "Usage: $0 [option...] {office_name}" >&2
    echo
    echo "   -h, --help                 Display this help message"
    echo "   office_name                Office name to search for (default: Raleigh West)"
    echo
    exit 1
}

# Parse command line arguments
while (("$#")); do
    case "$1" in
    -h | --help)
        display_help
        ;;
    -* | --*=) # unsupported flags
        echo "Error: Unsupported flag $1" >&2
        exit 1
        ;;
    *) # preserve positional arguments
        office_name=$1
        shift
        ;;
    esac
done

if [ ! -f ncdmv.html ]; then
    echo "Running test with selenium..." >&2
    pytest test_ncdmv.py
fi
if [ ! -f ncdmv.json ]; then
    echo 'extracting results...' >&2
    ./ncdmv_results_to_json.py ncdmv.html | tee ncdmv.json
fi
jq <ncdmv.json --arg office_name "$office_name" '.[] | select(.office_name == $office_name) | .is_reservable' -r
