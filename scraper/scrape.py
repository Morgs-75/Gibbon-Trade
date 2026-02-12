"""
Scheduled scraper for flooring supplier price comparison.
Reads supplier configuration from Supabase supplier_config table.
Supports WooCommerce, Shopify, and custom scrapers.
Writes product data to Supabase PostgreSQL.

Usage:
    python scrape.py                  # scrape all enabled suppliers from database
    python scrape.py kevmor           # scrape one specific supplier
    python scrape.py intafloors gibbon  # scrape specific suppliers

Environment variables:
    SUPABASE_URL        - e.g. https://xxx.supabase.co
    SUPABASE_SERVICE_KEY - service_role JWT
"""

import os
import re
import sys
import time
import logging
from datetime import datetime, timezone

import cloudscraper
import requests
from bs4 import BeautifulSoup
from supabase import create_client

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------------------------------------------------------------------------
# Kevmor
# ---------------------------------------------------------------------------

KEVMOR_CATEGORIES = [
    ("https://kevmor.com.au/308-carpet-adhesive", "Carpet Adhesive"),
    ("https://kevmor.com.au/358-contact-adhesive", "Contact Adhesive"),
    ("https://kevmor.com.au/334-resilient-vinyl-adhesive", "Vinyl Adhesive"),
    ("https://kevmor.com.au/387-psa-carpet-vinyl-tile", "PSA Adhesive"),
    ("https://kevmor.com.au/315-silicones", "Silicones"),
    ("https://kevmor.com.au/389-carpet-seam-sealer", "Carpet Seam Sealer"),
    ("https://kevmor.com.au/509-bulk-fill-levelling-compounds", "Levelling Compounds"),
    ("https://kevmor.com.au/510-patching-feather-finish", "Patching Compounds"),
    ("https://kevmor.com.au/512-cement-screeds", "Cement Screeds"),
    ("https://kevmor.com.au/513-self-levelling-compounds", "Self Levelling Compounds"),
    ("https://kevmor.com.au/511-rapid-setting-ramping-compounds", "Rapid Set Compounds"),
    ("https://kevmor.com.au/15-blades", "Blades"),
    ("https://kevmor.com.au/92-concave-blades", "Concave Blades"),
    ("https://kevmor.com.au/83-hook-blades", "Hook Blades"),
    ("https://kevmor.com.au/25-knives", "Knives"),
    ("https://kevmor.com.au/64-linoleumvinyl-knives", "Vinyl Knives"),
    ("https://kevmor.com.au/87-utility-knives", "Utility Knives"),
    ("https://kevmor.com.au/168-rotary-knives", "Rotary Knives"),
    ("https://kevmor.com.au/169-safety-knives", "Safety Knives"),
    ("https://kevmor.com.au/215-scraper-blades", "Scraper Blades"),
    ("https://kevmor.com.au/52-spreaders-trowels", "Trowels & Spreaders"),
    ("https://kevmor.com.au/31-rollers", "Rollers"),
    ("https://kevmor.com.au/75-stand-up-rollers", "Stand Up Rollers"),
    ("https://kevmor.com.au/76-wall-rollers", "Wall Rollers"),
    ("https://kevmor.com.au/77-levelling-installation-rollers", "Levelling Rollers"),
    ("https://kevmor.com.au/352-coating-and-paint-applicators-rollers", "Coating Applicators"),
    ("https://kevmor.com.au/16-carpet-laying-tools", "Carpet Laying Tools"),
    ("https://kevmor.com.au/541-carpet-installation-tool-kits", "Carpet Tool Kits"),
    ("https://kevmor.com.au/368-knee-kickers", "Knee Kickers"),
    ("https://kevmor.com.au/372-carpet-stretchers", "Power Stretchers"),
    ("https://kevmor.com.au/496-cutters-shears-trimmers", "Cutters & Shears"),
    ("https://kevmor.com.au/429-floor-grinders", "Floor Grinders"),
    ("https://kevmor.com.au/438-floor-removal-machines", "Floor Removal Machines"),
    ("https://kevmor.com.au/485-floor-scrapers", "Floor Scrapers"),
    ("https://kevmor.com.au/499-floor-scraper-blades-accessories", "Floor Scraper Blades"),
    ("https://kevmor.com.au/483-dust-collectors", "Dust Collectors"),
    ("https://kevmor.com.au/454-columbus-sander-grinder", "Columbus Grinder"),
    ("https://kevmor.com.au/349-polivac-machines-spare-parts", "Polivac Machines"),
    ("https://kevmor.com.au/354-floating-laminate-floor-tools", "Floating Floor Tools"),
    ("https://kevmor.com.au/491-laminate-wood-cutters", "Laminate Cutters"),
    ("https://kevmor.com.au/493-laminate-rollers", "Laminate Rollers"),
    ("https://kevmor.com.au/497-laminate-kits-misc", "Laminate Kits"),
    ("https://kevmor.com.au/18-ceramic", "Ceramic / Tiling"),
    ("https://kevmor.com.au/228-tiling-tools", "Tiling Tools"),
    ("https://kevmor.com.au/102-tile-cutter", "Tile Cutters"),
    ("https://kevmor.com.au/222-grout-applicators-floats-sponges", "Grout Tools"),
    ("https://kevmor.com.au/226-spacers-and-wedges", "Spacers & Wedges"),
    ("https://kevmor.com.au/350-leister", "Leister Welding Tools"),
    ("https://kevmor.com.au/82-welding-guns-parts", "Welding Guns"),
    ("https://kevmor.com.au/548-welding-tools", "Welding Tools"),
    ("https://kevmor.com.au/526-hot-weld-weld-rod", "Weld Rod"),
    ("https://kevmor.com.au/535-concrete-moisture-meters", "Concrete Moisture Meters"),
    ("https://kevmor.com.au/536-timber-moisture-meters", "Timber Moisture Meters"),
    ("https://kevmor.com.au/537-concrete-ph-test-kits", "pH Meters"),
    ("https://kevmor.com.au/106-knee-pads", "Knee Pads"),
    ("https://kevmor.com.au/347-back-support", "Back Support"),
    ("https://kevmor.com.au/336-safety-equipment-supplies", "Safety Equipment"),
    ("https://kevmor.com.au/273-brooms", "Brooms & Brushes"),
    ("https://kevmor.com.au/277-floor-mops", "Floor Mops"),
    ("https://kevmor.com.au/274-carpet-cleaner", "Carpet Cleaner"),
    ("https://kevmor.com.au/279-cleaning-cloths-wipes", "Cleaning Cloths"),
    ("https://kevmor.com.au/275-disinfectants", "Disinfectants"),
    ("https://kevmor.com.au/276-hard-floors", "Hard Floor Cleaner"),
    ("https://kevmor.com.au/45-tape", "Tape"),
    ("https://kevmor.com.au/81-sanding-discsbricksstones", "Sanding Supplies"),
    ("https://kevmor.com.au/138-cove-fillet", "Cove Fillet"),
    ("https://kevmor.com.au/137-edge-capping", "Edge Capping"),
    ("https://kevmor.com.au/412-wall-cove-trims", "Wall Cove Trims"),
    ("https://kevmor.com.au/423-cover-strips", "Cover Strips"),
    ("https://kevmor.com.au/424-premium-cover-strips", "Premium Cover Strips"),
    ("https://kevmor.com.au/425-standard-cover-strips", "Standard Cover Strips"),
    ("https://kevmor.com.au/365-diminishingreducer", "Diminishing/Reducer"),
    ("https://kevmor.com.au/378-expansion-jointcover", "Expansion Joint"),
    ("https://kevmor.com.au/139-skirting", "Skirting"),
    ("https://kevmor.com.au/407-brass-stair-nosing", "Brass Stair Nosing"),
    ("https://kevmor.com.au/406-carpet-stair-nosing", "Carpet Stair Nosing"),
    ("https://kevmor.com.au/379-pvc-stair-nosing", "PVC Stair Nosing"),
    ("https://kevmor.com.au/405-vinyl-stair-nosing", "Vinyl Stair Nosing"),
    ("https://kevmor.com.au/529-lvt-stair-nosing", "LVT Stair Nosing"),
    ("https://kevmor.com.au/530-commercial-stair-nosing", "Commercial Stair Nosing"),
    ("https://kevmor.com.au/449-specials", "Specials"),
    ("https://kevmor.com.au/450-clearance", "Clearance"),
    ("https://kevmor.com.au/448-new-products", "New Products"),
]


