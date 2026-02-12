// Netlify Function: PIN-protected supplier management
// Verifies PIN then adds/removes suppliers in Supabase

import { createClient } from '@supabase/supabase-js';

export default async (req) => {
  if (req.method !== "POST") {
    return new Response(JSON.stringify({ error: "POST only" }), {
      status: 405,
      headers: { "Content-Type": "application/json" }
    });
  }

  try {
    const body = await req.json();
    const { pin, action, data } = body;

    // Verify PIN (same as scrape)
    const correctPin = process.env.SCRAPE_PIN || "5293";
    if (pin !== correctPin) {
      return new Response(JSON.stringify({ error: "Invalid PIN" }), {
        status: 403,
        headers: { "Content-Type": "application/json" }
      });
    }

    // Initialize Supabase client
    const supabaseUrl = process.env.SUPABASE_URL;
    const supabaseKey = process.env.SUPABASE_SERVICE_KEY;

    if (!supabaseUrl || !supabaseKey) {
      return new Response(JSON.stringify({ error: "Supabase not configured" }), {
        status: 500,
        headers: { "Content-Type": "application/json" }
      });
    }

    const supabase = createClient(supabaseUrl, supabaseKey);

    // Perform action
    if (action === 'add') {
      // Add new supplier
      const { key, name, url, type, color, protected: isProtected } = data;

      // Validate required fields
      if (!key || !name || !url || !type) {
        return new Response(JSON.stringify({ error: "Missing required fields" }), {
          status: 400,
          headers: { "Content-Type": "application/json" }
        });
      }

      // Check if supplier already exists
      const { data: existing } = await supabase
        .from('supplier_config')
        .select('key')
        .eq('key', key)
        .single();

      if (existing) {
        return new Response(JSON.stringify({ error: "Supplier key already exists" }), {
          status: 409,
          headers: { "Content-Type": "application/json" }
        });
      }

      // Insert new supplier
      const { error } = await supabase
        .from('supplier_config')
        .insert({
          key,
          name,
          url,
          type,
          color: color || '#3b82f6',
          protected: isProtected || false,
          enabled: true
        });

      if (error) {
        console.error('Supabase insert error:', error);
        return new Response(JSON.stringify({ error: "Failed to add supplier: " + error.message }), {
          status: 500,
          headers: { "Content-Type": "application/json" }
        });
      }

      return new Response(JSON.stringify({
        success: true,
        message: `${name} added successfully!`
      }), {
        status: 200,
        headers: { "Content-Type": "application/json" }
      });

    } else if (action === 'delete') {
      // Remove supplier
      const { key } = data;

      if (!key) {
        return new Response(JSON.stringify({ error: "Missing supplier key" }), {
          status: 400,
          headers: { "Content-Type": "application/json" }
        });
      }

      // Check if protected
      const { data: supplier } = await supabase
        .from('supplier_config')
        .select('protected, name')
        .eq('key', key)
        .single();

      if (supplier && supplier.protected) {
        return new Response(JSON.stringify({ error: "Cannot delete protected supplier" }), {
          status: 403,
          headers: { "Content-Type": "application/json" }
        });
      }

      // Delete supplier
      const { error } = await supabase
        .from('supplier_config')
        .delete()
        .eq('key', key);

      if (error) {
        console.error('Supabase delete error:', error);
        return new Response(JSON.stringify({ error: "Failed to remove supplier: " + error.message }), {
          status: 500,
          headers: { "Content-Type": "application/json" }
        });
      }

      return new Response(JSON.stringify({
        success: true,
        message: `${supplier?.name || key} removed successfully!`
      }), {
        status: 200,
        headers: { "Content-Type": "application/json" }
      });

    } else {
      return new Response(JSON.stringify({ error: "Invalid action" }), {
        status: 400,
        headers: { "Content-Type": "application/json" }
      });
    }

  } catch (e) {
    console.error('Function error:', e);
    return new Response(JSON.stringify({ error: e.message }), {
      status: 500,
      headers: { "Content-Type": "application/json" }
    });
  }
};

export const config = {
  path: "/api/manage-suppliers",
};
