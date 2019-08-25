<p align="center">
  <img 
    src="https://iconation.team/images/very_small.png" 
    width="120px"
    alt="ICONation logo">
  X
  <img 
    src="https://iconation.team/images/hylian_nobg.png" 
    width="120px"
    alt="ICONation logo">
</p>

<h1 align="center">Hylian : Price Oracle SCORE</h1>

 [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Introduction

**Hylian** is a generic price oracle on ICON working with a list of price feeds such as [Daedric](https://github.com/iconation/Daedric). In the current version, it simply returns a median value of the whitelisted price feeds.

## Prerequisites

- **[T-Bears](https://github.com/icon-project/t-bears/)** should be installed
- **T-Bears needs to be launched using the configuration file** provided in this repository :
<pre>
tbears start -c ./config/localhost/tbears_server_config.json
</pre>

- You also need `jq`. Install it with `sudo apt-get install jq`

## Installation

- Run the **`install.sh` script** located in the root folder of the repository;

- It will generate 3 operator wallets : 
  - A first one on the Yeouido network in `./config/yeouido/keystores/operator.icx`
  - A second one on the Euljiro network in `./config/euljiro/keystores/operator.icx`
  - A last one on the Mainnet network in `./config/mainnet/keystores/operator.icx`

- Make sure to send some funds to these wallets before deploying a SCORE (20 ICX should be good enough).

- A wallet for localhost development is already pre-generated.
- If you correctly loaded T-bears using the configuration as described in the prerequisites, `tbears balance hxba2e54b54b695085f31ff1a9b33868b5aea44e33` should return some balance.

## Deploy Hylian SCORE to localhost, testnet or mainnet

- In the root folder of the project, run the following command:
<pre>./scripts/score/deploy_score.sh</pre>

- It should display the following usage:
```
> Usage:
 `-> ./scripts/score/deploy_score.sh [options]

> Options:
 -n <network> : Network to use (localhost, yeouido, euljiro or mainnet)
 -t <ticker name> : The name of the medianizer ticker
 -m <minimum> : The minimum amount of price feeds required for the oracle to run
```

- Fill the `-n` option corresponding to the network you want to deploy to: `localhost`, `yeouido`, `euljiro` or `mainnet`.
- Fill the `-t` option with the name of the ticker, such as `ICXUSD`. Note that ticker name needs to be the same than the deployed [Medianizer SCORE](https://github.com/iconation/Medianizer).
- Fille the `-m` option with the minimum number of price feeds available for the price oracle to work, otherwise it will raise an error.
- **Example** : 
<pre>$ ./scripts/score/deploy_score.sh -n localhost -t ICXUSD -m 5</pre>

## Update an already deployed Hylian to localhost, testnet or mainnet

- If you modified the Hylian SCORE source code, you may need to update it.

- In the root folder of the project, run the following command:
<pre>$ ./scripts/score/update_score.sh</pre>

- It should display the following usage:
```
> Usage:
 `-> ./scripts/score/update_score.sh [options]

> Options:
 -n <network> : Network to use (localhost, yeouido, euljiro or mainnet)
```

- Fill the `-n` option corresponding to the network where your SCORE is deployed to: `localhost`, `yeouido`, `euljiro` or `mainnet`.

- **Example** :
<pre>$ ./scripts/score/update_score.sh -n localhost</pre>

## Whitelist a price feed SCORE (such as Daedric)

- Your Hyalin SCORE needs price feeds in order to work. For doing so, you need to whitelist some price feed SCOREs.

- In the root folder of the project, run the following command:
<pre>$ ./scripts/score/add_feed.sh</pre>

- It should display the following usage:
```
> Usage:
 `-> ./scripts/score/add_feed.sh [options]

> Options:
 -n <network> : Network to use (localhost, yeouido, euljiro or mainnet)
 -a <score address> : SCORE address of the new price feed
```

- Fill the `-n` option corresponding to the network where your SCORE is deployed to: `localhost`, `yeouido`, `euljiro` or `mainnet`.
- Fill the `-a` option with the address of the price feed SCORE you want to whitelist.
- **Example** :
<pre>$ ./scripts/score/add_feed.sh -n localhost -a cx17fea4a9a01970cc730db9100dee9d1727af11a5</pre>

## Read the price from the oracle

- Once you have enough price feeds subscribed, you may call the oracle with the `value` method:

<pre>$ ./scripts/score/value.sh</pre>

- It should display the following usage:
```
> Usage:
 `-> ./scripts/score/value.sh [options]

> Options:
 -n <network> : Network to use (localhost, yeouido, euljiro or mainnet)
```

- Fill the `-n` option corresponding to the network where your SCORE is deployed to: `localhost`, `yeouido`, `euljiro` or `mainnet`.

- **Example** :
<pre>$ ./scripts/score/value.sh -n localhost</pre>

If not enough feeds fulfill the conditions declared in the Hylian SCORE, it will return the following error result:

```
{
    "jsonrpc": "2.0",
    "error": {
        "code": -32032,
        "message": "NOT_ENOUGH_FEEDS_AVAILABLE"
    },
    "id": 1
}
```

Otherwise, it will return the following result containing the price value:

```
> Command:
$ tbears call <(python ./scripts/score/dynamic_call/value.py localhost)
            -c ./config/localhost/tbears_cli_config.json
> Result:
$ response : {
    "jsonrpc": "2.0",
    "result": "0x8ac7230489e80000",
    "id": 1
}
```
