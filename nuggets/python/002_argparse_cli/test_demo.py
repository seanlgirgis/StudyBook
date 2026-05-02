from demo import build_messages


def test_default_behavior() -> None:
    assert build_messages() == ["Hello, nuggets!"]


def test_repeated_output() -> None:
    assert build_messages(name="Sean", repeat=3) == [
        "Hello, Sean!",
        "Hello, Sean!",
        "Hello, Sean!",
    ]


def test_uppercase_behavior() -> None:
    assert build_messages(name="Sean", repeat=2, uppercase=True) == [
        "HELLO, SEAN!",
        "HELLO, SEAN!",
    ]
