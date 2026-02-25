"""
Korean Culture Daily Prompt Generator
매일 한국 문화·역사 테마로 AI 이미지/영상 프롬프트 6종 자동 생성
"""

import os
import json
import hashlib
import datetime
import requests
import anthropic
from pathlib import Path

# ─────────────────────────────────────────────
# 설정
# ─────────────────────────────────────────────

OUTPUTS_DIR = Path("outputs")
OUTPUTS_DIR.mkdir(exist_ok=True)

KOREAN_THEMES = [
    {"title": "조선 왕조 — 궁궐과 달빛",       "emoji": "🏯", "era": "조선시대"},
    {"title": "고려 청자 — 비색의 신비",        "emoji": "🏺", "era": "고려시대"},
    {"title": "삼국시대 — 전사와 철갑",         "emoji": "⚔️",  "era": "삼국시대"},
    {"title": "무속 신앙 — 무당과 영혼",        "emoji": "🔮", "era": "민간신앙"},
    {"title": "한복 미학 — 색동과 바람",        "emoji": "👘", "era": "전통문화"},
    {"title": "조선 야경 — 연등과 달빛",        "emoji": "🏮", "era": "조선시대"},
    {"title": "신라 금관 — 황금과 보석",        "emoji": "👑", "era": "신라시대"},
    {"title": "판소리 — 소리와 한(恨)",         "emoji": "🥁", "era": "전통예술"},
    {"title": "제주 해녀 — 바다와 숨비소리",    "emoji": "🤿", "era": "제주문화"},
    {"title": "고구려 벽화 — 천상의 전사",      "emoji": "🎴", "era": "고구려시대"},
    {"title": "조선 민화 — 호랑이와 까치",      "emoji": "🐯", "era": "조선시대"},
    {"title": "불교 사찰 — 새벽 예불과 안개",   "emoji": "🪷", "era": "불교문화"},
    {"title": "독립운동 — 태극기와 저항",       "emoji": "🚩", "era": "근현대사"},
    {"title": "한국 무예 — 택견과 검도",        "emoji": "🥋", "era": "전통무예"},
    {"title": "한양 도성 — 성벽과 사계절",      "emoji": "🗼", "era": "조선시대"},
]


def day_hash(date_str: str) -> int:
    h = 0
    for c in date_str:
        h = (h * 31 + ord(c)) % 10000
    return h


def get_daily_theme(date_str: str) -> dict:
    idx = day_hash(date_str) % len(KOREAN_THEMES)
    return KOREAN_THEMES[idx]


def output_exists(date_str: str) -> bool:
    return (OUTPUTS_DIR / f"{date_str}.json").exists()


# ─────────────────────────────────────────────
# Claude API 호출
# ─────────────────────────────────────────────

def generate_prompts(date_str: str, theme: dict) -> dict:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    seed = day_hash(date_str)

    system = """당신은 한국 문화·역사 전문 AI 프롬프트 엔지니어입니다.
한국의 역사적 맥락, 미학, 전통 요소를 깊이 이해하고
Midjourney·Stable Diffusion·DALL-E 3·Sora·Runway·Kling AI에 최적화된
고품질 이미지·영상 프롬프트를 생성합니다.
반드시 순수 JSON만 반환하고 다른 텍스트는 일절 포함하지 않습니다."""

    prompt = f"""오늘의 테마: "{theme['title']}"
시대/분류: {theme['era']}
날짜: {date_str} | 시드: {seed}

다음 JSON 구조로 6개 프롬프트를 생성해. JSON만 반환:

{{
  "theme": "{theme['title']}",
  "era": "{theme['era']}",
  "emoji": "{theme['emoji']}",
  "themeDesc": "테마 핵심 설명 (50자 이내, 한국 역사·문화 맥락 포함)",
  "historicalNote": "이 테마의 역사적/문화적 배경 (80자 이내)",
  "items": [
    {{
      "id": 1,
      "category": "IMAGE",
      "platform": "Midjourney",
      "title": "작품 제목 (한국어, 20자 이내)",
      "prompt": "한국 문화 요소를 깊이 반영한 영어 프롬프트 (120~160단어)",
      "tags": ["태그1", "태그2", "태그3"],
      "mood": "분위기 — 한(恨)/흥(興)/멋/정(情) 정서 포함",
      "historicalRef": "참조한 역사적/문화적 요소"
    }},
    {{
      "id": 2,
      "category": "IMAGE",
      "platform": "Stable Diffusion",
      "title": "작품 제목",
      "prompt": "positive prompt (120~150단어)",
      "negative": "negative prompt (40~60단어)",
      "tags": ["태그1", "태그2", "태그3"],
      "mood": "분위기",
      "historicalRef": "역사적 참조"
    }},
    {{
      "id": 3,
      "category": "IMAGE",
      "platform": "DALL-E 3",
      "title": "작품 제목",
      "prompt": "한국 미술 전통을 현대적으로 재해석한 영어 프롬프트 (100~130단어)",
      "tags": ["태그1", "태그2", "태그3"],
      "mood": "분위기",
      "historicalRef": "역사적 참조"
    }},
    {{
      "id": 4,
      "category": "VIDEO",
      "platform": "Sora",
      "title": "영상 제목",
      "prompt": "카메라 무브/조명/계절감 포함 영상 프롬프트 (100~130단어)",
      "duration": "15s",
      "tags": ["태그1", "태그2", "태그3"],
      "mood": "분위기",
      "historicalRef": "역사적 참조"
    }},
    {{
      "id": 5,
      "category": "VIDEO",
      "platform": "Runway Gen-3",
      "title": "영상 제목",
      "prompt": "시네마틱 영상 프롬프트 (80~110단어)",
      "duration": "8s",
      "tags": ["태그1", "태그2", "태그3"],
      "mood": "분위기",
      "historicalRef": "역사적 참조"
    }},
    {{
      "id": 6,
      "category": "VIDEO",
      "platform": "Kling AI",
      "title": "영상 제목",
      "prompt": "한국어+영어 혼합 프롬프트 (60~80단어)",
      "duration": "5s",
      "tags": ["태그1", "태그2", "태그3"],
      "mood": "분위기",
      "historicalRef": "역사적 참조"
    }}
  ]
}}

"{theme['title']}" 테마에 완전히 몰입해서 독창적인 프롬프트를 생성해."""

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=3000,
        system=system,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text
    clean = raw.replace("```json", "").replace("```", "").strip()
    data = json.loads(clean)
    data["date"] = date_str
    data["generatedAt"] = datetime.datetime.utcnow().isoformat() + "Z"
    data["usage"] = {
        "input_tokens": message.usage.input_tokens,
        "output_tokens": message.usage.output_tokens
    }
    return data


