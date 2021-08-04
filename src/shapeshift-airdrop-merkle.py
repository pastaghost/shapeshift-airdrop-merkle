import os
import requests
import csv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


""" Commented addresses below have been moved to the governance_token_addresses_especial
    dict as a temporary workaround until Covalent fixes their token_holders endpoint. We
    can fetch the data using the token_holders_changes endpoint instead and check the diff
    between the genesis block and block height defined below.

"""
governance_token_addresses = {
    # "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e": 39790.41,  # Yearn
    # "0xc00e94cb662c3520282e6f5717214004a7f26888": 359.37,  # Compound
    # "0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9": 328.55,  # Aave
    # "0x111111111117dc0aa78b770fa6a738034120c302": 3.05,  # 1inch
    # "0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2": 3217.32,  # Maker
    # "0xdbdb4d16eda451d0503b854cf79d55697f90c8df": 710.01,  # Alchemix
    # "0xe41d2489571d322189246dafa5ebde1f4699f498": 0.9521,  # 0x
    # "0xD533a949740bb3306d119CC777fa900bA034cd52": 2.367,  # Curve
    # "0xba100000625a3754423978a60c9317c58a424e3d": 25.37,  # Balancer
    # "0xde30da39c46104798bb5aa3fe8b9e0e1f348163f": 10.72,  # Gitcoin
    # "0x3472A5A71965499acd81997a54BBA8D852C6E53d": 13.91,  # BadgerDAO
}

governance_token_addresses_especial = {
    "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984": 23.78,  # Uniswap
    "0x6b3595068778dd592e39a122f4f5a5cf09c90fe2": 9.98,  # Sushiswap
    "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e": 39790.41,  # Yearn
    "0xc00e94cb662c3520282e6f5717214004a7f26888": 359.37,  # Compound
    "0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9": 328.55,  # Aave
    "0x111111111117dc0aa78b770fa6a738034120c302": 3.05,  # 1inch
    "0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2": 3217.32,  # Maker
    "0xdbdb4d16eda451d0503b854cf79d55697f90c8df": 710.01,  # Alchemix
    "0xe41d2489571d322189246dafa5ebde1f4699f498": 0.9521,  # 0x
    "0xD533a949740bb3306d119CC777fa900bA034cd52": 2.367,  # Curve
    "0xba100000625a3754423978a60c9317c58a424e3d": 25.37,  # Balancer
    "0xde30da39c46104798bb5aa3fe8b9e0e1f348163f": 10.72,  # Gitcoin
    "0x3472A5A71965499acd81997a54BBA8D852C6E53d": 13.91,  # BadgerDAO
}

