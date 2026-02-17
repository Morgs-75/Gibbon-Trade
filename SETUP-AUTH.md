# Authentication Setup Guide

This guide will help you add email authentication to protect your Gibbon Trade pricing data.

## Steps to Enable Authentication

### 1. Update Database Policies

Run the SQL commands in `auth-policies.sql` in your Supabase SQL Editor:
- Go to your Supabase project
- Navigate to SQL Editor
- Copy and paste the contents of `auth-policies.sql`
- Run the query

This will update the Row Level Security policies to require authentication.

### 2. Enable Email Authentication in Supabase

1. Go to your Supabase Dashboard → Authentication → Providers
2. Make sure Email provider is **enabled**
3. Configure email settings:
   - **Confirm email**: Toggle ON if you want users to confirm their email
   - **Secure email change**: Toggle ON (recommended)
4. Optional: Configure email templates under Authentication → Email Templates

### 3. Create Your First User Account

Visit `login.html` in your browser and click "Create Account" to sign up with your email and password.

**Note**: If email confirmation is enabled, check your email for the confirmation link before signing in.

### 4. Update HTML Files to Use Authentication

The main `index.html` has already been updated. For the other pages (`fixed.html`, `insights.html`, `manage-suppliers.html`), you need to:

**Option A: Use the shared auth.js module (recommended)**

Add these lines right after the `<script>` tag that loads Supabase:

```html
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script src="auth.js"></script>
```

Then update your page's initialization code to wait for auth:

```javascript
// Replace your immediate initialization with this:
window.addEventListener('auth-ready', () => {
    // Your initialization code here (loadData(), etc.)
    loadData();
});
```

Add a logout button to the header controls:

```html
<button class="nav-btn" onclick="handleLogout()" title="Sign out">
    🚪 Logout
</button>
```

**Option B: Update each file individually**

See `index.html` for the complete pattern of:
1. Loading Supabase JS library
2. Creating authenticated client
3. Checking auth on page load
4. Using authenticated token in API calls
5. Adding logout button

### 5. Test Your Setup

1. Visit your site - you should be redirected to `login.html`
2. Sign in with your account
3. Verify you can see the pricing data
4. Click Logout - you should be redirected back to login
5. Try accessing pages directly without logging in - should redirect to login

### 6. (Optional) Invite Other Users

To add more users:
- **Self-service**: They can create accounts via the signup form
- **Admin-only**: Disable signups in Supabase (Auth → Settings → Email Auth → Disable Sign-ups) and create user accounts manually in the Supabase dashboard under Authentication → Users

## Troubleshooting

### "403 Forbidden" or "401 Unauthorized" errors
- Make sure you ran the `auth-policies.sql` in your Supabase SQL Editor
- Check that you're logged in (session hasn't expired)
- Try logging out and back in

### Can't create account
- Check that Email provider is enabled in Supabase Auth settings
- If email confirmation is required, check your spam folder
- Look for errors in the browser console (F12)

### Redirects to login immediately after signing in
- Check browser console for errors
- Verify the auth token is being stored correctly
- Make sure the Supabase URL and anon key are correct

## Security Notes

- The anon key is safe to expose in client-side code - it's designed for browser use
- Row Level Security (RLS) policies protect your data at the database level
- Passwords are hashed and never stored in plain text
- Session tokens expire automatically
- Users can only read data (not modify) unless you add additional policies

## Password Reset

To add password reset functionality:
1. Enable password reset emails in Supabase Auth settings
2. Add a "Forgot Password?" link on the login page
3. Use `supabaseClient.auth.resetPasswordForEmail(email)` in your code

## Next Steps

Consider:
- Setting up user roles (admin vs read-only)
- Adding user management page
- Configuring email templates with your branding
- Setting up Magic Link login (passwordless)