def _parse_kevmor_price(text: str):
    text = text.strip()
    if "Instore" in text or "Phone" in text:
        return None, "Instore/Phone Only"
    amounts = re.findall(r"\$[\d,]+\.?\d*", text)
    if not amounts:
        return None, text or "N/A"
    last = amounts[-1].replace("$", "").replace(",", "")
    try:
        return float(last), text
    except ValueError:
        return None, text


def scrape_kevmor():
    logger.info("Starting Kevmor scrape...")
    scraper = cloudscraper.create_scraper()
    products = []
    seen_urls = set()

    for idx, (url, category) in enumerate(KEVMOR_CATEGORIES):
        logger.info(f"  Kevmor: {category} ({idx+1}/{len(KEVMOR_CATEGORIES)})")
        try:
            page = 1
            while True:
                page_url = f"{url}?page={page}" if page > 1 else url
                r = scraper.get(page_url, timeout=20)
                if r.status_code != 200:
                    break
                soup = BeautifulSoup(r.text, "html.parser")
                items = soup.select("article.product-miniature")
                if not items:
                    break
                for item in items:
                    name_el = item.select_one(".product-title a, h3 a, h2 a")
                    price_el = item.select_one(".price, [class*=price]")
                    img_el = item.select_one("img")
                    link_el = item.select_one("a[href]")
                    name = name_el.get_text(strip=True) if name_el else None
                    href = (name_el or link_el or {}).get("href", "")
                    if not name or href in seen_urls:
                        continue
                    seen_urls.add(href)
                    price_text = price_el.get_text(strip=True) if price_el else ""
                    price_val, price_display = _parse_kevmor_price(price_text)
                    img_src = img_el.get("src", "") if img_el else ""
                    products.append({
                        "source": "kevmor",
                        "name": name,
                        "price": price_val,
                        "price_display": price_display,
                        "url": href,
                        "image": img_src,
                        "category": category,
                    })
                next_link = soup.select_one("a.next, [rel=next]")
                if next_link and page < 20:
                    page += 1
                    time.sleep(0.3)
                else:
                    break
            time.sleep(0.5)
        except Exception as e:
            logger.warning(f"Kevmor error on {category}: {e}")

    logger.info(f"Kevmor done: {len(products)} products")
    return products


