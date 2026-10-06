#!/usr/bin/env python3
from pathlib import Path
import shutil
import sys
import re

GTM_ID = "GTM-TQV6TN2"

GTM_HEAD = f"""<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','{GTM_ID}');</script>
<!-- End Google Tag Manager -->"""

GTM_BODY = f"""<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->"""

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 add_gtm.py path/to/file.html")
        raise SystemExit(2)

    path = Path(sys.argv[1])

    if path.suffix.lower() not in {".html", ".htm"}:
        print("Refusing: file must be .html or .htm")
        raise SystemExit(2)

    if not path.exists():
        print(f"Not found: {path}")
        raise SystemExit(2)

    text = path.read_text(encoding="utf-8", errors="strict")

    if GTM_ID in text:
        print(f"No change: {GTM_ID} is already present in {path.name}")
        return

    if not re.search(r"<head(?:\s[^>]*)?>", text, flags=re.I):
        print("Refusing: no <head> tag found")
        raise SystemExit(2)

    if not re.search(r"<body(?:\s[^>]*)?>", text, flags=re.I):
        print("Refusing: no <body> tag found")
        raise SystemExit(2)

    backup = path.with_suffix(path.suffix + ".bak")
    shutil.copy2(path, backup)

    text = re.sub(
        r"(<head(?:\s[^>]*)?>)",
        r"\1\n" + GTM_HEAD,
        text,
        count=1,
        flags=re.I,
    )
    text = re.sub(
        r"(<body(?:\s[^>]*)?>)",
        r"\1\n" + GTM_BODY,
        text,
        count=1,
        flags=re.I,
    )

    path.write_text(text, encoding="utf-8")
    print(f"Updated: {path}")
    print(f"Backup:  {backup}")

if __name__ == "__main__":
    main()
