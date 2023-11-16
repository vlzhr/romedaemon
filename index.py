from megapool_balances import get_balances_in_pools
from requests import get
from json import loads, dumps

ROME = "AP4Cb5xLYGH6ZigHreCZHoXpQTWDkPsG2BHqfDUx6taJ"

height = str(loads(get("https://nodes.wavesnodes.com/blocks/height").text)["height"] - 1)


def get_rome_distribution():
    balances = loads(get("https://nodes.wavesnodes.com/assets/{}/distribution/{}/limit/1000".format(ROME, height)).text)["items"]

    from_pools = get_balances_in_pools(ROME)
    balances2 = from_pools["balances"]
    ignore_list = from_pools["pools"]

    result_dic = {}
    for address in balances:
        if not address in ignore_list:
            result_dic[address] = balances[address] / 1e6

    for address in balances2:
        result_dic[address] = result_dic.get(address, 0) + balances2[address]
