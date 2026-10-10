"""PWA 아이콘 생성: python tools/make_icons.py  ->  public/icons/*.png
산 모티프를 초록 그라데이션 위에 그린다.
"""
from pathlib import Path

from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent.parent / "public" / "icons"
OUT.mkdir(parents=True, exist_ok=True)
SS = 4  # 안티앨리어싱용 확대 배율


def gradient(size):
    """대각선 짙은 초록 -> 초록 -> 연두 그라데이션."""
    stops = [(0.0, (11, 61, 46)), (0.55, (18, 117, 79)), (1.0, (62, 200, 128))]
    img = Image.new("RGB", (size, size))
    px = img.load()
    for y in range(size):
        for x in range(size):
            t = (x + y) / (2 * (size - 1))
            for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
                if t <= t1:
                    k = (t - t0) / (t1 - t0)
                    px[x, y] = tuple(round(a + (b - a) * k) for a, b in zip(c0, c1))
                    break
    return img


def atom(size, scale):
    """영남알프스를 닮은 산줄기와 해를 그린다. scale: 그림이 차지하는 비율."""
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    w = size * scale
    x0, y0 = (size - w) / 2, size / 2 + w * 0.26  # 산 밑변

    def pt(fx, fy):
        return (x0 + w * fx, y0 - w * fy)
    d.polygon([pt(0, 0), pt(0.22, 0.36), pt(0.36, 0.18), pt(0.58, 0.62), pt(1, 0), ], fill=(255, 255, 255, 240))
    d.polygon([pt(0.58, 0.62), pt(0.66, 0.46), pt(0.62, 0.40), pt(0.5, 0.40)], fill=(190, 240, 215, 255))
    sx, sy = pt(0.78, 0.66)
    r = w * 0.095
    d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 214, 102, 255))
    return layer


def make(size, scale, name, rounded=True):
    big = size * SS
    img = gradient(big).convert("RGBA")
    img = Image.alpha_composite(img, atom(big, scale))
    if rounded:  # 둥근 모서리(일반 아이콘). maskable 은 OS 가 직접 자르므로 꽉 채운다.
        mask = Image.new("L", (big, big), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, big - 1, big - 1], radius=int(big * 0.22), fill=255)
        img.putalpha(mask)
    img = img.resize((size, size), Image.LANCZOS)
    img.save(OUT / name, optimize=True)
    print(name, size)


make(512, 0.80, "icon-512.png")
make(192, 0.80, "icon-192.png")
make(512, 0.62, "maskable-512.png", rounded=False)   # 안전 영역(중앙 80%) 안에 그림을 둔다
make(180, 0.78, "apple-touch-icon.png", rounded=False)  # iOS 가 직접 둥글게 자른다
make(64, 0.84, "favicon-64.png")
