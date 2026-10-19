#!/usr/bin/env python3
"""Download original WordPress images before deploying. Run where kirova23.com is reachable."""
from pathlib import Path
from urllib.request import Request, urlopen

assets = {'1330360-3.jpg': '2022/07/1330360-3.jpg', 'hands-1-1.png': '2022/08/hands-1-1.png', 'circles-4.png': '2022/08/circles-4.png', 'boxes-1-1.png': '2022/08/boxes-1-1.png', 'image-7.png': '2022/08/image-7.png', 'favicon.jpg': '2022/08/cropped-untitled_artwork-300x300.jpg'}
out = Path(__file__).parent / "assets"
out.mkdir(exist_ok=True)
for filename, remote in assets.items():
    urls = [f"https://www.kirova23.com/wp-content/uploads/{remote}",
            f"http://www.kirova23.com/wp-content/uploads/{remote}"]
    if filename == "1330360-3.jpg":
        urls.append(f"http://54.69.112.107/wp-content/uploads/{remote}")
    for url in urls:
        try:
            with urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=15) as response:
                data = response.read()
                if not response.headers.get("Content-Type", "").startswith("image/"):
                    raise ValueError("Response was not an image")
            (out / filename).write_bytes(data)
            print(f"OK: {filename} ({len(data)} bytes)")
            break
        except Exception as exc:
            print(f"FAILED {url}: {exc}")
    else:
        print(f"MISSING: {filename}. Export this image from WordPress media library.")