# ─────────────────────────────────────────────
# Markdown 렌더링
# ─────────────────────────────────────────────

def to_markdown(data: dict) -> str:
    d = data["date"]
    kst = datetime.datetime.strptime(d, "%Y-%m-%d")
    weekdays = ["월", "화", "수", "목", "금", "토", "일"]
    wd = weekdays[kst.weekday()]
    date_label = f"{kst.year}년 {kst.month}월 {kst.day}일 ({wd})"

    lines = [
        f"# {data.get('emoji','')} {data['theme']}",
        f"",
        f"> **{date_label}** | {data.get('era','')}",
        f"",
        f"{data.get('themeDesc','')}",
        f"",
        f"> 📚 **역사 배경:** {data.get('historicalNote','')}",
        f"",
        f"---",
        f"",
    ]

    image_items = [i for i in data["items"] if i["category"] == "IMAGE"]
    video_items = [i for i in data["items"] if i["category"] == "VIDEO"]

    lines.append("## 🎨 이미지 프롬프트")
    lines.append("")
    for item in image_items:
        lines += [
            f"### {item['id']}. [{item['platform']}] {item['title']}",
            f"",
            f"**분위기:** {item.get('mood','')}  ",
            f"**史 참조:** {item.get('historicalRef','')}  ",
            f"**태그:** {' '.join(['`'+t+'`' for t in item.get('tags',[])])}",
            f"",
            f"```",
            item["prompt"],
            f"```",
        ]
        if "negative" in item:
            lines += [
                f"",
                f"**Negative:**",
                f"```",
                item["negative"],
                f"```",
            ]
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 🎬 영상 프롬프트")
    lines.append("")
    for item in video_items:
        lines += [
            f"### {item['id']}. [{item['platform']}] {item['title']} `{item.get('duration','')}` ",
            f"",
            f"**분위기:** {item.get('mood','')}  ",
            f"**史 참조:** {item.get('historicalRef','')}  ",
            f"**태그:** {' '.join(['`'+t+'`' for t in item.get('tags',[])])}",
            f"",
            f"```",
            item["prompt"],
            f"```",
            f"",
        ]

    lines += [
        "---",
        "",
        f"*generated {data.get('generatedAt','')} · Claude Opus 4*",
        f"*tokens: input {data.get('usage',{}).get('input_tokens',0)} / output {data.get('usage',{}).get('output_tokens',0)}*",
    ]

    return "\n".join(lines)


# ─────────────────────────────────────────────
# Discord 알림
# ─────────────────────────────────────────────

def send_discord(data: dict):
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL", "")
    if not webhook_url:
        return

    theme = data["theme"]
    emoji = data.get("emoji", "🎨")
    era = data.get("era", "")
    desc = data.get("themeDesc", "")
    note = data.get("historicalNote", "")
    date_str = data["date"]

    # 첫 번째 아이템 프롬프트 미리보기
    first = data["items"][0] if data["items"] else {}
    preview = first.get("prompt", "")[:300] + "..." if first.get("prompt") else ""

    fields = []
    for item in data["items"]:
        icon = "🎨" if item["category"] == "IMAGE" else "🎬"
        dur = f" `{item['duration']}`" if item.get("duration") else ""
        fields.append({
            "name": f"{icon} [{item['platform']}]{dur} — {item['title']}",
            "value": f"_{item.get('mood','')}_\n`{'` `'.join(item.get('tags',[]))}`",
            "inline": False
        })

    embed = {
        "title": f"{emoji} {theme}",
        "description": f"**{era}** · {date_str}\n\n{desc}\n\n> 📚 {note}",
        "color": 0xC9A84C,
        "fields": fields[:6],
        "footer": {
            "text": f"Korean Culture Daily Prompt · {data.get('generatedAt','')[:10]}"
        }
    }

    payload = {"embeds": [embed]}
    try:
        res = requests.post(webhook_url, json=payload, timeout=10)
        print(f"Discord 전송: {res.status_code}")
    except Exception as e:
        print(f"Discord 오류: {e}")


