import os
import requests
import csv



governance_token_addresses = {
    # "0x19d97d8fa813ee2f51ad4b4e04ea08baf4dffc28": 1,  # Test
    "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e": 39790.41,  # Yearn
    "0xc00e94cb662c3520282e6f5717214004a7f26888": 359.37,  # Compound
    "0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9": 328.55,  # Aave
    "0xdbdb4d16eda451d0503b854cf79d55697f90c8df": 710.01,  # Alchemix
    "0x111111111117dc0aa78b770fa6a738034120c302": 3.05,  # 1inch
    "0xe41d2489571d322189246dafa5ebde1f4699f498": 0.9521,  # 0x
    "0xD533a949740bb3306d119CC777fa900bA034cd52": 2.367,  # Curve
    "0xba100000625a3754423978a60c9317c58a424e3d": 25.37,  # Balancer
    "0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2": 3217.32,  # Maker
    "0xde30da39c46104798bb5aa3fe8b9e0e1f348163f": 10.72,  # Gitcoin
    "0x3472A5A71965499acd81997a54BBA8D852C6E53d": 13.91,  # BadgerDAO
}

governance_token_addresses_especial = {
    "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984": 23.78,  # Uniswap
    "0x6b3595068778dd592e39a122f4f5a5cf09c90fe2": 9.98,  # Sushiswap
}

# Get historical price information by block height for these and apply threshold
# Price information from Zerion
lp_token_addresses = {
    "0x9928e4046d7c6513326ccea028cd3e7a91c7590a": 1.15,  # UniswapV2 FEI/TRIBE
    "0x94b0a3d511b6ecdb17ebf877278ab030acb0a878": 103.61,  # UniswapV2 FEI/ETH
    "0xceff51756c56ceffca006cd410b03ffc46dd3a58": 47950857827.66,  # SushiSwap WBTC/WETH
    "0x397ff1542f962076d0bfe58ea045ffa2d347aca0": 143525203.84,  # SushiSwap USDC/WETH
    "0x0ef1b8a0e726fc3948e15b23993015eb1627f210": 6.91,  # 1Inch ETH/1INCH
    "0xd471b6755eba924ad94dd9144ea50022010efccc": 10.47,  # 1Inch 1INCH/VSP
    "0xa6f548df93de924d73be7d25dc02554c6bd66db5": 9956.92,  # Balancer 50 WBTC 50 WETH
    "0x5c6ee304399dbdb9c8ef030ab642b10820db8f56": 54.58,  # Balancer 80 BAL 20 WETH
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
]


balance_threshold = 1500
block_height = 12597000  # Timestamp=1623196855, 2021-06-09:12:00:55 GMT
etherscan_pro_api_key = os.environ.get("ETHERSCAN_PRO_API_KEY")
covalent_api_key = os.environ.get("COVALENT_API_KEY")

eligible_addresses = []


def get_governance_token_holders():
    for key in governance_token_addresses:
        r = requests.get(
            f"https://api.covalenthq.com/v1/1/tokens/{key}/token_holders/?block-height={block_height}&key={covalent_api_key}"
        )
        if r.status_code == 200:
            request_payload = r.json()
            if len(request_payload["data"]["items"]):
                print(
                    f"Fetching holders for {request_payload['data']['items'][0]['contract_ticker_symbol']} governance token"
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
        else:
            print(f"Request returned non-success code: {r.status_code}")
            print(r)
    get_governance_token_holders_especial()


def get_governance_token_holders_especial():
    """The API called in the get_governance_token_holders function fails for Uniswap and Sushiswap since
    the list of token holders is so large. As a workaround, the same data can be extracted for these contracts
    can be extracted using a different endpoint and some fanagling of the returned data."""
    for key in governance_token_addresses_especial:
        print(f"Fetching holders for governance token with address: {key}")
        r = requests.get(
            f"https://api.covalenthq.com/v1/1/tokens/{key}/token_holders_changes/?starting-block=1&ending-block={block_height}&key={covalent_api_key}"
        )
        if r.status_code == 200:
            request_payload = r.json()
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
        else:
            print(f"Request returned non-success code: {r.status_code}")
            print(r)


def get_lp_token_holders():
    for key in lp_token_addresses:
        r = requests.get(
            f"https://api.covalenthq.com/v1/1/tokens/{key}/token_holders/?block-height={block_height}&key={covalent_api_key}"
        )
        if r.status_code == 200:
            request_payload = r.json()
            if len(request_payload["data"]["items"]):
                print(
                    f"Fetching holders for {request_payload['data']['items'][0]['contract_ticker_symbol']} LP token"
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
        else:
            print(f"Request returned non-success code: {r.status_code}")
            print(r)


def get_staking_token_holders():
    for token in staking_tokens:
        r = requests.get(
            f"https://api.covalenthq.com/v1/1/tokens/{token}/token_holders/?block-height={block_height}&key={covalent_api_key}"
        )
        if r.status_code == 200:
            request_payload = r.json()
            if len(request_payload["data"]["items"]):
                print(
                    f"Fetching holders for {request_payload['data']['items'][0]['contract_ticker_symbol']} staking token"
                )
            else:
                continue
            for holder in request_payload["data"]["items"]:
                eligible_addresses.append(holder["address"])
        else:
            print(f"Request returned non-success code: {r.status_code}")
            print(r)


def remove_duplicates():
    global eligible_addresses
    eligible_addresses = list(set(eligible_addresses))


def remove_airdropped_addresses():
    with open(
        os.path.join(os.path.dirname(__file__), "../data/airdropped_addresses.csv")
    ) as f:
        airdropped_addresses = [row.split(",")[0] for row in f]
    global eligible_addresses
    eligible_addresses = list(set(eligible_addresses) - set(airdropped_addresses))


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
        r = requests.get(
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
            print(f"Request returned non-success code: {r.status_code}")
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


def index_token_transfers(address):
    r = requests.get(
        f"https://api.covalenthq.com/v1/1/address/{address}/transactions_v2/?&key={covalent_api_key}"
    )
    if r.status_code == 200:
        request_payload = r.json()
        print(f"Fetching transactions for contract address: {address}")
        token_transfers = [
            tx
            for tx in request_payload["data"]["items"]
            if tx["log_events"]["decoded"]["name"] == "Transfer"
        ]
        print(token_transfers[:2])
    else:
        print(f"Request returned non-success code: {r.status_code}")


if __name__ == "__main__":
    get_governance_token_holders()
    get_lp_token_holders()
    get_staking_token_holders()
    get_addresses_with_staked_tokens()
    remove_duplicates()
    remove_airdropped_addresses()
    write_to_csv()