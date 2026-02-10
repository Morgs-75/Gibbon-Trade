-- Products table
CREATE TABLE IF NOT EXISTS products (
    id BIGSERIAL PRIMARY KEY,
    source TEXT NOT NULL,           -- 'kevmor', 'intafloors', 'gibbon'
    name TEXT NOT NULL,
    price NUMERIC(10,2),            -- NULL if no price available
    price_display TEXT,             -- Human-readable price string
    url TEXT,
    image TEXT,
    category TEXT,
    sku TEXT,
    description TEXT,
    scraped_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index for fast queries
CREATE INDEX idx_products_source ON products(source);
CREATE INDEX idx_products_name ON products(name);
CREATE INDEX idx_products_scraped_at ON products(scraped_at);

-- Scrape log table
CREATE TABLE IF NOT EXISTS scrape_log (
    id BIGSERIAL PRIMARY KEY,
    source TEXT NOT NULL,
    product_count INTEGER NOT NULL,
    products_with_price INTEGER NOT NULL DEFAULT 0,
    started_at TIMESTAMPTZ NOT NULL,
    completed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status TEXT NOT NULL DEFAULT 'success'
);

-- Enable Row Level Security
ALTER TABLE products ENABLE ROW LEVEL SECURITY;
ALTER TABLE scrape_log ENABLE ROW LEVEL SECURITY;

-- Allow public read access (anon key)
CREATE POLICY "Allow public read on products" ON products
    FOR SELECT USING (true);

CREATE POLICY "Allow public read on scrape_log" ON scrape_log
    FOR SELECT USING (true);

-- Allow service_role full access (for scraper)
CREATE POLICY "Allow service write on products" ON products
    FOR ALL USING (true) WITH CHECK (true);

CREATE POLICY "Allow service write on scrape_log" ON scrape_log
    FOR ALL USING (true) WITH CHECK (true);
