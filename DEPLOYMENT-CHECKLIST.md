# Deployment Checklist - Fix Integration Issues

## Critical Issues Found

The application is broken due to **incomplete migration** from single "gibbon" source to split "gibbon_csv" + "gibbon_web" sources.

## Required Fixes (Do these in order)

### 1. Update Supabase supplier_config Table

**Run this SQL in Supabase SQL Editor:**

```sql
-- Add the new split sources
INSERT INTO supplier_config (key, name, url, type, color, protected, enabled)
VALUES
    ('gibbon_csv', 'Gibbon CSV', 'https://gibbontrade.com.au', 'custom', '#16a34a', false, true),
    ('gibbon_web', 'Gibbon Web', 'https://gibbontrade.com.au', 'woocommerce', '#22c55e', false, true)
ON CONFLICT (key) DO UPDATE SET
    name = EXCLUDED.name,
    color = EXCLUDED.color,
    enabled = EXCLUDED.enabled;
```

The file `update-gibbon-sources.sql` has been created with this SQL.

### 2. Migrate Existing Data in Products Table

**Option A: If you have OLD products with source='gibbon' that came from web scraping**

```sql
-- Update old 'gibbon' products to 'gibbon_web'
UPDATE products
SET source = 'gibbon_web'
WHERE source = 'gibbon';
```

**Option B: If those are actually CSV imports, keep them and just re-scrape**

Just run the scrapers again (step 3) to populate gibbon_web with fresh data.

### 3. Run the Scrapers to Populate Data

The scrapers have already been updated correctly:
- `scrape.py` line 302: `scrape_gibbon()` writes to source `gibbon_web` ✓
- `import_gibbon_csv.py` line 117: writes to source `gibbon_csv` ✓

**Run these commands:**

```bash
# Set your environment variables
export SUPABASE_URL="https://ualogaryduudrnozmoyx.supabase.co"
export SUPABASE_SERVICE_KEY="your_service_role_key_here"

# Scrape gibbon web products
cd scraper
python scrape.py gibbon_web

# Import gibbon CSV (if you have a CSV file)
python import_gibbon_csv.py "../GIbbon Trade List Sales Price 17.02.2026.csv"
```

### 4. Deploy Updated Frontend to Netlify

The `index.html` file has been updated with these fixes:
- ✓ Added backwards compatibility for legacy 'gibbon' source
- ✓ Added gibbon_csv and gibbon_web to default supplier list
- ✓ Added fallback mapping for old data.json
- ✓ Improved error messages with details
- ✓ Added console logging for debugging

**Deploy commands:**

```bash
cd "/c/Users/Troy Morgan/OneDrive/Gibbon Trade"
git add index.html update-gibbon-sources.sql DEPLOYMENT-CHECKLIST.md
git commit -m "Fix supplier source name mismatch - add gibbon_csv and gibbon_web support

- Add backwards compatibility for legacy 'gibbon' source
- Update default suppliers to include gibbon_csv, gibbon_web, and gibbon
- Add fallback mapping for old data.json format
- Improve error messages to show both Supabase and fallback errors
- Add console logging to debug which suppliers are loaded
"
git push origin master
```

Netlify will auto-deploy from the git push.

### 5. Verify the Fix

**Open browser console on https://prices.gibbontrade.com.au/**

You should see:
```
Loaded suppliers from database: kevmor (XXX products), intafloors (XXX products), gibbon_csv (XXX products), gibbon_web (XXX products)
Active suppliers: gibbon_csv, gibbon_web, gibbon, kevmor, intafloors
```

**Check for these specific issues:**
- ✗ "DATA is not defined" error → Should be gone
- ✗ Zero matches when searching → Should now show matches
- ✓ Products load and display → Should work
- ✓ Matching algorithm runs → Should show matches in "Price Comparison" tab

## What Was Wrong

### Root Cause
The code was split to have two gibbon sources (gibbon_csv for imported CSV data, gibbon_web for scraped web data), but:
1. Database `supplier_config` table only had `gibbon` entry, not `gibbon_csv` or `gibbon_web`
2. Existing products in database had source `gibbon`, not the new split names
3. Frontend expected `gibbon_csv` and `gibbon_web` by default but they didn't exist
4. Result: Zero products matched because supplier keys didn't align with product source values

### The Fix
- Updated frontend to accept legacy `gibbon` as well as new split sources
- Added SQL to insert gibbon_csv and gibbon_web into supplier_config
- Scrapers already correctly write to gibbon_web and gibbon_csv
- Added backwards compatibility mapping in fallback path

## Additional Notes

### If You Still See Issues After This

**Check Supabase RLS Policies:**
```sql
-- Verify policies allow authenticated reads
SELECT * FROM pg_policies WHERE tablename IN ('products', 'supplier_config', 'scrape_log');
```

Expected policies:
- `Authenticated users can read products`
- `Authenticated users can read supplier_config`
- `Authenticated users can read scrape_log`

**Check Your Session:**
- Clear browser cookies for prices.gibbontrade.com.au
- Log out and log back in
- Check browser console for 401 Unauthorized errors

**Check Product Data:**
```sql
-- See which sources exist in products table
SELECT source, COUNT(*) as count, COUNT(price) as with_price
FROM products
GROUP BY source
ORDER BY source;
```

You should see rows for: `gibbon_csv`, `gibbon_web`, `kevmor`, `intafloors`

## Files Changed

- `C:\Users\Troy Morgan\OneDrive\Gibbon Trade\index.html` - Frontend fixes
- `C:\Users\Troy Morgan\OneDrive\Gibbon Trade\update-gibbon-sources.sql` - New SQL script
- `C:\Users\Troy Morgan\OneDrive\Gibbon Trade\DEPLOYMENT-CHECKLIST.md` - This file

Files already correct (no changes needed):
- `scraper/scrape.py` - Already writes to gibbon_web ✓
- `scraper/import_gibbon_csv.py` - Already writes to gibbon_csv ✓
- `auth-policies.sql` - RLS policies correct ✓
- `login.html` - Authentication correct ✓
