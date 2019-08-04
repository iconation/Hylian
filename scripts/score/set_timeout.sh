#!/bin/bash

. ./scripts/utils/utils.sh

function print_usage {
    usage_header ${0}
    usage_option " -n <network> : Network to use (localhost, yeouido, euljiro or mainnet)"
    usage_option " -t <timeout value> : The new value of the timeout (in microseconds)"
    usage_footer
    exit 1
}

function process {
    if [[ ("$network" == "") || ("$timeout" == "") ]]; then
        print_usage
    fi

    command="tbears sendtx <(python ./scripts/score/dynamic_call/set_timeout.py ${network} ${timeout}) 
            -c ./config/${network}/tbears_cli_config.json"

    txresult=$(./scripts/icon/txresult.sh -n "${network}" -c "${command}")
    echo -e "${txresult}"
}

# Parameters
while getopts "n:t:" option; do
    case "${option}" in
        n)
            network=${OPTARG}
            ;;
        t)
            timeout=${OPTARG}
            ;;
        *)
            print_usage 
            ;;
    esac 
done
shift $((OPTIND-1))

process