# Get historical price information by block height for these and apply threshold
# Price information from Zerion
lp_token_addresses = {
    "0xd3d2e2692501a5c9ca623199d38826e513033a17": 1059.31,  # UNI-ETH UniswapV2
    "0x5aa90c7362ea46b3cbfbd7f01ea5ca69c98fef1c": 256.99,  # UNI-ETH Balancer
    "0x795065dcc9f64b5614c407a6efdc400da6221fb0": 389.19,  # Sushi-ETH Sushiswap
    "0xce84867c3c02b05dc570d0135103d3fb9cc19433": 633.60,  # Sushi-ETH UniswapV2
    "0x088ee5007c98a9677165d78dd2109ae4a3d04d0c": 35081.13,  # YFI-ETH Sushiswap
    "0x2fdbadf3c4d5a8666bc06645b8358ab803996e28": 43555.28,  # YFI-ETH UniswapV2
    "0x31503dcb60119a812fee820bb7042752019f2355": 2606.97,  # COMP-ETH Sushiswap
    "0xefaa1604e82e1b3af8430b90192c1b9e8197e377": 976.25,  # COMP-ETH Balancer
    "0xd75ea151a61d06868e31f8988d28dfe5e9df57b4": 2033.14,  # AAVE-ETH Sushiswap
    "0xdfc14d2af169b0d36c4eff567ada9b2e0cae044f": 2221.05,  # AAVE-ETH Uniswap V2
    "0xc3f279090a47e80990fe3a9c30d24cb117ef91a8": 2892.92,  # ALCX-ETH Sushiswap
    "0x0ef1b8a0e726fc3948e15b23993015eb1627f210": 6.91,  # 1inch-ETH 1inch
    "0xd471b6755eba924ad94dd9144ea50022010efccc": 10.47,  # 1inch-VSP 1inch
    "0x0bc5ae46c32d99c434b7383183aca16dd6e9bdc8": 104.43,  # ZRX-WETH Sushiswap
    "0xc6f348dd3b91a56d117ec0071c1e9b83c0996de4": 137.88,  # ZRX-ETH UniswapV2
    "0x33f6ddaea2a8a54062e021873bcaee006cdf4007": 4.99,  # cvxCRV-CRV Sushiswap
    "0x58dc5a51fe44589beb22e8ce67720b5bc5378009": 574.18,  # WETH-CRV Sushiswap
    "0x5c6ee304399dbdb9c8ef030ab642b10820db8f56": 54.58,  # 80BAL-20ETH Balancer
    "0xa70d458a4d9bc0e6571565faee18a48da5c0d593": 939.19,  # BAL-ETH Uniswapv2
    "0xba13afecda9beb75de5c56bbaf696b880a5a50dd": 6196.95,  # MKR-ETH Sushiswap
    "0xc2adda861f89bbb333c90c492cb837741916a225": 7294.81,  # MKR-ETH Uniswap v2
    "0xa3509a16bbfc5992eb01cc861b615ccd8e937da8": 458.46,  # ETH-GTC Uniswapv2
    "0xcd7989894bc033581532d2cd88da5db0a4b12859": 155113262.53,  # BADGER-WBTC Uniswapv2
    "0x110492b31c59716ac47337e616804e3e3adc0b4a": 143945303.72,  # BADGER-WBTC Sushiswap
}

# Contract address, followed by list of function hashes for stake/withdraw methods.
# (Curve is a special case and has create lock, withdraw, and increase amount methods)
staking_contract_addresses = {
    "0xBa37B002AbaFDd8E89a1995dA52740bbC013D992": [
        "a694fc3a",
        "2e1a7d4d",
    ],  # Yearn stakers deposit governance tokens into the yearn staking contract
    "0xAB8e74017a8Cc7c15FFcCd726603790d26d7DeCa": [
        "e2bbb158",
        "441a3e70",
    ],  # ALCX stakers deposit ALCX in the Alchemix staking contract
    "0x5f3b5DfEb7B28CDbD7FAba78963EE202a494e2A2": [
        "65fc3873",
        "3ccfd60b",
        "4957677c",
    ],  # Curve stakers lock CRV into the veCRV contract
}

staking_tokens = [
    "0x8798249c2e607446efb7ad49ec89dd1865ff4272",  # Sushi stakers are issued xSUSHI tokens
    "0x4da27a545c0c5b758a6ba100e3a049001de870f5",  # AAVE stakers hold staked AAVE (stkAAVE) tokens
    "0x19d97d8fa813ee2f51ad4b4e04ea08baf4dffc28",  # BadgerDAO stakers are given bBadger tokens
    "0xa0446d8804611944f1b527ecd37d7dcbe442caba",  # 1Inch stakers hold staked 1Inch (stk1Inch) tokens
    "0xc3f279090a47e80990fe3a9c30d24cb117ef91a8",  # SushiSwap ETH/ALCX stakers hold ETH/ALCX LP tokens
]


balance_threshold = 1500
block_height = 12597000  # Timestamp=1623196855, 2021-06-09:12:00:55 GMT
etherscan_pro_api_key = os.environ.get("ETHERSCAN_PRO_API_KEY")
covalent_api_key = os.environ.get("COVALENT_API_KEY")

eligible_addresses = []


''' The Covalent API calls frequently time out, so the GET requests should be automatically retried in the 
    event that non-200 status codes are returned.
'''
retry_strategy = Retry(
    total=100,
    status_forcelist=[400, 429, 500, 502, 503, 504, 524],
    method_whitelist=["HEAD", "GET", "OPTIONS"],
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)


