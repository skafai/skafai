# /// script
# requires-python = ">=3.11"
# ///
"""Download every shieldcn image referenced by README.md into assets/badges/ and point the
README at the local copies, so the profile never depends on shieldcn being up.

Run after scripts/build_readme.py: uv run scripts/vendor_images.py
"""

import hashlib
import re
import urllib.request
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

ROOT = Path(__file__).parent.parent
OUT = ROOT / "assets" / "badges"
URL = re.compile(r'https://shieldcn\.dev/[^"\s)]+')


def file_name(url: str) -> str:
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    stem = unquote(parsed.path.strip("/").removesuffix(".svg"))
    slug = re.sub(r"[^a-z0-9]+", "-", stem.lower()).strip("-")[:40]
    mode = query.get("mode", [""])[0]
    digest = hashlib.sha1(url.encode()).hexdigest()[:8]
    return "-".join(part for part in (slug, mode, digest) if part) + ".svg"


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "profile-readme-vendor"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def main() -> None:
    readme = ROOT / "README.md"
    text = readme.read_text()
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.svg"):
        old.unlink()
    mapping = {}
    for url in sorted(set(URL.findall(text))):
        target = OUT / file_name(url)
        target.write_bytes(fetch(url.replace("&amp;", "&")))
        mapping[url] = target.relative_to(ROOT).as_posix()
    for url, local in mapping.items():
        text = text.replace(url, local)
    readme.write_text(text)
    print(f"vendored {len(mapping)} images")


if __name__ == "__main__":
    main()
