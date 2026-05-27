import sys
from html.parser import HTMLParser
from urllib.request import urlopen
from html import unescape


class TableCellParser(HTMLParser):
    """
    Simple HTML parser that collects the text inside table cells.

    The published Google Doc stores the coordinate data in an HTML table.
    This parser extracts each <td> or <th> cell into a flat list.
    """

    def __init__(self):
        super().__init__()
        self.in_cell = False
        self.current = []
        self.cells = []

    def handle_starttag(self, tag, attrs):
        # Start collecting text when a table cell begins.
        if tag in ("td", "th"):
            self.in_cell = True
            self.current = []

    def handle_data(self, data):
        # Save text that appears inside the current table cell.
        if self.in_cell:
            self.current.append(data)

    def handle_endtag(self, tag):
        # When the cell ends, clean up the text and store it.
        if tag in ("td", "th") and self.in_cell:
            text = unescape("".join(self.current)).strip()
            self.cells.append(text)
            self.in_cell = False


def print_secret_message(url):
    """
    Download a published Google Doc, read its coordinate table,
    and print the hidden message as a character grid.
    """

    # Download the published Google Doc as HTML.
    html = urlopen(url).read().decode("utf-8")

    # Extract all table cells from the document.
    parser = TableCellParser()
    parser.feed(html)
    cells = parser.cells

    points = []

    # Parse every x, character, y triple from the table.
    # Header cells such as "x-coordinate" are skipped because they are not digits.
    for i in range(len(cells) - 2):
        x_text = cells[i].strip()
        char = cells[i + 1]
        y_text = cells[i + 2].strip()

        if x_text.isdigit() and y_text.isdigit():
            points.append((int(x_text), int(y_text), char))

    # If no coordinate rows were found, avoid crashing on max().
    if not points:
        print("No coordinate data found.")
        return

    # Find the grid size needed to hold all characters.
    max_x = max(x for x, y, char in points)
    max_y = max(y for x, y, char in points)

    # Build a blank grid filled with spaces.
    grid = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    # Place each character at its x/y coordinate.
    for x, y, char in points:
        grid[y][x] = char

    # Print from max_y down to 0 so the message is oriented correctly.
    for y in range(max_y, -1, -1):
        print("".join(grid[y]))


def main():
    # Test URLs used when the script is run without command-line arguments.
    test_urls = [
        "https://docs.google.com/document/d/e/"
        "2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_"
        "u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub",

        "https://docs.google.com/document/d/e/"
        "2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_"
        "gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub",
    ]

    # If a URL is provided on the command line, run only that URL.
    if len(sys.argv) > 1:
        print_secret_message(sys.argv[1])

    # Otherwise, run all built-in test URLs.
    else:
        for url in test_urls:
            print("=" * 60)
            print_secret_message(url)
            print()


if __name__ == "__main__":
    main()