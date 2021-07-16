import os
import requests
import csv
from time import sleep

'''
Questions:

1.) Can you provide some clarification on the instruction:
        "Staked tokens to be included: any of the above projects that offer single asset staking for rewards and/or governance"
    Do you want me to find all addresses who have staked any of their governance tokens in any contracts at all?
    I can see all transfer calls to this contract, and I can see whether the destination was a wallet address or a contract, 
    but how can I know for sure whether the destination contract is a staking contract?

'''

governance_token_addresses = {
    "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984": 23.78,  # Uniswap
    "0x6b3595068778dd592e39a122f4f5a5cf09c90fe2": 9.98,  # Sushiswap
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

lp_token_addresses = [
    "0x9928e4046d7c6513326ccea028cd3e7a91c7590a",  # UniswapV2 FEI/TRIBE
    "0x94b0a3d511b6ecdb17ebf877278ab030acb0a878",  # UniswapV2 FEI/ETH
    "0xceff51756c56ceffca006cd410b03ffc46dd3a58",  # SushiSwap WBTC/WETH
    "0x397ff1542f962076d0bfe58ea045ffa2d347aca0",  # SushiSwap USDC/WETH
    "0x0ef1b8a0e726fc3948e15b23993015eb1627f210",  # 1Inch ETH/1INCH
    "0xd471b6755eba924ad94dd9144ea50022010efccc",  # 1Inch 1INCH/VSP
    "0xa6f548df93de924d73be7d25dc02554c6bd66db5",  # Balancer 50 WBTC 50 WETH
    "0x06df3b2bbb68adc8b0e302443692037ed9f91b42",  # Balancer USD Stable Pool
]


balance_threshold = 1500
block_height = 12597000
network = "Ethereum"
etherscan_pro_api_key = os.environ.get["ETHERSCAN_PRO_API_KEY"]

eligible_addresses = []


def get_governance_token_holders():
    for key in governance_token_addresses:
        r = requests.get(
            f"https://api.etherscan.io/api?module=stats&action=tokensupplyhistory&contractaddress={key}&blockno={block_height}&apikey={etherscan_pro_api_key}"
        ).json()
        for address in r.holders:
            address_balance = address.quantity * governance_token_addresses[key]
            if address_balance >= balance_threshold:
                eligible_addresses.append(address)
        sleep(600)  # API is rate limited to 2 calls/sec


def get_lp_token_holders():
    for address in lp_token_addresses:
        r = requests.get(
            f"https://api.etherscan.io/api?module=stats&action=tokensupplyhistory&contractaddress={key}&blockno={block_height}&apikey={etherscan_pro_api_key}"
        ).json()
        eligible_addresses.append(address)
        sleep(600)  # API is rate limited to 2 calls/sec


def remove_duplicates():
    global eligible_addresses
    eligible_addresses = list(set(eligible_addresses))


def remove_airdropped_addresses():
    with open("../data/airdropped_addresses.csv") as f:
        airdropped_addresses = [row.split()[0] for row in f]
    global eligible_addresses
    eligible_addresses = list(set(eligible_addresses) - set(airdropped_addresses))


def write_to_csv():
    with open("../data/eligible_addresses.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerows([[address, "200"] for address in eligible_addresses])


if __name__ == "__main__":
    get_governance_token_holders()
    get_lp_token_holders()
    remove_duplicates()
    remove_airdropped_addresses()
    write_to_csv()