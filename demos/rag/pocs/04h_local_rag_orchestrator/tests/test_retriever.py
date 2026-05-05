from src.retriever import retrieve


def test_retriever_finds_plumbing_leak() -> None:
    records = [
        {
            "id": "kb_plumbing_leak_001",
            "title": "Plumbing leak repair",
            "service_type": "plumbing",
            "symptoms": ["leak", "pipe", "sink", "water under sink"],
            "text": "Repair leaks in pipes and sink lines.",
        },
        {
            "id": "kb_ac_repair_001",
            "title": "AC repair",
            "service_type": "AC",
            "symptoms": ["not cooling"],
            "text": "Cooling diagnostics.",
        },
    ]

    result = retrieve("There is water under my sink and pipe leak", records, top_k=2)
    assert result
    assert result[0]["id"] == "kb_plumbing_leak_001"


def test_retriever_finds_ac_repair() -> None:
    records = [
        {
            "id": "kb_ac_repair_001",
            "title": "AC repair service",
            "service_type": "AC",
            "symptoms": ["not cooling", "warm air"],
            "text": "Diagnose AC cooling faults.",
        },
        {
            "id": "kb_clogged_drain_001",
            "title": "Drain clearing",
            "service_type": "plumbing",
            "symptoms": ["slow drain"],
            "text": "Drain service only.",
        },
    ]

    result = retrieve("My system is not cooling", records, top_k=2)
    assert result
    assert result[0]["id"] == "kb_ac_repair_001"