import json
import sys

if __name__ == '__main__':
    network = sys.argv[1]
    timeout = sys.argv[2]
    score_address_txt = "./config/" + network + "/score_address.txt"

    call = json.loads(open("./calls/set_timeout.json", "rb").read())
    call["params"]["to"] = open(score_address_txt, "r").read()

    call["params"]["data"]["params"]["timeout"] = timeout

    print(json.dumps(call))
