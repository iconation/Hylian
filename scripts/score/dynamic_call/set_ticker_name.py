import json
import sys

if __name__ == '__main__':
    network = sys.argv[1]
    ticker_name = sys.argv[2]
    score_address_txt = "./config/" + network + "/score_address.txt"

    call = json.loads(open("./calls/set_ticker_name.json", "rb").read())
    call["params"]["to"] = open(score_address_txt, "r").read()

    call["params"]["data"]["params"]["ticker_name"] = ticker_name

    print(json.dumps(call))
