import json
from multicall import Call, Multicall

STAKING_ESCROW = "0xbbD3C0C794F40c4f993B03F65343aCC6fcfCb2e2"


def toStakingProvider(info):
    return {"value": info[0], "stakingProvider": info[11]}


def main():
    result = {}

    with open("mainnet-stakers.txt") as file:
        mainnet_stakers = [line.rstrip('\n') for line in file]

    chunk_size = 500
    chunk_list = []

    for i in range(0, len(mainnet_stakers), chunk_size):
        chunk_list.append(mainnet_stakers[i:i+chunk_size])

    for chunk in chunk_list:
        calls = []

        for line in chunk:
            index, address = line.split(' ')
            calls.append(
                Call(
                    STAKING_ESCROW,
                    [
                        "stakerInfo(address)((uint256,uint16,uint16,uint16,uint16,uint256,uint16,address,uint256,uint256,uint256,address,uint256,uint256))",
                        address,
                    ],
                    [(address, toStakingProvider)],
                )
            )

        multicall = Multicall(calls)
        callResult = multicall()
        result = {**result, **callResult}

    json_file = json.dumps(result, indent=2)
    print(json_file)

if __name__ == "__main__":
    main()
