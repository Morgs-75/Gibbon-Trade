# How to Identify Scraper Type

## Quick Reference

| Scraper Type | Best For | Detection |
|--------------|----------|-----------|
| **WooCommerce** | WordPress + WooCommerce stores | Check for `/wp-json/wc/store/v1/products` |
| **Shopify** | Shopify stores | Check for `/products.json` |
| **Custom** | Everything else | Requires custom scraping code |

---

## Method 1: Quick URL Test

### Test for WooCommerce:
Try accessing: `https://[website]/wp-json/wc/store/v1/products`

**Example:**
```
https://intafloors.com.au/wp-json/wc/store/v1/products
```

✅ **If you see JSON data** → Use **WooCommerce**
❌ **If you get 404 or error** → Not WooCommerce

### Test for Shopify:
Try accessing: `https://[website]/products.json?limit=1`

**Example:**
```
https://gluesntools.com.au/products.json?limit=1
```

✅ **If you see JSON data** → Use **Shopify**
❌ **If you get 404 or error** → Not Shopify

---

## Method 2: Browser Developer Tools

1. Open the website in your browser
2. Press **F12** to open Developer Tools
3. Go to **Network** tab
4. Refresh the page
5. Look for requests containing:
   - `wp-json` → **WooCommerce**
   - `cdn.shopify.com` or `/products.json` → **Shopify**

---

## Method 3: View Page Source

### WooCommerce Signs:
- Contains `wp-content`
- Has `woocommerce` in HTML
- Uses `/wp-json/` API endpoints
- Often has WordPress branding in footer

**View source and search for:**
```
wp-content
wp-json
woocommerce
```

### Shopify Signs:
- Contains `cdn.shopify.com`
- Has `Shopify.` JavaScript variables
- Often has "Powered by Shopify" in footer

**View source and search for:**
```
shopify
cdn.shopify.com
myshopify.com
```

---

## Current Suppliers (Reference)

| Supplier | Type | How We Know |
|----------|------|-------------|
| Kevmor | Custom | PrestaShop (different platform) |
| Intafloors | WooCommerce | `/wp-json/wc/store/v1/products` works |
| Gibbon Trade | WooCommerce | `/wp-json/wc/store/v1/products` works |
| Marques | WooCommerce | WordPress + WooCommerce |
| Floor Trade | WooCommerce | WordPress + WooCommerce |
| Glues N Tools | Shopify | `/products.json` works |
| Homely | WooCommerce | WordPress + WooCommerce |

---

## When to Use "Custom"

Use **Custom** when:
- ❌ `/wp-json/wc/store/v1/products` doesn't work
- ❌ `/products.json` doesn't work
- ✅ The site uses a different platform (Magento, PrestaShop, custom-built, etc.)

**Note:** Custom scrapers require code changes in `scraper/scrape.py` to implement.

---

## Step-by-Step: Adding a New Supplier

### Example: Adding "Floor Supplies Australia"

**1. Check WooCommerce:**
```
https://floorsuppliesaustralia.com.au/wp-json/wc/store/v1/products
```

**2. Check Shopify:**
```
https://floorsuppliesaustralia.com.au/products.json?limit=1
```

**3. Results:**
- ✅ WooCommerce returns JSON → Choose **WooCommerce**
- ✅ Shopify returns JSON → Choose **Shopify**
- ❌ Both return errors → Choose **Custom** (requires dev work)

**4. Fill in the form:**
- Supplier Name: `Floor Supplies Australia`
- Supplier Key: `floorsupplies` (lowercase, no spaces)
- Website URL: `https://floorsuppliesaustralia.com.au`
- Scraper Type: `WooCommerce` (or whatever you found)
- Display Color: Pick any color

---

## Testing Your Choice

After adding a supplier, you can test if it works by:

1. **Trigger a scrape** from the main page (Refresh Data button)
2. **Wait 10-15 minutes** for scraping to complete
3. **Check if products appear** for that supplier
4. **Look at scrape logs** in Supabase:
   ```sql
   SELECT * FROM scrape_log
   WHERE source = 'your-supplier-key'
   ORDER BY completed_at DESC
   LIMIT 1;
   ```

---

## Common Platforms

| Platform | Scraper Type | Notes |
|----------|--------------|-------|
| WordPress + WooCommerce | WooCommerce | Most common |
| Shopify | Shopify | Second most common |
| PrestaShop | Custom | Like Kevmor |
| Magento | Custom | Requires custom code |
| BigCommerce | Custom | Requires custom code |
| Custom/Static | Custom | Requires custom code |

---

## Need Help?

If you're unsure:
1. Try both WooCommerce and Shopify URL tests
2. If both fail, look at page source for clues
3. When in doubt, choose **Custom** (won't break anything, just won't scrape until code is added)
4. You can always edit the supplier type later by deleting and re-adding

---

## Quick Commands (Copy & Paste)

Test any website by replacing `WEBSITE-URL`:

**WooCommerce Test:**
```bash
curl -s "https://WEBSITE-URL/wp-json/wc/store/v1/products?per_page=1" | head -20
```

**Shopify Test:**
```bash
curl -s "https://WEBSITE-URL/products.json?limit=1" | head -20
```

If you see JSON data, that scraper type works! If you see HTML or error, it doesn't.
