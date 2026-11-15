"""index.html 안의 쿠팡 상품 사진 주소(ads-partners.coupang.com)를 img/ 폴더에 내려받고,
페이지가 저장소 안 사진을 쓰도록 주소를 바꾼다. (깃허브 액션에서 실행)"""
import hashlib, os, re, urllib.request
html = open("index.html", encoding="utf-8").read()
os.makedirs("img", exist_ok=True)
for url in sorted(set(re.findall(r'img: "(https://ads-partners\.coupang\.com/[^"]+)"', html))):
    name = "img/" + hashlib.sha1(url.encode()).hexdigest()[:12] + ".jpg"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Referer": "https://lsagisu93-ops.github.io/dog/"})
    try:
        data = urllib.request.urlopen(req, timeout=30).read()
    except Exception as e:
        print("실패:", url[:80], e); continue
    if len(data) < 500:
        print("너무 작음:", url[:80], len(data)); continue
    open(name, "wb").write(data)
    html = html.replace(f'img: "{url}"', f'img: "{name}"')
    print("저장:", name, len(data))
open("index.html", "w", encoding="utf-8").write(html)
