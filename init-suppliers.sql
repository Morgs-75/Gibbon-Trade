-- Initialize supplier_config table with default suppliers
-- Run this after creating the table structure

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