def get_governance_token_holders():
    for key in governance_token_addresses:
        page_number = 0
        page_size = 10000
        has_more = True
        while has_more:
            r = http.get(
                f"https://api.covalenthq.com/v1/1/tokens/{key}/token_holders/?block-height={block_height}&key={covalent_api_key}&page-number={page_number}&page-size={page_size}"
            )
            if r.status_code == 200:
                request_payload = r.json()
                if len(request_payload["data"]["items"]):
                    total_count = request_payload["data"]["pagination"]["total_count"]
                    range_lower = (page_number * page_size) + 1
                    range_upper = (
                        (page_number + 1) * page_size
                        if (page_number + 1) * page_size < total_count
                        else total_count
                    )
                    print(
                        f"Fetching accounts holding {request_payload['data']['items'][0]['contract_ticker_symbol']} governance token. ({range_lower}-{range_upper} of {total_count})"
                    )
                else:
                    continue
                for holder in request_payload["data"]["items"]:
                    address_balance = (
                        int(holder["balance"])
                        / (10 ** holder["contract_decimals"])
                        * governance_token_addresses[key]
                    )
                    if address_balance >= balance_threshold:
                        eligible_addresses.append(holder["address"])
                has_more = request_payload["data"]["pagination"]["has_more"]
                page_number += 1
            else:
                print(f"Request returned non-success code {r.status_code}")
                break
    get_governance_token_holders_especial()


def get_governance_token_holders_especial():
    """The API called in the get_governance_token_holders function fails for Uniswap and Sushiswap since
    the list of token holders is so large. As a workaround, the same data can be extracted for these contracts
    can be extracted using a different endpoint and some fanagling of the returned data."""
    for key in governance_token_addresses_especial:
        page_number = 0
        page_size = 50000
        has_more = True
        while has_more:
            r = http.get(
                f"https://api.covalenthq.com/v1/1/tokens/{key}/token_holders_changes/?starting-block=1&ending-block={block_height}&key={covalent_api_key}&page-number={page_number}&page-size={page_size}"
            )
            if r.status_code == 200:
                request_payload = r.json()
                if len(request_payload["data"]["items"]):
                    total_count = request_payload["data"]["pagination"]["total_count"]
                    range_lower = (page_number * page_size) + 1
                    range_upper = (
                        (page_number + 1) * page_size
                        if (page_number + 1) * page_size < total_count
                        else total_count
                    )
                    print(
                        f"Fetching accounts holding governance token with address: {key}. ({range_lower}-{range_upper} of {total_count})"
                    )
                else:
                    continue
                for item in request_payload["data"]["items"]:
                    address_balance = (
                        int(item["next_balance"])
                        / (
                            10 ** 18
                        )  # We really should get this dynamically, but this only applies to UNI/SUSHI for now
                        * governance_token_addresses_especial[key]
                    )
                    if address_balance >= balance_threshold:
                        eligible_addresses.append((item["token_holder"]))
                has_more = request_payload["data"]["pagination"]["has_more"]
                page_number += 1
            else:
                print(f"Request returned non-success code {r.status_code}")
                break


def get_lp_token_holders():
    for key in lp_token_addresses:
        page_number = 0
        page_size = 10000
        has_more = True
        while has_more:
            r = http.get(
                f"https://api.covalenthq.com/v1/1/tokens/{key}/token_holders/?block-height={block_height}&key={covalent_api_key}&page-number={page_number}&page-size={page_size}"
            )
            if r.status_code == 200:
                request_payload = r.json()
                if len(request_payload["data"]["items"]):
                    total_count = request_payload["data"]["pagination"]["total_count"]
                    range_lower = (page_number * page_size) + 1
                    range_upper = (
                        (page_number + 1) * page_size
                        if (page_number + 1) * page_size < total_count
                        else total_count
                    )
                    print(
                        f"Fetching accounts holding {request_payload['data']['items'][0]['contract_ticker_symbol']} LP token. ({range_lower}-{range_upper} of {total_count})"
                    )
                else:
                    continue
                for holder in request_payload["data"]["items"]:
                    address_balance = (
                        int(holder["balance"])
                        / (10 ** holder["contract_decimals"])
                        * lp_token_addresses[key]
                    )
                    if address_balance >= balance_threshold:
                        eligible_addresses.append(holder["address"])
                has_more = request_payload["data"]["pagination"]["has_more"]
                page_number += 1
            else:
                print(f"Request returned non-success code {r.status_code}")
                break