# ---------------------------------------------------------------------------
# Intafloors (WooCommerce Store API)
# ---------------------------------------------------------------------------

def _scrape_woocommerce(base_url, source_name):
    """Generic WooCommerce Store API scraper."""
    logger.info(f"Starting {source_name} scrape...")
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-AU,en;q=0.9",
    })

    # Visit shop to establish session
    session.get(f"{base_url}/shop/", timeout=20)
    session.headers["Accept"] = "application/json"

    api = f"{base_url}/wp-json/wc/store/v1"

    # Get categories
    cat_map = {}
    try:
        r = session.get(f"{api}/products/categories?per_page=100", timeout=20)
        if r.status_code == 200:
            for cat in r.json():
                cat_map[cat["id"]] = cat["name"]
    except Exception as e:
        logger.warning(f"{source_name} categories error: {e}")

    products = []
    page = 1
    while True:
        logger.info(f"  {source_name}: page {page} ({len(products)} so far)")
        try:
            r = session.get(f"{api}/products?per_page=100&page={page}", timeout=30)
            if r.status_code != 200:
                # Re-establish session
                session.headers["Accept"] = "text/html"
                session.get(f"{base_url}/shop/", timeout=20)
                session.headers["Accept"] = "application/json"
                r = session.get(f"{api}/products?per_page=100&page={page}", timeout=30)
                if r.status_code != 200:
                    break

            data = r.json()
            if not data:
                break

            for p in data:
                prices = p.get("prices", {})
                price_raw = prices.get("price", "0")
                regular_raw = prices.get("regular_price", "0")
                minor_unit = prices.get("currency_minor_unit", 2)
                try:
                    price_val = int(price_raw) / (10 ** minor_unit) if price_raw else 0
                    regular_val = int(regular_raw) / (10 ** minor_unit) if regular_raw else 0
                except (ValueError, TypeError):
                    price_val, regular_val = 0, 0

                if price_val == 0:
                    price_display = "Contact for Price"
                elif price_val < regular_val:
                    price_display = f"${price_val:,.2f} (was ${regular_val:,.2f}) GST excl."
                else:
                    price_display = f"${price_val:,.2f} GST excl."

                cat_ids = [c["id"] for c in p.get("categories", [])]
                cat_names = [cat_map.get(cid, f"cat-{cid}") for cid in cat_ids]
                imgs = p.get("images", [])
                img_src = imgs[0].get("thumbnail", "") if imgs else ""

                products.append({
                    "source": source_name.lower().replace(" ", "_"),
                    "name": p.get("name", "Unknown"),
                    "price": price_val if price_val > 0 else None,
                    "price_display": price_display,
                    "url": p.get("permalink", ""),
                    "image": img_src,
                    "category": ", ".join(cat_names[:2]) if cat_names else "Uncategorized",
                    "sku": p.get("sku", ""),
                    "description": BeautifulSoup(
                        p.get("short_description", ""), "html.parser"
                    ).get_text(strip=True)[:200],
                })

            total_pages = int(r.headers.get("X-WP-TotalPages", 999))
            if page >= total_pages:
                break
            page += 1
            time.sleep(0.3)
        except Exception as e:
            logger.warning(f"{source_name} error on page {page}: {e}")
            break

    logger.info(f"{source_name} done: {len(products)} products")
    return products


