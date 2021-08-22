"""CLI for requesting COVID-19 incidence number for given German ZIP code."""

import re

import requests
import typer
from bs4 import BeautifulSoup

PATTERN = r"pro 100.000 Einwohner in den letzten 7 Tagen</td>\n<td>([\d.]+)[\d,]*</td>"

app = typer.Typer(
    help="CLI for requesting COVID-19 incidence number for given German ZIP code."
)


@app.command()
def print_incidence(
    zip: str = typer.Argument(
        ...,
        help="5-digit German ZIP code.",
    )
):
    """Returns incidence number for German zip code."""
    incidence = _get_incidence(zip)
    print(incidence)


def _get_incidence(zip: str) -> int:
    """Query and parse incidence number for given ZIP code.

    Args:
        zip (str): ZIP code in German format (5 digits).

    Returns:
        int: Incidence number (rounded down).
    """
    assert len(zip) == 5, "PLZ is not of length 5!"

    res = requests.get(url=f"https://covid-plz-check.de/?query={zip}")
    html_raw = res.text
    soup = BeautifulSoup(html_raw, "html.parser")
    table = soup.find(class_="table")

    regex_matches = re.findall(PATTERN, str(table))
    incidence = int(regex_matches[0])
    return incidence


if __name__ == "__main__":
    app()
