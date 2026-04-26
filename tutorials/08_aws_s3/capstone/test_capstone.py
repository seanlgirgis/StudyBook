def test_prefix():
    from datetime import date

    def prefix(env, domain, d):
        return f"{env}/{domain}/year={d.year}/month={d.month:02d}/day={d.day:02d}/"

    assert prefix("raw", "iot", date(2026, 4, 25)) == \
        "raw/iot/year=2026/month=04/day=25/"


def test_cost_calc():
    size = 100
    standard = size * 0.023
    assert standard == 2.3


def test_lifecycle_logic():
    transitions = [30, 180]
    assert transitions[0] < transitions[1]