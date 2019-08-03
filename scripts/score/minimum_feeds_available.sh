#!/bin/bash

. ./scripts/utils/utils.sh

function print_usage {
    usage_header ${0}
    usage_option " -n <network> : Network to use (localhost, yeouido, euljiro or mainnet)"
    usage_footer
    exit 1
}

function process {
    if [[ ("$network" == "") ]]; then
        print_usage
    fi

    command="tbears call <(python ./scripts/score/dynamic_call/minimum_feeds_available.py "${network}") 
            -c ./config/${network}/tbears_cli_config.json"

    txresult=$(./scripts/icon/call.sh -n "${network}" -c "${command}")
    echo -e "${txresult}"
}

# Parameters
while getopts "n:a:" option; do
    case "${option}" in
        n)
            network=${OPTARG}
            ;;
        *)
            print_usage 
            ;;
    esac 
done
shift $((OPTIND-1))

process