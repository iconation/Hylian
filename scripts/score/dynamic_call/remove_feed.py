import json
import sys

if __name__ == '__main__':
    network = sys.argv[1]
    feed_address = sys.argv[2]
    score_address_txt = "./config/" + network + "/score_address.txt"

    call = json.loads(open("./calls/remove_feed.json", "rb").read())
    call["params"]["to"] = open(score_address_txt, "r").read()

    call["params"]["data"]["params"]["address"] = feed_address

    print(json.dumps(call))
