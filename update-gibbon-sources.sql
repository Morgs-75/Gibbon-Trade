-- Update supplier_config to split gibbon into gibbon_csv and gibbon_web
-- Run this in your Supabase SQL editor

-- First, add gibbon_csv entry if it doesn't exist
INSERT INTO supplier_config (key, name, url, type, color, protected, enabled)
VALUES ('gibbon_csv', 'Gibbon CSV', 'https://gibbontrade.com.au', 'custom', '#16a34a', false, true)
ON CONFLICT (key) DO UPDATE SET
    name = EXCLUDED.name,
    color = EXCLUDED.color,
    enabled = EXCLUDED.enabled;

-- Then, add gibbon_web entry if it doesn't exist
INSERT INTO supplier_config (key, name, url, type, color, protected, enabled)
VALUES ('gibbon_web', 'Gibbon Web', 'https://gibbontrade.com.au', 'woocommerce', '#22c55e', false, true)
ON CONFLICT (key) DO UPDATE SET
    name = EXCLUDED.name,
    color = EXCLUDED.color,
    enabled = EXCLUDED.enabled;

-- Update existing 'gibbon' entry to be legacy/disabled (optional - comment out if you want to keep it active)
UPDATE supplier_config
SET enabled = true, name = 'Gibbon Trade (Legacy)'
WHERE key = 'gibbon';

-- Check the results
SELECT key, name, enabled, color FROM supplier_config ORDER BY key;
