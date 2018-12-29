class Token():
    """
    Contains NEO Alias Coin specification
    NAC name and symbol is are not definitive and will be consulted with
    community
    """
    name = "Neo Alias Coin"
    symbol = "NAC"
    decimals = 8

    in_circulation_key = b'in_circulation'

    total_supply = 1000000000 * 100000000  # 1000m total supply * 10^8 ( decimals)