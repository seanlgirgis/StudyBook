"""Stage 1, Tiny Block 8: Reject invalid requests early.

Mechanics:
    Handled by rag_foundation.

Functionality studied here:
    Request objects validate their data before anything is sent to the model.
"""

from rag_foundation import TextGenerationRequest


def main() -> None:
    try:
        request = TextGenerationRequest(
            prompt="Explain embeddings.",
            max_output_tokens=0,
        )

        print(request)

    except ValueError as error:
        print("REQUEST REJECTED")
        print("----------------")
        print(error)


if __name__ == "__main__":
    main()