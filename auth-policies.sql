-- Update Row Level Security policies to require authentication
-- Run this in your Supabase SQL editor to protect your data

-- Products table - require authentication
DROP POLICY IF EXISTS "Allow public read on products" ON products;
CREATE POLICY "Authenticated users can read products" ON products
    FOR SELECT TO authenticated
    USING (true);

-- Scrape log - require authentication
DROP POLICY IF EXISTS "Allow public read on scrape_log" ON scrape_log;
CREATE POLICY "Authenticated users can read scrape_log" ON scrape_log
    FOR SELECT TO authenticated
    USING (true);

-- Supplier config - require authentication
DROP POLICY IF EXISTS "Allow public read on supplier_config" ON supplier_config;
CREATE POLICY "Authenticated users can read supplier_config" ON supplier_config
    FOR SELECT TO authenticated
    USING (true);

-- Service role still has full access (no changes needed)
