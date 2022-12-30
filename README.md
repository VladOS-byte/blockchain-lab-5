# blockchain-lab-5
## Requirements
- python3
- eth-brownie
## Pre-usage
- install brownie
- [create](https://eth-brownie.readthedocs.io/en/stable/network-management.html?highlight=network#using-a-forked-development-network) fork mainnet network in brownie
## Usage
- For test use
```
brownie test -s --disable-warnings --network mainnet-fork
```
## Output
- For test
```
MBP-Vlad-2:blockchain-lab-5 vlad$ brownie test -s --disable-warnings --network mainnet-fork
Brownie v1.19.2 - Python development framework for Ethereum

================================= test session starts ==================================
platform darwin -- Python 3.8.9, pytest-6.2.5, py-1.11.0, pluggy-1.0.0 -- /Library/Developer/CommandLineTools/usr/bin/python3
cachedir: .pytest_cache
hypothesis profile 'brownie-verbose' -> verbosity=2, deadline=None, max_examples=50, stateful_step_count=10, report_multiple_bugs=False, database=DirectoryBasedExampleDatabase(PosixPath('/Users/vlad/.brownie/hypothesis'))
rootdir: /Users/vlad/GitHub/alchemy-ethereum-api/blockchain-lab-5
plugins: eth-brownie-1.19.2, anyio-3.6.1, forked-1.4.0, web3-5.31.1, xdist-1.34.0, hypothesis-6.27.3
collected 12 items                                                                     

Launching 'ganache-cli --accounts 10 --hardfork istanbul --fork https://eth-mainnet.alchemyapi.io/v2/API --gasLimit 12000000 --mnemonic brownie --port 8545 --chainId 1'...

tests/test_voter.py::test_transfer PASSED
tests/test_voter.py::test_empty_proposal PASSED
tests/test_voter.py::test_vote_for_undefined_proposal RUNNING
Transaction sent: 0x4be392701506fc61575c75a694ae51d267da892cb5c469f1014f2845c007df1d
tests/test_voter.py::test_vote_for_undefined_proposal PASSED
tests/test_voter.py::test_vote_for_default_proposal RUNNING
Transaction sent: 0x53b8bf0f414a04fb008e3ad41ce868c00872363b58491f37c339f994ea8386aa
tests/test_voter.py::test_vote_for_default_proposal PASSED
tests/test_voter.py::test_propose PASSED
tests/test_voter.py::test_proposes PASSED
tests/test_voter.py::test_much_propose RUNNING
Transaction sent: 0x586941c861cbe8894c5d2ed909b6152885da16a5074268bebcec4ab8b38d23b8
tests/test_voter.py::test_much_propose PASSED
tests/test_voter.py::test_propose_after_vote PASSED
tests/test_voter.py::test_vote_for_amount PASSED
tests/test_voter.py::test_vote_already_gained RUNNING
Transaction sent: 0xd4492f401b03fd73955f62ecdb97b11ea419ba1ba29706df0b3a4e881dfc7fbd
tests/test_voter.py::test_vote_already_gained PASSED
tests/test_voter.py::test_vote_too_much_amount RUNNING
Transaction sent: 0xf951f6f2563609c289f804fe19337f434d58a950f9d635794dd825af8236703b
tests/test_voter.py::test_vote_too_much_amount PASSED
tests/test_voter.py::test_vote_and_transfer PASSED

============================ 12 passed in 60.18s (0:01:00) =============================
Terminating local RPC client...
```
