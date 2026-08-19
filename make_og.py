# -*- coding: utf-8 -*-
"""
OG 이미지(1200x630) 생성 — 법령 MCP 실무 프롬프트 20선
index.html 의 ink/cream/gold 미니멀 팔레트 적용

사용법: python make_og.py
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent
W, H = 1200, 630

# index.html :root 변수와 동일
INK = (26, 26, 26)        # --ink  #1A1A1A
PAPER = (255, 255, 255)   # --paper
CREAM = (245, 240, 232)   # --cream #F5F0E8
GOLD = (201, 169, 97)     # --gold  #C9A961
MUTED = (138, 138, 138)   # --muted #8A8A8A
RULE = (229, 229, 229)    # --rule  #E5E5E5

FONTS = Path("C:/Windows/Fonts")


def font(name, size):
    for cand in (FONTS / name,
                 Path("/usr/share/fonts/truetype/noto") / name,
                 Path("/usr/share/fonts/opentype/noto") / name):
        if cand.exists():
            return ImageFont.truetype(str(cand), size)
    return ImageFont.load_default()


f_black = lambda s: font("NotoSansKR-Black.ttf", s)
f_bold = lambda s: font("NotoSansKR-Bold.ttf", s)
f_med = lambda s: font("NotoSansKR-Medium.ttf", s)
f_reg = lambda s: font("NotoSansKR-Regular.ttf", s)


def text_w(d, s, fnt):
    return d.textbbox((0, 0), s, font=fnt)[2]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # 우측 크림 블록 (페이지의 .chip / .notice 톤)
    d.rectangle([W - 300, 0, W, H], fill=CREAM)

    # 상단 골드 라인
    d.rectangle([0, 0, W, 8], fill=GOLD)

    L = 76  # 좌측 여백

    # eyebrow — 페이지 .kick 과 동일 문구
    d.text((L, 92), "안양대학교 국비교육 특강 · 2026. 8. 20",
           font=f_bold(24), fill=GOLD)

    # 타이틀 (헤드라인 두 줄, 숫자만 골드)
    d.text((L, 146), "법령 MCP 실무 프롬프트", font=f_black(66), fill=INK)
    y2 = 232
    d.text((L, y2), "20선", font=f_black(66), fill=GOLD)
    n_w = text_w(d, "20선", f_black(66))
    # 타이틀 밑 굵은 룰 (페이지 header border-bottom 3px 대응)
    d.rectangle([L, y2 + 96, L + 560, y2 + 99], fill=INK)

    # 설명
    d.text((L, 366),
           "AI가 국가법령정보(법제처)를 직접 조회하게 만든 뒤,",
           font=f_reg(27), fill=(85, 85, 85))
    d.text((L, 404),
           "실무에 바로 쓰는 프롬프트 모음",
           font=f_reg(27), fill=(85, 85, 85))

    # 카테고리 칩 (페이지 필터와 동일 구성)
    chips = [("기본", "4"), ("부서별", "8"), ("문서작성", "4"), ("심화", "4")]
    x, y = L, 472
    for label, cnt in chips:
        txt = f"{label} {cnt}"
        tw = text_w(d, txt, f_bold(23))
        w = tw + 40
        d.rounded_rectangle([x, y, x + w, y + 50], radius=25,
                            fill=CREAM, outline=RULE, width=1)
        d.text((x + 20, y + 11), txt, font=f_bold(23), fill=INK)
        x += w + 12

    # 하단 구분선 + 크레딧
    d.rectangle([L, 566, W - 340, 567], fill=RULE)
    d.text((L, 584), "메이랜드AI비즈랩 & AICLab · 김진수 소장",
           font=f_med(22), fill=MUTED)

    # 우측 크림 블록 안 — 큰 숫자 모티프
    rx = W - 300
    d.text((rx + 46, 214), "20", font=f_black(150), fill=GOLD)
    d.text((rx + 52, 386), "PROMPTS", font=f_bold(30), fill=INK)
    d.rectangle([rx + 54, 434, rx + 190, 437], fill=INK)
    d.text((rx + 54, 456), "복사해서 바로", font=f_reg(21), fill=(85, 85, 85))
    d.text((rx + 54, 486), "붙여넣기", font=f_reg(21), fill=(85, 85, 85))

    out = BASE / "og-image.png"
    img.save(out, "PNG", optimize=True)
    print(f"saved: {out}  ({W}x{H}, {out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
