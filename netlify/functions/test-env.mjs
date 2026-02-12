// Test function to check environment variables
export default async (req) => {
  const hasSupabaseUrl = !!process.env.SUPABASE_URL;
  const hasSupabaseKey = !!process.env.SUPABASE_SERVICE_KEY;
  const hasScrapePIN = !!process.env.SCRAPE_PIN;

  return new Response(JSON.stringify({
    message: "Environment Variable Check",
    SCRAPE_PIN_exists: hasScrapePIN,
    SCRAPE_PIN_value: hasScrapePIN ? "Set (hidden)" : "NOT SET",
    SUPABASE_URL_exists: hasSupabaseUrl,
    SUPABASE_URL_value: hasSupabaseUrl ? process.env.SUPABASE_URL : "NOT SET",
    SUPABASE_SERVICE_KEY_exists: hasSupabaseKey,
    SUPABASE_SERVICE_KEY_value: hasSupabaseKey ? "Set (hidden)" : "NOT SET",
  }, null, 2), {
    status: 200,
    headers: { "Content-Type": "application/json" }
  });
};

export const config = {
  path: "/api/test-env",
};
