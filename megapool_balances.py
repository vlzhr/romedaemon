from requests import get
from json import loads, dumps


def get_balances_in_pools(tokenId="AP4Cb5xLYGH6ZigHreCZHoXpQTWDkPsG2BHqfDUx6taJ"):
    pools = loads(get("https://puzzle-js-back.herokuapp.com/api/v1/pools").text)
    result = {"balances": {}, "pools": {}}

    users = {}
    poolAddresses = [pool["contractAddress"] for pool in pools if tokenId in [asset["assetId"] for asset in pool["assets"]]]
    for address in poolAddresses:
        poolBalance = loads(get("https://nodes-puzzle.wavesnodes.com/addresses/balance/"+address).text)["balance"] if tokenId == "WAVES" else  loads(get("https://nodes-puzzle.wavesnodes.com/assets/balance/{}?id={}".format(address, tokenId)).text)["balances"][0]["balance"]
        data = loads(get("https://nodes-puzzle.wavesnodes.com/addresses/data/"+address).text)
        dic = {n["key"]: n["value"] for n in data}

        if not dic.get("global_indexStaked", 0) == 0:
            for n in dic:
                if "indexStaked" in n and not "global" in n:
                    users[n.split("_")[0]] = users.get(n.split("_")[0], 0) + int(poolBalance * dic[n] / dic["global_indexStaked"])

            print(address, poolAddresses.index(address) + 1)
        else:
            print("empty pool", address)

        result["pools"][address] = "PuzzleSwap"

    decimals = 1e6
    users = {n: users[n] / decimals for n in users if not users[n] == 0}
    result["balances"] = users

    return result

