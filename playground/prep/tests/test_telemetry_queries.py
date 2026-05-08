from src import telemetry_queries as tq


def _assert_select_only(sql: str):
    s = sql.strip().lower()
    assert s.startswith("select") or s.startswith("with")
    banned = ["drop", "delete", "update", "insert", "alter", "truncate"]
    for token in banned:
        assert token not in s


def test_query_builders_return_select_only_sql():
    queries = [
        tq.sql_list_public_tables(),
        tq.sql_preview_telemetry(10),
        tq.sql_service_average_cpu_memory(),
        tq.sql_threshold_risk_samples(10),
        tq.sql_hourly_service_rollup(),
        tq.sql_jsonb_tag_preview(10),
    ]
    for q in queries:
        _assert_select_only(q)
