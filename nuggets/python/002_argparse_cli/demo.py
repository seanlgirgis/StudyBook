from __future__ import annotations

import argparse


def build_messages(name: str = "nuggets", repeat: int = 1, uppercase: bool = False) -> list[str]:
    if repeat < 1:
        raise ValueError("repeat must be at least 1")

    message = f"Hello, {name}!"
    if uppercase:
        message = message.upper()

    return [message for _ in range(repeat)]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Tiny argparse demo for nuggets.")
    parser.add_argument("--name", default="nuggets", help="Name to greet.")
    parser.add_argument("--repeat", type=int, default=1, help="How many greetings to print.")
    parser.add_argument("--uppercase", action="store_true", help="Print greeting in uppercase.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> list[str]:
    args = parse_args(argv)
    messages = build_messages(name=args.name, repeat=args.repeat, uppercase=args.uppercase)

    for line in messages:
        print(line)

    return messages


if __name__ == "__main__":
    main()
