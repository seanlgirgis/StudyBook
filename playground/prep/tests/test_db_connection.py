from src.db import smoke_test


def test_smoke_test_returns_data():
    df = smoke_test()
    assert not df.empty
    assert len(df) >= 1


def test_smoke_test_has_expected_shape_or_columns():
    df = smoke_test()
    cols = {str(c).lower() for c in df.columns}
    assert "current_database" in cols or len(df) >= 1
