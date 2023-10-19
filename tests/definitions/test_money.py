import pytest

from disquant.definitions.money import Currency, Money


def test_init():
    money = Money(10_000_000, Currency.EUR)

    assert money.amount == 10_000_000
    assert money.currency == Currency.EUR


def test_eq():
    amount_1 = Money(10_000_000, Currency.EUR)
    amount_2 = Money(10_000_000, Currency.EUR)

    assert amount_1 is not amount_2
    assert amount_1 == amount_2


def test_lt():
    amount_1 = Money(9_000_000, Currency.EUR)
    amount_2 = Money(10_000_000, Currency.EUR)

    assert amount_1 < amount_2


def test_total_ordering():
    amount_1 = Money(9_000_000, Currency.EUR)
    amount_2 = Money(10_000_000, Currency.EUR)
    amount_3 = Money(10_000_000, Currency.EUR)

    assert amount_1 < amount_2
    assert amount_2 <= amount_3
    assert amount_2 == amount_3
    assert amount_2 > amount_1
    assert amount_3 >= amount_2
    assert amount_3 > amount_1
    assert amount_1 != amount_3


def test_sort():
    asc_amounts = []
    for i in range(1, 10):
        asc_amounts.append(Money(i * 1_000_000, Currency.EUR))

    desc_amounts = sorted(asc_amounts.copy(), reverse=True)

    assert sorted(desc_amounts) == asc_amounts


def test_different_currency_raises_exception():
    amount_eur = Money(10_000_000, Currency.EUR)
    amount_usd = Money(10_000_000, Currency.USD)

    with pytest.raises(ValueError):
        assert amount_eur == amount_usd


def test_add():
    amount_1 = Money(9_000_000, Currency.EUR)
    amount_2 = Money(10_000_000, Currency.EUR)

    assert amount_1 + amount_2 == Money(19_000_000, Currency.EUR)


def test_invalid_add():
    amount_1 = Money(9_000_000, Currency.EUR)
    amount_2 = Money(10_000_000, Currency.USD)

    with pytest.raises(ValueError):
        amount_3 = amount_1 + amount_2


def test_sub():
    amount_1 = Money(9_000_000, Currency.EUR)
    amount_2 = Money(10_000_000, Currency.EUR)

    assert amount_1 - amount_2 == Money(-1_000_000, Currency.EUR)


def test_invalid_sub():
    amount_1 = Money(9_000_000, Currency.EUR)
    amount_2 = Money(10_000_000, Currency.USD)

    with pytest.raises(ValueError):
        amount_3 = amount_1 - amount_2


def test_hash():
    """
    Money is a hashable object so it can be used as a
    dictionary key.
    """
    amount = Money(10_000_000, Currency.EUR)
    thresholds = {amount: "CATEGORY"}

    assert isinstance(thresholds, dict)


def test_round():
    amount_1 = Money("9.6", Currency.EUR)

    assert round(amount_1, 0) == Money(10, Currency.EUR)
