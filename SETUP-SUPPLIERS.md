# Supplier Management Setup Guide

## Overview

The new Supplier Management page allows you to add or remove competitors for price comparison and scraping purposes, all protected by the same PIN that protects scraping.

## Setup Steps

### 1. Update Database Schema

Run the updated schema to add the `supplier_config` table:

```bash
# Apply schema updates
psql $DATABASE_URL -f schema.sql
```

Or run directly in Supabase SQL Editor:
```sql
-- Copy and paste the new table definition from schema.sql
```

### 2. Initialize Default Suppliers

Populate the table with current suppliers:

```bash
psql $DATABASE_URL -f init-suppliers.sql
```

Or run in Supabase SQL Editor:
```sql
-- Copy and paste from init-suppliers.sql
```

### 3. Install Dependencies (if needed)

The Netlify function requires `@supabase/supabase-js`. Update your `package.json`:

```json
{
  "dependencies": {
    "@supabase/supabase-js": "^2.39.0"
  }
}
```

Then run:
```bash
cd netlify/functions
npm install
```

### 4. Verify Environment Variables

Ensure these variables are set in Netlify:

- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_SERVICE_KEY` - Service role key (not anon key!)
- `SCRAPE_PIN` - 4-digit PIN (default: 5293)

### 5. Deploy

Push changes to trigger Netlify deployment:

```bash
git add .
git commit -m "Add supplier management page"
git push
```

## Usage

### Access the Page

Navigate to: `https://your-site.netlify.app/manage-suppliers.html`

Or click **🏪 Suppliers** in the navigation menu on any page.

### Add a New Supplier

1. Fill in the form:
   - **Supplier Name**: Display name (e.g., "Floor Supplies Australia")
   - **Supplier Key**: Internal identifier (e.g., "floorsupplies") - lowercase, no spaces
   - **Website URL**: Full URL including https://
   - **Scraper Type**:
     - `WooCommerce` - for sites using WooCommerce Store API
     - `Shopify` - for sites using Shopify products.json API
     - `Custom` - for sites needing custom scraping logic
   - **Display Color**: Hex color for UI elements

2. Click **Add Supplier**
3. Enter your 4-digit PIN
4. Supplier will be added to the database

### Remove a Supplier

1. Click **🗑️ Remove** next to the supplier
2. Confirm the removal
3. Enter your 4-digit PIN
4. Supplier will be removed

**Note**: Protected suppliers (like Gibbon Trade) cannot be removed.

## Database Structure

### supplier_config table

| Column | Type | Description |
|--------|------|-------------|
| id | BIGSERIAL | Primary key |
| key | TEXT | Unique identifier (e.g., 'kevmor') |
| name | TEXT | Display name |
| url | TEXT | Base website URL |
| type | TEXT | Scraper type: 'woocommerce', 'shopify', or 'custom' |
| color | TEXT | Hex color for UI (#3b82f6) |
| protected | BOOLEAN | Cannot be deleted if true |
| enabled | BOOLEAN | Whether to scrape this supplier |
| created_at | TIMESTAMPTZ | When added |
| updated_at | TIMESTAMPTZ | Last modified |

## API Endpoint

**POST** `/api/manage-suppliers`

### Request Body

```json
{
  "pin": "5293",
  "action": "add|delete",
  "data": {
    "key": "supplier-key",
    "name": "Supplier Name",
    "url": "https://example.com",
    "type": "woocommerce",
    "color": "#3b82f6"
  }
}
```

### Response

Success:
```json
{
  "success": true,
  "message": "Supplier Name added successfully!"
}
```

Error:
```json
{
  "error": "Invalid PIN"
}
```

## Security

- All changes require PIN authentication
- Same PIN as scrape trigger (configured via `SCRAPE_PIN` environment variable)
- Protected suppliers cannot be deleted
- Uses Supabase RLS policies for database access

## Future Updates to Scraper

To make the scraper read from the database instead of hardcoded suppliers:

1. Update `scraper/scrape.py` to fetch suppliers from `supplier_config` table
2. Filter by `enabled = true`
3. Use the `type` field to determine which scraper function to use
4. This allows dynamic scraping without code changes

## Troubleshooting

### "Supabase not configured" error
- Check that `SUPABASE_URL` and `SUPABASE_SERVICE_KEY` are set in Netlify environment variables
- Ensure you're using the service_role key, not the anon key

### "Invalid PIN" error
- Verify the PIN matches the `SCRAPE_PIN` environment variable
- Default PIN is 5293 if not set

### Suppliers not loading
- Check that the `supplier_config` table exists
- Run `init-suppliers.sql` to populate default data
- Check browser console for errors
- Verify RLS policies are set correctly

### Function not found
- Ensure `netlify/functions/manage-suppliers.mjs` is deployed
- Check Netlify function logs for errors
- Verify `@supabase/supabase-js` is installed