def scrape_intafloors():
    return _scrape_woocommerce("https://intafloors.com.au", "intafloors")


def scrape_gibbon():
    return _scrape_woocommerce("https://gibbontrade.com.au", "gibbon")


def scrape_marques():
    return _scrape_woocommerce("https://marquesflooring.com.au", "marques")


def scrape_floortrade():
    return _scrape_woocommerce("https://www.floortrade.au", "floortrade")


def scrape_homely():
    return _scrape_woocommerce("https://www.homelyflooring.com.au", "homely")


# ---------------------------------------------------------------------------
# Shopify Store API
# ---------------------------------------------------------------------------

def _scrape_shopify(base_url, source_name):
    """Generic Shopify /products.json scraper."""
    logger.info(f"Starting {source_name} scrape...")
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json",
    })

    products = []
    page = 1
    while True:
        logger.info(f"  {source_name}: page {page} ({len(products)} so far)")
        try:
            r = session.get(
                f"{base_url}/products.json?limit=250&page={page}", timeout=30
            )
            if r.status_code != 200:
                logger.warning(f"{source_name} HTTP {r.status_code} on page {page}")
                break

            data = r.json().get("products", [])
            if not data:
                break

            for p in data:
                variant = p.get("variants", [{}])[0]
                try:
                    price_val = float(variant.get("price", "0") or "0")
                except (ValueError, TypeError):
                    price_val = 0

                compare_at = None
                try:
                    raw = variant.get("compare_at_price")
                    if raw:
                        compare_at = float(raw)
                except (ValueError, TypeError):
                    pass

                if price_val == 0:
                    price_display = "Contact for Price"
                elif compare_at and compare_at > price_val:
                    price_display = f"${price_val:,.2f} (was ${compare_at:,.2f})"
                else:
                    price_display = f"${price_val:,.2f}"

                # Strip HTML from body_html for description
                body = p.get("body_html") or ""
                description = BeautifulSoup(body, "html.parser").get_text(strip=True)[:200]

                imgs = p.get("images", [])
                img_src = imgs[0].get("src", "") if imgs else ""

                products.append({
                    "source": source_name,
                    "name": p.get("title", "Unknown"),
                    "price": price_val if price_val > 0 else None,
                    "price_display": price_display,
                    "url": f"{base_url}/products/{p.get('handle', '')}",
                    "image": img_src,
                    "category": p.get("product_type", "") or "Uncategorized",
                    "sku": variant.get("sku", ""),
                    "description": description,
                })

            page += 1
            time.sleep(0.5)
        except Exception as e:
            logger.warning(f"{source_name} error on page {page}: {e}")
            break

    logger.info(f"{source_name} done: {len(products)} products")
    return products


