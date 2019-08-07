import json
import sys

if __name__ == '__main__':
    network = sys.argv[1]
    minimum = sys.argv[2]
    score_address_txt = "./config/" + network + "/score_address.txt"

    call = json.loads(open("./calls/set_minimum_feeds_available.json", "rb").read())
    call["params"]["to"] = open(score_address_txt, "r").read()

    call["params"]["data"]["params"]["minimum_feeds_available"] = minimum

    print(json.dumps(call))
