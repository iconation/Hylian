#!/bin/bash

function getKeystorePath {
    network=${1}
    echo "./config/${network}/keystores/operator.icx"
}

function generateKeystore {
    network=${1}
    echo -e "\n===[${network}]===================================="
    keystore=$(getKeystorePath ${network})
    # Check if file exists
    if [ -f "$keystore" ]; then
        echo "Operator wallet is already generated for ${network}."
    else
        echo "Generating operator keystore for ${network} ..."
        tbears keystore ${keystore}
    fi
    echo -e "===[/${network}]====================================\n"
}

# Generate keystores
# localhost should be pre-generated
# generateKeystore "localhost"
generateKeystore "yeouido"
generateKeystore "euljiro"
generateKeystore "mainnet"
