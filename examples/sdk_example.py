"""Etsy scraper API: DataGuru Python SDK example.

Runs DataGuru's Etsy APIs and prints the JSON they return:
  - Etsy Product Details: $0.0032 per successful request ($3.20 per 1,000)
  - Etsy Product Search: $0.0032 per successful request ($3.20 per 1,000)

Setup:
    pip install -r requirements.txt
    export DATAGURU_API_KEY="your key"   # free credit at https://dashboard.dataguru.cc

Run:
    python examples/sdk_example.py            # every API below
    python examples/sdk_example.py etsy-product-details
"""
import json
import sys
from pathlib import Path

from dataguru import DataGuru, DataGuruError

def etsy_product_details(dg):
    """Etsy Product Details: Get listing details from an Etsy product URL, including price and discount, stock, variations, ratings and reviews, shipping, materials, images, description and shop information."""
    return dg.call(
        "etsy-product-details",
        product_url="https://www.etsy.com/listing/1301860928/personalized-leather-duffle-bag-handmade",
    )


def etsy_product_search(dg):
    """Etsy Product Search: Search Etsy by keyword and get matching listings with titles, prices and discounts, shop names and ratings, badges, free-shipping flags and images."""
    return dg.call(
        "etsy-product-search",
        query="leather duffle bag",
    )


EXAMPLES = {
    "etsy-product-details": etsy_product_details,
    "etsy-product-search": etsy_product_search,
}
DEFAULT = ['etsy-product-details', 'etsy-product-search']


def main(names):
    out = Path("output")
    out.mkdir(exist_ok=True)
    with DataGuru() as dg:  # reads DATAGURU_API_KEY
        for name in names:
            data = EXAMPLES[name](dg)
            (out / f"{name}.json").write_text(json.dumps(data, indent=2, ensure_ascii=False))
            print(f"{name}: saved output/{name}.json")
            print(json.dumps(data, indent=2, ensure_ascii=False)[:1500])


if __name__ == "__main__":
    names = sys.argv[1:] or DEFAULT
    unknown = [n for n in names if n not in EXAMPLES]
    if unknown:
        sys.exit(f"Unknown API {unknown}. Choose from: {', '.join(EXAMPLES)}")
    try:
        main(names)
    except DataGuruError as error:
        sys.exit(f"DataGuru error: {error}")
