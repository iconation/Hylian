#!/bin/bash

. ./scripts/utils/utils.sh

function print_usage {
    usage_header ${0}
    usage_option " -n <network> : Network to use (localhost, yeouido, euljiro or mainnet)"
    usage_option " -t <ticker name> : The new name of the medianizer ticker"
    usage_footer
    exit 1
}

function process {
    if [[ ("$network" == "") || ("$ticker_name" == "") ]]; then
        print_usage
    fi

    command="tbears sendtx <(python ./scripts/score/dynamic_call/set_ticker_name.py ${network} ${ticker_name}) 
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
            ticker_name=${OPTARG}
            ;;
        *)
            print_usage 
            ;;
    esac 
done
shift $((OPTIND-1))

process