# ─────────────────────────────────────────────
# Slack 알림
# ─────────────────────────────────────────────

def send_slack(data: dict):
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL", "")
    if not webhook_url:
        return

    theme = data["theme"]
    emoji = data.get("emoji", "🎨")
    date_str = data["date"]
    desc = data.get("themeDesc", "")
    note = data.get("historicalNote", "")

    items_text = ""
    for item in data["items"]:
        icon = "🎨" if item["category"] == "IMAGE" else "🎬"
        dur = f"({item['duration']})" if item.get("duration") else ""
        items_text += f"• {icon} *[{item['platform']}]{dur}* {item['title']} — _{item.get('mood','')}_\n"

    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": f"{emoji} {theme} — {date_str}"}
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*{desc}*\n📚 {note}"}
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": items_text}
        },
        {
            "type": "context",
            "elements": [{"type": "mrkdwn", "text": f"Korean Culture Daily Prompt · Claude Opus 4"}]
        }
    ]

    try:
        res = requests.post(webhook_url, json={"blocks": blocks}, timeout=10)
        print(f"Slack 전송: {res.status_code}")
    except Exception as e:
        print(f"Slack 오류: {e}")


# ─────────────────────────────────────────────
# 메인
# ─────────────────────────────────────────────

def main():
    # 날짜 결정
    date_str = os.environ.get("DATE_OVERRIDE", "").strip()
    if not date_str:
        # KST = UTC+9
        kst = datetime.timezone(datetime.timedelta(hours=9))
        date_str = datetime.datetime.now(kst).strftime("%Y-%m-%d")

    force = os.environ.get("FORCE_REGEN", "false").lower() == "true"

    print(f"\n{'='*50}")
    print(f"  Korean Culture Daily Prompt Generator")
    print(f"  날짜: {date_str}")
    print(f"{'='*50}\n")

    # 이미 생성됐는지 확인
    json_path = OUTPUTS_DIR / f"{date_str}.json"
    if json_path.exists() and not force:
        print(f"✅ {date_str} 이미 생성됨. 건너뜀 (force_regen=true 로 덮어쓰기 가능)")
        return

    # 테마 결정
    theme = get_daily_theme(date_str)
    print(f"🎯 오늘의 테마: {theme['emoji']} {theme['title']} ({theme['era']})")

    # Claude 호출
    print("🔮 Claude API 호출 중...")
    data = generate_prompts(date_str, theme)
    print(f"✅ 생성 완료! ({data['usage']['output_tokens']} tokens)")

    # JSON 저장
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"💾 JSON 저장: {json_path}")

    # Markdown 저장
    md_path = OUTPUTS_DIR / f"{date_str}.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(to_markdown(data))
    print(f"📝 Markdown 저장: {md_path}")

    # README 인덱스 업데이트
    update_readme(date_str, data)

    # 알림 발송
    send_discord(data)
    send_slack(data)

    print(f"\n✨ 완료! {theme['emoji']} {theme['title']}\n")

    # 결과 미리보기 출력
    print("─" * 50)
    for item in data["items"]:
        icon = "🎨" if item["category"] == "IMAGE" else "🎬"
        print(f"{icon} [{item['platform']}] {item['title']}")
        print(f"   {item.get('mood','')}")
        print()


def update_readme(date_str: str, data: dict):
    """outputs/README.md 인덱스 자동 업데이트"""
    index_path = OUTPUTS_DIR / "README.md"

    # 기존 인덱스 로드
    entries = {}
    if index_path.exists():
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()
        # 기존 엔트리 파싱 (간단하게 재빌드)

    # 모든 JSON 파일 스캔
    all_files = sorted(OUTPUTS_DIR.glob("????-??-??.json"), reverse=True)

    lines = [
        "# 📚 한국 문화 AI 프롬프트 아카이브",
        "",
        "매일 오전 7시 (KST) 자동 생성됩니다.",
        "",
        "| 날짜 | 테마 | 시대 |",
        "|------|------|------|",
    ]

    for f in all_files:
        try:
            with open(f, "r", encoding="utf-8") as fp:
                d = json.load(fp)
            ds = d.get("date", f.stem)
            emoji = d.get("emoji", "")
            theme = d.get("theme", "")
            era = d.get("era", "")
            lines.append(f"| [{ds}]({ds}.md) | {emoji} {theme} | {era} |")
        except:
            pass

    with open(index_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"📋 인덱스 업데이트: {index_path}")


if __name__ == "__main__":
    main()