def scrape_gluesntools():
    return _scrape_shopify("https://gluesntools.com.au", "gluesntools")


# ---------------------------------------------------------------------------
# Database operations
# ---------------------------------------------------------------------------

def upsert_products(source: str, products: list, started_at: datetime):
    """Delete old products for source and insert new ones."""
    logger.info(f"Writing {len(products)} {source} products to Supabase...")

    # Delete existing products for this source
    supabase.table("products").delete().eq("source", source).execute()

    # Insert in batches of 500
    batch_size = 500
    for i in range(0, len(products), batch_size):
        batch = products[i:i + batch_size]
        rows = []
        for p in batch:
            rows.append({
                "source": source,
                "name": p["name"],
                "price": p.get("price"),
                "price_display": p.get("price_display", ""),
                "url": p.get("url", ""),
                "image": p.get("image", ""),
                "category": p.get("category", ""),
                "sku": p.get("sku", ""),
                "description": p.get("description", ""),
            })
        supabase.table("products").insert(rows).execute()
        logger.info(f"  Inserted batch {i//batch_size + 1} ({len(rows)} rows)")

    # Log the scrape
    with_price = sum(1 for p in products if p.get("price"))
    supabase.table("scrape_log").insert({
        "source": source,
        "product_count": len(products),
        "products_with_price": with_price,
        "started_at": started_at.isoformat(),
        "status": "success",
    }).execute()

    logger.info(f"Done: {source} - {len(products)} products ({with_price} with price)")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

SCRAPERS = {
    "kevmor": scrape_kevmor,
    "intafloors": scrape_intafloors,
    "gibbon": scrape_gibbon,
    "marques": scrape_marques,
    "floortrade": scrape_floortrade,
    "gluesntools": scrape_gluesntools,
    "homely": scrape_homely,
}


def main():
    # Load supplier configuration from database
    logger.info("Loading supplier configuration from database...")
    try:
        response = supabase.table("supplier_config").select("*").eq("enabled", True).execute()
        db_suppliers = {s["key"]: s for s in response.data}
        logger.info(f"Loaded {len(db_suppliers)} enabled suppliers from database")
    except Exception as e:
        logger.error(f"Failed to load supplier config from database: {e}")
        logger.info("Falling back to hardcoded SCRAPERS")
        db_suppliers = {}

    # Allow command-line override for specific suppliers
    if len(sys.argv) > 1:
        targets = sys.argv[1:]
    else:
        # Use database suppliers if available, otherwise fall back to hardcoded list
        targets = list(db_suppliers.keys()) if db_suppliers else list(SCRAPERS.keys())

    for source in targets:
        # Get supplier config from database or fallback to hardcoded
        if source in db_suppliers:
            config = db_suppliers[source]
            supplier_type = config["type"]
            supplier_url = config["url"]
            supplier_name = config["name"]

            logger.info(f"Scraping {supplier_name} ({source}) - type: {supplier_type}")

            # Determine which scraper function to use based on type
            if supplier_type == "custom" and source in SCRAPERS:
                # Use custom scraper function
                scraper_func = SCRAPERS[source]
            elif supplier_type == "woocommerce":
                # Use generic WooCommerce scraper
                scraper_func = lambda: _scrape_woocommerce(supplier_url, source)
            elif supplier_type == "shopify":
                # Use generic Shopify scraper
                scraper_func = lambda: _scrape_shopify(supplier_url, source)
            else:
                logger.error(f"Unknown scraper type '{supplier_type}' for {source}")
                continue
        elif source in SCRAPERS:
            # Fallback to hardcoded scraper
            logger.info(f"Using hardcoded scraper for {source}")
            scraper_func = SCRAPERS[source]
        else:
            logger.error(f"Unknown source: {source}")
            continue

        # Execute scrape
        started = datetime.now(timezone.utc)
        try:
            products = scraper_func()
            upsert_products(source, products, started)
        except Exception as e:
            logger.exception(f"Failed to scrape {source}: {e}")
            supabase.table("scrape_log").insert({
                "source": source,
                "product_count": 0,
                "products_with_price": 0,
                "started_at": started.isoformat(),
                "status": f"error: {e}",
            }).execute()


if __name__ == "__main__":
    main()
