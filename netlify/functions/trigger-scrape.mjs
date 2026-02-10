// Netlify Function: PIN-protected scrape trigger
// Verifies PIN then dispatches the GitHub Actions scrape workflow

export default async (req) => {
  if (req.method !== "POST") {
    return new Response(JSON.stringify({ error: "POST only" }), { status: 405 });
  }

  const body = await req.json();
  const pin = body.pin;

  // Verify PIN
  const correctPin = process.env.SCRAPE_PIN || "5293";
  if (pin !== correctPin) {
    return new Response(JSON.stringify({ error: "Invalid PIN" }), { status: 403 });
  }

  // Trigger GitHub Actions workflow
  const ghToken = process.env.GITHUB_TOKEN;
  if (!ghToken) {
    return new Response(JSON.stringify({ error: "GitHub token not configured" }), { status: 500 });
  }

  try {
    const res = await fetch(
      "https://api.github.com/repos/Morgs-75/Gibbon-Trade/actions/workflows/scrape.yml/dispatches",
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${ghToken}`,
          Accept: "application/vnd.github.v3+json",
          "User-Agent": "Gibbon-Trade-Netlify",
        },
        body: JSON.stringify({ ref: "master" }),
      }
    );

    if (res.status === 204) {
      return new Response(JSON.stringify({ success: true, message: "Scrape triggered! Data will update in ~10 minutes." }));
    } else {
      const text = await res.text();
      return new Response(JSON.stringify({ error: `GitHub API ${res.status}: ${text}` }), { status: 502 });
    }
  } catch (e) {
    return new Response(JSON.stringify({ error: e.message }), { status: 500 });
  }
};

export const config = {
  path: "/api/trigger-scrape",
};
