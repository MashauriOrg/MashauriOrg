# Mashauri tools GTM helper

Purpose: make sure every new HTML tool uploaded to `tools.mashauri.org` is tracked by Google Analytics without manually rebuilding the tracking setup each time.

## Current tracking setup

- Google Tag Manager container: `GTM-TQV6TN2`
- GA4 property/stream used by `mashauri.org` and `tools.mashauri.org`: `G-FY6XPNLQ12`
- Do **not** add the GA4 `gtag.js` snippet directly to new tools. GTM already sends data to GA4.

## Fastest workflow for a new tool

1. Build the HTML tool.
2. Run `python3 add_gtm.py your-tool.html`.
3. The script adds the GTM head and noscript blocks only if they are missing.
4. Upload the resulting HTML file to `tools.mashauri.org/public_html`.
5. Open the live page and use Google Tag Manager Preview once to confirm the GA4 tag fires.

## Alternative: start from the template

Copy `tool-template.html` and build the tool inside it. The GTM code is already present.

## Safety

The helper script:
- refuses to add GTM twice;
- does not add a direct GA4 snippet;
- creates a `.bak` backup before modifying a file;
- only modifies HTML files;
- inserts the GTM script immediately after `<head>`;
- inserts the noscript block immediately after `<body>`.

If a tool stores user state in `localStorage`, adding GTM does not normally erase that stored state, provided the page URL and storage key remain unchanged.
