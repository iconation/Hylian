import json
import sys

if __name__ == '__main__':
    network = sys.argv[1]
    score_address_txt = "./config/" + network + "/score_address.txt"

    call = json.loads(open("./calls/value.json", "rb").read())
    call["params"]["to"] = open(score_address_txt, "r").read()

    print(json.dumps(call))
