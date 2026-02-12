-- Add supplier_config table (run this if you get errors with schema.sql)
-- This file only adds the new table and policies

-- Create supplier configuration table
CREATE TABLE IF NOT EXISTS supplier_config (
    id BIGSERIAL PRIMARY KEY,
    key TEXT NOT NULL UNIQUE,       -- 'kevmor', 'intafloors', etc.
    name TEXT NOT NULL,              -- Display name
    url TEXT NOT NULL,               -- Base URL
    type TEXT NOT NULL,              -- 'woocommerce', 'shopify', 'custom'
    color TEXT DEFAULT '#3b82f6',   -- Hex color for UI
    protected BOOLEAN DEFAULT false, -- Cannot be deleted if true
    enabled BOOLEAN DEFAULT true,    -- Whether to scrape this supplier
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE supplier_config ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist
DROP POLICY IF EXISTS "Allow public read on supplier_config" ON supplier_config;
DROP POLICY IF EXISTS "Allow service write on supplier_config" ON supplier_config;

-- Allow public read access (anon key)
CREATE POLICY "Allow public read on supplier_config" ON supplier_config
    FOR SELECT USING (true);

-- Allow service_role full access (for API)
CREATE POLICY "Allow service write on supplier_config" ON supplier_config
    FOR ALL USING (true) WITH CHECK (true);

-- Insert default suppliers (safe to run multiple times)
INSERT INTO supplier_config (key, name, url, type, color, protected, enabled)
VALUES
    ('kevmor', 'Kevmor', 'https://kevmor.com.au', 'custom', '#f97316', false, true),
    ('intafloors', 'Intafloors', 'https://intafloors.com.au', 'woocommerce', '#06b6d4', false, true),
    ('gibbon', 'Gibbon Trade', 'https://gibbontrade.com.au', 'woocommerce', '#22c55e', true, true),
    ('marques', 'Marques', 'https://marquesflooring.com.au', 'woocommerce', '#a855f7', false, true),
    ('floortrade', 'Floor Trade', 'https://www.floortrade.au', 'woocommerce', '#ec4899', false, true),
    ('gluesntools', 'Glues N Tools', 'https://gluesntools.com.au', 'shopify', '#eab308', false, true),
    ('homely', 'Homely', 'https://www.homelyflooring.com.au', 'woocommerce', '#14b8a6', false, true)
ON CONFLICT (key) DO NOTHING;
