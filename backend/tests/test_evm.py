from decimal import Decimal

from app.evm import calculate_activity, calculate_project


def test_activity_calculation():
    result = calculate_activity(
        Decimal("100000"),
        Decimal("60"),
        Decimal("40"),
        Decimal("70000"),
    )

    assert result["pv"] == Decimal("60000.00")
    assert result["ev"] == Decimal("40000.00")
    assert result["cv"] == Decimal("-30000.00")
    assert result["sv"] == Decimal("-20000.00")
    assert result["cpi"] == Decimal("0.5714")
    assert result["spi"] == Decimal("0.6667")
    assert result["eac"] == Decimal("175000.00")
    assert result["vac"] == Decimal("-75000.00")
    assert result["cpi_status"] == "over_budget"
    assert result["spi_status"] == "behind"


def test_zero_actual_cost_returns_no_cpi():
    result = calculate_activity(Decimal("100"), Decimal("50"), Decimal("25"), Decimal("0"))
    assert result["cpi"] is None
    assert result["eac"] is None
    assert result["vac"] is None
    assert result["cpi_status"] == "not_available"


def test_zero_planned_value_returns_no_spi():
    result = calculate_activity(Decimal("100"), Decimal("0"), Decimal("25"), Decimal("20"))
    assert result["spi"] is None
    assert result["spi_status"] == "not_available"


def test_empty_project_returns_zero_values():
    result = calculate_project([])
    assert result["pv"] == Decimal("0")
    assert result["ev"] == Decimal("0")
    assert result["cpi"] is None
    assert result["spi"] is None


def test_project_consolidates_activity_values():
    values = [
        {"bac": Decimal("1000"), "actual_cost": Decimal("300"), "pv": Decimal("600"), "ev": Decimal("500")},
        {"bac": Decimal("2000"), "actual_cost": Decimal("500"), "pv": Decimal("1000"), "ev": Decimal("1200")},
    ]
    result = calculate_project(values)

    assert result["pv"] == Decimal("1600.00")
    assert result["ev"] == Decimal("1700.00")
    assert result["cv"] == Decimal("900.00")
    assert result["sv"] == Decimal("100.00")
    assert result["cpi"] == Decimal("2.1250")
    assert result["spi"] == Decimal("1.0625")
