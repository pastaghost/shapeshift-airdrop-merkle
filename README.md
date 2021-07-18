Submission for Gitcoin Bounty: https://gitcoin.co/issue/shapeshift/airdrop-merkle/1/100026107

Somewhat quick and dirty, also not very Pythonic, but this is a one-time-use script.

To run, set environment variables ETHERSCAN_PRO_API_KEY and COVALENT API KEY, then run python3 src/shapeshift-airdrop-merkle.py



As discussed in the ShapeShift discord and forum, there is a proposal developing to issue a new airdrop contract rewarding members of the original 13 DAO communities whose governance tokens were staked or deposited in liquidity pools at the time of the snapshot.

More info: https://forum.shapeshift.com/t/mini-airdrop-to-dao-communities-who-were-missed-due-to-staking-or-lping/96/3

This is a bounty to assemble the list of addresses that should be included according to the parameters described below:

DAO communities that should be included and token price to use for threshold calculation:
Uniswap (0x1f9840a85d5af5bf1d1762f925bdaddc4201f984) - $23.78
Sushiswap (0x6b3595068778dd592e39a122f4f5a5cf09c90fe2) - $9.98
Yearn (0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e) - $39,790.41
Compound (0xc00e94cb662c3520282e6f5717214004a7f26888) - $359.37
Aave (0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9) - $328.55
Alchemix (0xdbdb4d16eda451d0503b854cf79d55697f90c8df) - $710.01
1inch (0x111111111117dc0aa78b770fa6a738034120c302) - $3.05
0x (0xe41d2489571d322189246dafa5ebde1f4699f498) - $0.9521
Curve (0xD533a949740bb3306d119CC777fa900bA034cd52) - $2.367
Balancer (0xba100000625a3754423978a60c9317c58a424e3d) - $25.37
Maker (0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2) - $3,217.32
Gitcoin (0xde30da39c46104798bb5aa3fe8b9e0e1f348163f) - $10.72
BadgerDAO (0x3472A5A71965499acd81997a54BBA8D852C6E53d) - $13.91
Threshold of token balance to be included: $1,500 at the above prices (not including the paired asset in an LP position)
Block height for snapshot: 12597000
Network: Ethereum
Liquidity pools to be included: top 2 liquidity pools by TVL on either Uniswap, Sushiswap, 1inch, or Balancer
Staked tokens to be included: any of the above projects that offer single asset staking for rewards and/or governance
Steps to completing this bounty:

Organize list of staking contracts and liquidity pools that should be excluded
Filter out duplicates
Filter out DAO community members that already received the 200 FOX airdrop (.csv attached)
Deliver a csv with all eligible addresses in column A and 200 in column b, ie. (0x05A1ff0a3.....A6cb2011c, 200, etc.) as well as details of which staking contracts and liquidity pools were included.