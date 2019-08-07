#!/bin/bash

. ./scripts/utils/utils.sh

function print_usage {
    usage_header ${0}
    usage_option " -n <network> : Network to use (localhost, yeouido, euljiro or mainnet)"
    usage_option " -m <minimum> : The minimum amount of price feeds required for the oracle to run"
    usage_footer
    exit 1
}

function process {
    if [[ ("$network" == "") || ("$minimum" == "") ]]; then
        print_usage
    fi

    command="tbears sendtx <(python ./scripts/score/dynamic_call/set_minimum_feeds_available.py ${network} ${minimum}) 
            -c ./config/${network}/tbears_cli_config.json"

    txresult=$(./scripts/icon/txresult.sh -n "${network}" -c "${command}")
    echo -e "${txresult}"
}

# Parameters
while getopts "n:m:" option; do
    case "${option}" in
        n)
            network=${OPTARG}
            ;;
        m)
            minimum=${OPTARG}
            ;;
        *)
            print_usage 
            ;;
    esac 
done
shift $((OPTIND-1))

process