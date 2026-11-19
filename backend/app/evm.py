from decimal import Decimal, ROUND_HALF_UP

ZERO = Decimal("0")
ONE = Decimal("1")
HUNDRED = Decimal("100")
MONEY_QUANTUM = Decimal("0.01")


def money(value: Decimal) -> Decimal:
    return value.quantize(MONEY_QUANTUM, rounding=ROUND_HALF_UP)


def ratio(numerator: Decimal, denominator: Decimal) -> Decimal | None:
    if denominator == ZERO:
        return None
    return (numerator / denominator).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)


def calculate_activity(bac: Decimal, planned_progress: Decimal, actual_progress: Decimal, actual_cost: Decimal) -> dict:
    pv = money(bac * planned_progress / HUNDRED)
    ev = money(bac * actual_progress / HUNDRED)
    cv = money(ev - actual_cost)
    sv = money(ev - pv)
    cpi = ratio(ev, actual_cost)
    spi = ratio(ev, pv)
    exact_cpi = ev / actual_cost if actual_cost != ZERO else None
    eac = money(bac / exact_cpi) if exact_cpi not in (None, ZERO) else None
    vac = money(bac - eac) if eac is not None else None

    cpi_status = "not_available" if cpi is None else "under_budget" if cpi > ONE else "over_budget" if cpi < ONE else "on_budget"
    spi_status = "not_available" if spi is None else "ahead" if spi > ONE else "behind" if spi < ONE else "on_schedule"

    return {
        "pv": pv,
        "ev": ev,
        "cv": cv,
        "sv": sv,
        "cpi": cpi,
        "spi": spi,
        "eac": eac,
        "vac": vac,
        "cpi_status": cpi_status,
        "spi_status": spi_status,
    }


def calculate_project(activity_values: list[dict]) -> dict:
    if not activity_values:
        return {
            "pv": ZERO,
            "ev": ZERO,
            "cv": ZERO,
            "sv": ZERO,
            "cpi": None,
            "spi": None,
            "eac": None,
            "vac": None,
            "cpi_status": "not_available",
            "spi_status": "not_available",
        }

    bac = sum((Decimal(str(value["bac"])) for value in activity_values), ZERO)
    pv = sum((Decimal(str(value["pv"])) for value in activity_values), ZERO)
    ev = sum((Decimal(str(value["ev"])) for value in activity_values), ZERO)
    ac = sum((Decimal(str(value["actual_cost"])) for value in activity_values), ZERO)

    cv = money(ev - ac)
    sv = money(ev - pv)
    cpi = ratio(ev, ac)
    spi = ratio(ev, pv)
    exact_cpi = ev / ac if ac != ZERO else None
    eac = money(bac / exact_cpi) if exact_cpi not in (None, ZERO) else None
    vac = money(bac - eac) if eac is not None else None

    cpi_status = "not_available" if cpi is None else "under_budget" if cpi > ONE else "over_budget" if cpi < ONE else "on_budget"
    spi_status = "not_available" if spi is None else "ahead" if spi > ONE else "behind" if spi < ONE else "on_schedule"

    return {
        "pv": money(pv),
        "ev": money(ev),
        "cv": cv,
        "sv": sv,
        "cpi": cpi,
        "spi": spi,
        "eac": eac,
        "vac": vac,
        "cpi_status": cpi_status,
        "spi_status": spi_status,
    }
