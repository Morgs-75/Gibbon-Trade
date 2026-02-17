// Shared authentication module for Gibbon Trade
// Include this script on all protected pages

const SUPABASE_URL = 'https://ualogaryduudrnozmoyx.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVhbG9nYXJ5ZHV1ZHJub3ptb3l4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA3NjQyOTcsImV4cCI6MjA4NjM0MDI5N30.qdsd1YKj8VjafV1lxA9p0iqSONfH5TDQyi41ljSYFhs';

// Initialize Supabase client
const { createClient } = supabase;
const supabaseClient = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
let authToken = null;
let currentUser = null;

// Check authentication on page load
async function checkAuth() {
    const { data: { session } } = await supabaseClient.auth.getSession();
    if (!session) {
        window.location.href = 'login.html';
        return false;
    }
    authToken = session.access_token;
    currentUser = session.user;
    return true;
}

// Logout function
async function handleLogout() {
    await supabaseClient.auth.signOut();
    window.location.href = 'login.html';
}

// Authenticated fetch to Supabase REST API
async function sbFetch(path) {
    const headers = {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': `Bearer ${authToken}`,
    };
    const res = await fetch(`${SUPABASE_URL}/rest/v1/${path}`, { headers });
    if (!res.ok) {
        if (res.status === 401) {
            // Unauthorized - redirect to login
            window.location.href = 'login.html';
            return;
        }
        throw new Error(`Supabase ${res.status}: ${await res.text()}`);
    }
    return res.json();
}

// Initialize auth on page load
(async () => {
    await checkAuth();
    // Trigger custom event so pages know auth is ready
    window.dispatchEvent(new Event('auth-ready'));
})();
