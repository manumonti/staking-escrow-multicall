import json
from multicall import Call, Multicall

STAKING_ESCROW = "0xbbD3C0C794F40c4f993B03F65343aCC6fcfCb2e2"
WALLET_REGISTRY = "0x46d52E41C2F300BC82217Ce22b920c34995204eb"


def toStakingProvider(info):
    return {"value": info[0], "stakingProvider": info[11]}


def main():
    staker_list = {}

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
        call_result = multicall()
        staker_list = {**staker_list, **call_result}


    staker_with_st_prov_list = {}

    for stake in staker_list:
        staking_provider = staker_list[stake]["stakingProvider"]
        if staking_provider == "0x0000000000000000000000000000000000000000":
            staker_list[stake]["tBTC"] = 0
        else:
            staker_with_st_prov_list[stake] = staker_list[stake]

    calls = []
    for stake in staker_with_st_prov_list:
        staking_provider = staker_with_st_prov_list[stake]["stakingProvider"]
        calls.append(
            Call(
                WALLET_REGISTRY,
                ["eligibleStake(address)(uint96)", staking_provider],
                [(stake, None)],
            )
        )

    multicall = Multicall(calls)
    call_result = multicall()

    for stake in staker_with_st_prov_list:
        staker_with_st_prov_list[stake]["tBTC"] = call_result[stake]

    staker_list.update(staker_with_st_prov_list)

    staker_list_json = json.dumps(staker_list, indent=2)

    with open("staker_list.json", "w") as file:
        file.write(staker_list_json)
        file.close()

if __name__ == "__main__":
    main()
