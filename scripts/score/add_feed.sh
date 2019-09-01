#!/bin/bash

. ./scripts/utils/utils.sh

function print_usage {
    usage_header ${0}
    usage_option " -n <network> : Network to use (localhost, yeouido, euljiro or mainnet)"
    usage_option " -a <score address> : SCORE address of the new price feed"
    usage_option " -x <operator name> : Operator feed name"
    usage_footer
    exit 1
}

function process {
    if [[ ("$network" == "") || ("$score" == "") || ("$name" == "") ]]; then
        print_usage
    fi

    command=$(cat <<-COMMAND
    tbears sendtx <(
        python ./scripts/score/dynamic_call/add_feed.py
            ${network@Q}
            ${score@Q}
            ${name@Q}
        )
        -c ./config/${network}/tbears_cli_config.json
COMMAND
)

    txresult=$(./scripts/icon/txresult.sh -n "${network}" -c "${command}")
    echo -e "${txresult}"
}

# Parameters
while getopts "n:a:x:" option; do
    case "${option}" in
        n)
            network=${OPTARG}
            ;;
        a)
            score=${OPTARG}
            ;;
        x)
            name=${OPTARG}
            ;;
        *)
            print_usage 
            ;;
    esac 
done
shift $((OPTIND-1))

process