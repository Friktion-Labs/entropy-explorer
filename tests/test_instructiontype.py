from .context import entropy


def test_instruction_type_init_entropy_group() -> None:
    actual = entropy.InstructionType(0)
    assert actual == entropy.InstructionType.InitEntropyGroup


def test_instruction_type_init_margin_account() -> None:
    actual = entropy.InstructionType(1)
    assert actual == entropy.InstructionType.InitMarginAccount


def test_instruction_type_deposit() -> None:
    actual = entropy.InstructionType(2)
    assert actual == entropy.InstructionType.Deposit


def test_instruction_type_withdraw() -> None:
    actual = entropy.InstructionType(3)
    assert actual == entropy.InstructionType.Withdraw


def test_instruction_type_add_to_spot_market() -> None:
    actual = entropy.InstructionType(4)
    assert actual == entropy.InstructionType.AddSpotMarket


def test_instruction_type_add_to_basket() -> None:
    actual = entropy.InstructionType(5)
    assert actual == entropy.InstructionType.AddToBasket


def test_instruction_type_borrow() -> None:
    actual = entropy.InstructionType(6)
    assert actual == entropy.InstructionType.Borrow


def test_instruction_type_cache_prices() -> None:
    actual = entropy.InstructionType(7)
    assert actual == entropy.InstructionType.CachePrices


def test_instruction_type_cache_root_banks() -> None:
    actual = entropy.InstructionType(8)
    assert actual == entropy.InstructionType.CacheRootBanks


def test_instruction_type_place_spot_order() -> None:
    actual = entropy.InstructionType(9)
    assert actual == entropy.InstructionType.PlaceSpotOrder


def test_instruction_type_add_oracle() -> None:
    actual = entropy.InstructionType(10)
    assert actual == entropy.InstructionType.AddOracle


def test_instruction_type_add_perp_market() -> None:
    actual = entropy.InstructionType(11)
    assert actual == entropy.InstructionType.AddPerpMarket


def test_instruction_type_place_perp_order() -> None:
    actual = entropy.InstructionType(12)
    assert actual == entropy.InstructionType.PlacePerpOrder


def test_instruction_type_cancel_perp_order_by_client_id() -> None:
    actual = entropy.InstructionType(13)
    assert actual == entropy.InstructionType.CancelPerpOrderByClientId


def test_instruction_type_cancel_perp_order() -> None:
    actual = entropy.InstructionType(14)
    assert actual == entropy.InstructionType.CancelPerpOrder


def test_instruction_type_consume_events() -> None:
    actual = entropy.InstructionType(15)
    assert actual == entropy.InstructionType.ConsumeEvents


def test_instruction_type_cache_perp_markets() -> None:
    actual = entropy.InstructionType(16)
    assert actual == entropy.InstructionType.CachePerpMarkets


def test_instruction_type_update_funding() -> None:
    actual = entropy.InstructionType(17)
    assert actual == entropy.InstructionType.UpdateFunding


def test_instruction_type_set_oracle() -> None:
    actual = entropy.InstructionType(18)
    assert actual == entropy.InstructionType.SetOracle


def test_instruction_type_settle_funds() -> None:
    actual = entropy.InstructionType(19)
    assert actual == entropy.InstructionType.SettleFunds


def test_instruction_type_cancel_spot_order() -> None:
    actual = entropy.InstructionType(20)
    assert actual == entropy.InstructionType.CancelSpotOrder


def test_instruction_type_update_root_bank() -> None:
    actual = entropy.InstructionType(21)
    assert actual == entropy.InstructionType.UpdateRootBank


def test_instruction_type_settle_pnl() -> None:
    actual = entropy.InstructionType(22)
    assert actual == entropy.InstructionType.SettlePnl


def test_instruction_type_settle_borrow() -> None:
    actual = entropy.InstructionType(23)
    assert actual == entropy.InstructionType.SettleBorrow
