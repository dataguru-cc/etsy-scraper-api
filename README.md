# Etsy Scraper API

Scrape Etsy with a JSON API. This repo has working Python examples for DataGuru's Etsy scraper APIs: Etsy Product Details and Etsy Product Search.

[DataGuru](https://dataguru.cc) runs the scraping, proxies, retries and parsing, and returns clean JSON. You pay only for successful requests, from $0.0032 per request, out of a prepaid balance: no subscription. New accounts get $1.00 of free credit.

## Etsy APIs

| API | What it returns | Price | Page |
| --- | --- | --- | --- |
| [Etsy Product Details](#etsy-product-details) | Get listing details from an Etsy product URL, including price and discount, stock, variations, ratings and reviews, shipping, materials, images, description and shop information. | $0.0032 | [https://dataguru.cc/apis/etsy-product-details/](https://dataguru.cc/apis/etsy-product-details/) |
| [Etsy Product Search](#etsy-product-search) | Search Etsy by keyword and get matching listings with titles, prices and discounts, shop names and ratings, badges, free-shipping flags and images. | $0.0032 | [https://dataguru.cc/apis/etsy-product-search/](https://dataguru.cc/apis/etsy-product-search/) |

## Quick start

1. Create a free account and an API key at [dashboard.dataguru.cc](https://dashboard.dataguru.cc).
2. Install and run:

```bash
git clone https://github.com/dataguru-cc/etsy-scraper-api.git
cd etsy-scraper-api
pip install -r requirements.txt
export DATAGURU_API_KEY="your key"
python examples/sdk_example.py etsy-product-details
```

## Examples

Every example covers all 2 Etsy APIs. Pass an API name to run just one; with no name each script runs them all, and each call is billed at the price above.

| File | Style | Run |
| --- | --- | --- |
| [`examples/sdk_example.py`](examples/sdk_example.py) | [DataGuru Python SDK](https://github.com/dataguru-cc/dataguru-python) (`pip install dataguru-sdk`), one function per API, saves JSON to `output/` | `python examples/sdk_example.py` |
| [`examples/requests_example.py`](examples/requests_example.py) | Plain `requests`, synchronous | `python examples/requests_example.py` |
| [`examples/async_example.py`](examples/async_example.py) | `asyncio` + `httpx`, concurrent with a limit | `python examples/async_example.py` |
| [`examples/scrapy_spider.py`](examples/scrapy_spider.py) | Scrapy spider, items to JSON/CSV | `scrapy runspider examples/scrapy_spider.py -O etsy.json` |

All requests use the header `Authorization: Api-Key YOUR_API_KEY`. Errors return `{"success": false, "error": {"code", "message", "request_id"}}`, with HTTP 402 when the balance runs out and 429 (with `Retry-After`) when rate limited. Failed requests are not charged.

## API reference

### Etsy Product Details

Get listing details from an Etsy product URL, including price and discount, stock, variations, ratings and reviews, shipping, materials, images, description and shop information.

- Endpoint: `POST https://api.dataguru.cc/api/v1/etsy/products/details`
- Price: $0.0032 per successful request ($3.20 per 1,000)
- Rate limit: 60 requests/minute
- Page and live playground: https://dataguru.cc/apis/etsy-product-details/
- Documentation: https://dataguru.cc/documentation/etsy-product-details/

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `location` | string | no | Two-letter country code (default US). Prices and shipping are shown for that country. |
| `product_url` | string | yes | Full Etsy listing URL (e.g. https://www.etsy.com/listing/1016735270/leather-duffel-weekender-bag-men). |

**Response fields:** `listing_id`, `title`, `url`, `location`, `description`, `price`, `availability`, `quantity_available`, `rating`, `review_count`, `category`, `breadcrumbs`, `materials`, `images`, `variations`, `shipping`, `shop`, `listed_on`, `reviews`, plus `_metadata`

```bash
curl -X POST "https://api.dataguru.cc/api/v1/etsy/products/details" \
  -H "Authorization: Api-Key $DATAGURU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_url": "https://www.etsy.com/listing/1301860928/personalized-leather-duffle-bag-handmade"}'
```

<details><summary>Response schema</summary>

Values are type placeholders from the API's published schema, not real data.

```json
{
  "listing_id": "1234567890",
  "title": "string",
  "url": "https://example.com/...",
  "location": "string",
  "description": "string",
  "price": {
    "current_price": 0.0,
    "min_price": 0.0,
    "max_price": 0.0,
    "original_price": 0.0,
    "discount_percent": 0,
    "currency": "USD"
  },
  "availability": "string",
  "quantity_available": 0.0,
  "rating": 0.0,
  "review_count": 0.0,
  "category": "string",
  "breadcrumbs": [
    "string"
  ],
  "materials": [
    "string"
  ],
  "images": [
    "string"
  ],
  "variations": [
    {
      "name": "string",
      "options": [
        {
          "value": "string",
          "sold_out": false
        }
      ]
    }
  ],
  "shipping": {
    "cost": 0.0,
    "currency": "USD",
    "ships_from": "string",
    "ships_to": "string",
    "handling_days_min": 0.0,
    "handling_days_max": 0.0,
    "transit_days_min": 0.0,
    "transit_days_max": 0.0
  },
  "shop": {
    "name": "string",
    "shop_id": "1234567890",
    "url": "https://example.com/...",
    "logo": "string",
    "rating": 0.0,
    "review_count": 0,
    "sales": 0,
    "star_seller": false
  },
  "listed_on": "string",
  "reviews": [
    {
      "rating": 0.0,
      "date": "2026-01-01T12:00:00Z",
      "author": "string",
      "text": "string"
    }
  ],
  "_metadata": {
    "request_id": "3f6c1a2e-8b4d-4c1e-9a7f-2d5e6b7c8d9e",
    "execution_time_ms": 842,
    "endpoint": "Etsy Product Details",
    "mode": "live",
    "format": "json",
    "timestamp": "2026-01-01T12:00:00+00:00"
  }
}
```

</details>

### Etsy Product Search

Search Etsy by keyword and get matching listings with titles, prices and discounts, shop names and ratings, badges, free-shipping flags and images.

- Endpoint: `POST https://api.dataguru.cc/api/v1/etsy/products/search`
- Price: $0.0032 per successful request ($3.20 per 1,000)
- Rate limit: 60 requests/minute
- Page and live playground: https://dataguru.cc/apis/etsy-product-search/
- Documentation: https://dataguru.cc/documentation/etsy-product-search/

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `limit` | integer | no | Maximum number of search results to return (up to 12, the first page of results). Default: `12`. |
| `location` | string | no | Two-letter country code (default US). Prices are shown in that country's currency. |
| `query` | string | yes | Search keywords, e.g. "leather duffle bag" |

**Response fields:** `query`, `location`, `returned_results`, `results`, plus `_metadata`

```bash
curl -X POST "https://api.dataguru.cc/api/v1/etsy/products/search" \
  -H "Authorization: Api-Key $DATAGURU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "leather duffle bag"}'
```

<details><summary>Response schema</summary>

Values are type placeholders from the API's published schema, not real data.

```json
{
  "query": "string",
  "location": "string",
  "returned_results": 0,
  "results": [
    {
      "listing_id": "1234567890",
      "title": "string",
      "url": "https://example.com/...",
      "price": {
        "current_price": 0.0,
        "original_price": 0.0,
        "discount_percent": 0,
        "currency": "USD",
        "currency_symbol": "string"
      },
      "shop_rating": 0.0,
      "shop_review_count": 0,
      "shop_name": "string",
      "shop_id": "1234567890",
      "image": "string",
      "badges": [
        "string"
      ],
      "free_shipping": false,
      "sponsored": false
    }
  ],
  "_metadata": {
    "request_id": "3f6c1a2e-8b4d-4c1e-9a7f-2d5e6b7c8d9e",
    "execution_time_ms": 842,
    "endpoint": "Etsy Product Search",
    "mode": "live",
    "format": "json",
    "timestamp": "2026-01-01T12:00:00+00:00"
  }
}
```

</details>

## More

- Python SDK and examples for all DataGuru APIs: [github.com/dataguru-cc/dataguru-python](https://github.com/dataguru-cc/dataguru-python) ([docs](https://dataguru-python.readthedocs.io/))
- Every API, with a live playground: [https://dataguru.cc/apis/](https://dataguru.cc/apis/)
- Use DataGuru from Claude, ChatGPT or Cursor through the MCP server: [https://dataguru.cc/mcp/](https://dataguru.cc/mcp/)
- Run thousands of inputs from a CSV at half price with batch jobs: [https://dataguru.cc/documentation/](https://dataguru.cc/documentation/)
- Other scraper APIs: [1688](https://github.com/dataguru-cc/1688-scraper-api), [Airbnb](https://github.com/dataguru-cc/airbnb-scraper-api), [Alibaba](https://github.com/dataguru-cc/alibaba-scraper-api), [AliExpress](https://github.com/dataguru-cc/aliexpress-scraper-api), [Amazon](https://github.com/dataguru-cc/amazon-scraper-api), [arXiv](https://github.com/dataguru-cc/arxiv-scraper-api), [ASOS](https://github.com/dataguru-cc/asos-scraper-api), [Best Buy](https://github.com/dataguru-cc/best-buy-scraper-api), [Booking.com](https://github.com/dataguru-cc/booking-scraper-api), [Brave Search](https://github.com/dataguru-cc/brave-search-scraper-api), [CA State Bar](https://github.com/dataguru-cc/california-state-bar-scraper-api), [Capterra](https://github.com/dataguru-cc/capterra-scraper-api), [CoinGecko](https://github.com/dataguru-cc/coingecko-scraper-api), [CoinMarketCap](https://github.com/dataguru-cc/coinmarketcap-scraper-api), [Companies House](https://github.com/dataguru-cc/companies-house-scraper-api), [Costco](https://github.com/dataguru-cc/costco-scraper-api), [CourtListener](https://github.com/dataguru-cc/courtlistener-scraper-api), [Crunchbase](https://github.com/dataguru-cc/crunchbase-scraper-api), [Discord](https://github.com/dataguru-cc/discord-scraper-api), [DoorDash](https://github.com/dataguru-cc/doordash-scraper-api), [eBay](https://github.com/dataguru-cc/ebay-scraper-api), [Expedia](https://github.com/dataguru-cc/expedia-scraper-api), [Fiverr](https://github.com/dataguru-cc/fiverr-scraper-api), [Flipkart](https://github.com/dataguru-cc/flipkart-scraper-api), [Glassdoor](https://github.com/dataguru-cc/glassdoor-scraper-api), [Google Flights](https://github.com/dataguru-cc/google-flights-scraper-api), [Google Patents](https://github.com/dataguru-cc/google-patents-scraper-api), [Google Scholar](https://github.com/dataguru-cc/google-scholar-scraper-api), [Google Search](https://github.com/dataguru-cc/google-search-scraper-api), [Grubhub](https://github.com/dataguru-cc/grubhub-scraper-api), [Home Depot](https://github.com/dataguru-cc/home-depot-scraper-api), [Instagram](https://github.com/dataguru-cc/instagram-scraper-api), [Investing.com](https://github.com/dataguru-cc/investing-com-scraper-api), [Justia](https://github.com/dataguru-cc/justia-scraper-api), [Kayak](https://github.com/dataguru-cc/kayak-scraper-api), [Kick](https://github.com/dataguru-cc/kick-scraper-api), [Lazada](https://github.com/dataguru-cc/lazada-scraper-api), [MarketWatch](https://github.com/dataguru-cc/marketwatch-scraper-api), [Mercado Libre](https://github.com/dataguru-cc/mercado-libre-scraper-api), [Monster](https://github.com/dataguru-cc/monster-scraper-api), [OpenCorporates](https://github.com/dataguru-cc/opencorporates-scraper-api), [OpenTable](https://github.com/dataguru-cc/opentable-scraper-api), [PACER](https://github.com/dataguru-cc/pacer-scraper-api), [PitchBook](https://github.com/dataguru-cc/pitchbook-scraper-api), [PubMed](https://github.com/dataguru-cc/pubmed-scraper-api), [Reddit](https://github.com/dataguru-cc/reddit-scraper-api), [Redfin](https://github.com/dataguru-cc/redfin-scraper-api), [Resy](https://github.com/dataguru-cc/resy-scraper-api), [Rightmove](https://github.com/dataguru-cc/rightmove-scraper-api), [SEC EDGAR](https://github.com/dataguru-cc/sec-edgar-scraper-api), [Seeking Alpha](https://github.com/dataguru-cc/seeking-alpha-scraper-api), [Shopee](https://github.com/dataguru-cc/shopee-scraper-api), [Skyscanner](https://github.com/dataguru-cc/skyscanner-scraper-api), [Target](https://github.com/dataguru-cc/target-scraper-api), [TikTok](https://github.com/dataguru-cc/tiktok-scraper-api), [TradingView](https://github.com/dataguru-cc/tradingview-scraper-api), [TripAdvisor](https://github.com/dataguru-cc/tripadvisor-scraper-api), [Trulia](https://github.com/dataguru-cc/trulia-scraper-api), [TrustRadius](https://github.com/dataguru-cc/trustradius-scraper-api), [Twitch](https://github.com/dataguru-cc/twitch-scraper-api), [Uber Eats](https://github.com/dataguru-cc/uber-eats-scraper-api), [Upwork](https://github.com/dataguru-cc/upwork-scraper-api), [Vrbo](https://github.com/dataguru-cc/vrbo-scraper-api), [Walmart](https://github.com/dataguru-cc/walmart-scraper-api), [Wayfair](https://github.com/dataguru-cc/wayfair-scraper-api), [X (Twitter)](https://github.com/dataguru-cc/twitter-scraper-api), [Yahoo Finance](https://github.com/dataguru-cc/yahoo-finance-scraper-api), [YouTube](https://github.com/dataguru-cc/youtube-scraper-api), [Zillow](https://github.com/dataguru-cc/zillow-scraper-api), [ZoomInfo](https://github.com/dataguru-cc/zoominfo-scraper-api), [Zoopla](https://github.com/dataguru-cc/zoopla-scraper-api)

## License

The example code is MIT licensed. Use of the DataGuru API is subject to the [terms of service](https://dataguru.cc/terms/).