def get_staking_token_holders():
    for token in staking_tokens:
        page_number = 0
        page_size = 10000
        has_more = True
        while has_more:

            r = http.get(
                f"https://api.covalenthq.com/v1/1/tokens/{token}/token_holders/?block-height={block_height}&key={covalent_api_key}&page-number={page_number}&page-size={page_size}"
            )
            if r.status_code == 200:
                request_payload = r.json()
                if len(request_payload["data"]["items"]):
                    total_count = request_payload["data"]["pagination"]["total_count"]
                    range_lower = (page_number * page_size) + 1
                    range_upper = (
                        (page_number + 1) * page_size
                        if (page_number + 1) * page_size < total_count
                        else total_count
                    )
                    print(
                        f"Fetching accounts holding {request_payload['data']['items'][0]['contract_ticker_symbol']} staking token. ({range_lower}-{range_upper} of {total_count})"
                    )
                else:
                    continue
                for holder in request_payload["data"]["items"]:
                    eligible_addresses.append(holder["address"])
                has_more = request_payload["data"]["pagination"]["has_more"]
                page_number += 1
            else:
                print(f"Request returned non-success code {r.status_code}")
                break


def remove_duplicates():
    global eligible_addresses
    eligible_addresses = list(set(eligible_addresses))


def remove_airdropped_addresses(from_file=False):
    addresses = []
    global eligible_addresses
    with open(
        os.path.join(os.path.dirname(__file__), "../data/airdrop_addresses.csv")
    ) as f:
        airdropped_addresses = [row.split(",")[0] for row in f]
    if from_file:
        with open(
            os.path.join(os.path.dirname(__file__), "../data/eligible_addresses.csv")
        ) as f:
            addresses = [row.split(",")[0] for row in f]
    else:
        addresses = eligible_addresses
    eligible_addresses = list(set(addresses) - set(airdropped_addresses))


def write_to_csv():
    with open(
        os.path.join(os.path.dirname(__file__), "../data/eligible_addresses.csv"), "w"
    ) as f:
        csvwriter = csv.writer(f)
        csvwriter.writerows([[address, "200"] for address in eligible_addresses])


def get_erc20_transfer_events(address):
    transactions = []
    method_ids = staking_contract_addresses[address]
    data_remaining = True
    page = 0
    print(f"Getting accounts with tokens staked in contract: {address}")
    while data_remaining:
        r = http.get(
            f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock={block_height}&apikey={etherscan_pro_api_key}&sort=asc&page={page}&offset={page * 10000}"
        )
        if r.status_code == 200:
            request_payload = r.json()
            if request_payload["result"] == None:
                break
            if len(request_payload["result"]):
                transactions += [
                    tx
                    for tx in request_payload["result"]
                    if tx["input"][2:10] in method_ids
                ]
                page += 1
            else:
                print("Request payload has no length")
                break
        else:
            print(f"Request returned non-success code {r.status_code}")
            print(r)
    return transactions


def filter_staked_addresses_by_deposit_activity(contract_address, transactions):
    addresses = []
    deposit_method = staking_contract_addresses[contract_address][0]
    increase_balance_method = (
        staking_contract_addresses[contract_address][2]
        if contract_address == "0x5f3b5DfEb7B28CDbD7FAba78963EE202a494e2A2"
        else "XXXXXXXX"
    )
    addresses = [
        tx["from"]
        for tx in transactions
        if tx["input"][2:10] in [deposit_method, increase_balance_method]
    ]

    return addresses


def get_addresses_with_staked_tokens():
    addresses = []
    for key in staking_contract_addresses:
        transactions = get_erc20_transfer_events(key)
        addresses += filter_staked_addresses_by_deposit_activity(key, transactions)

    global eligible_addresses
    eligible_addresses += addresses


if __name__ == "__main__":
    get_governance_token_holders()
    get_lp_token_holders()
    get_staking_token_holders()
    get_addresses_with_staked_tokens()
    remove_duplicates()
    remove_airdropped_addresses()
    write_to_csv()