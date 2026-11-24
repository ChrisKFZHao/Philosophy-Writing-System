#!/usr/bin/env python3
"""Flag sentence-level patterns that make Chinese academic prose hard to read.

Paragraphs with fewer than 10 Chinese characters (headings) and sentences with
fewer than 4 are skipped. Lengths and densities count only Han characters in the
analyzed paragraphs.

A run of three or more consecutive sentences with no connective link is flagged
as a bare assertion run (断续句群).

Flags are prompts for judgment, not errors; the script never rewrites text.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path


HAN = re.compile(r"[\u4e00-\u9fff]")
BLANK_LINE = re.compile(r"\n(?:[ \t]*\n)+")
SENTENCE_PART = re.compile(r"[^。！？；]+")
BARE_SENTENCE_PART = re.compile(r"[^。！？]+")
CLAUSE_PART = re.compile(r"[^，、：]+")
LIGHT_VERB = re.compile(r"(进行|作出|做出|加以|予以)(?=[\u4e00-\u9fff]{2})")
ZUOWEI_ZHIYI = re.compile(r"作为[^，。；]{1,20}之一")
YOUYU_SHIDE = re.compile(r"由于[^。；]{1,40}?(使得|使)")
NOT_BUT = re.compile(r"(不是|并非|并不是)[^。；]{1,60}?而是")
LONG_PAREN = re.compile(r"（([^（）]*?)）")
KEY_PLACEHOLDER = re.compile(r"〔[A-Z0-9][A-Z0-9-]{10,}〕")
SIGNPOST = re.compile(r"上一节|下一节|下文先|本节先|本节将|本节首先|先说结论|先看|现在回到|综合以上")
DISCLAIMER = re.compile(r"这并不是说|这不是说|并不意味着|不意味着|不等于|并不排除|不排除|既不是|也不是|并不要求|也不保证")

CHECKS: tuple[tuple[str, str], ...] = (
    ("long-sentence", "长句"),
    ("de-chain", "“的”字链"),
    ("light-verb", "万能动词"),
    ("zuowei-zhiyi", "“作为……之一”"),
    ("youyu-shide", "“由于……使得”"),
    ("not-but", "否定式定义 “不是……而是”"),
    ("dash-insert", "破折号插入"),
    ("long-paren", "长括注"),
    ("key-placeholder", "文献 KEY 占位符"),
    ("meta-phrase", "套话"),
    ("hedge-stack", "限定词堆叠"),
    ("long-paragraph", "长段落"),
    ("bare-run", "断续句群"),
    ("signpost", "章节路标套话"),
    ("disclaimer", "否定式澄清"),
)

# Added only when --glossary is given, so the default report stays unchanged.
GLOSSARY_CHECKS: tuple[tuple[str, str], ...] = (
    ("glossary-gloss", "术语括注与术语表不符"),
    ("glossary-avoid", "出现术语表禁用译名"),
    ("glossary-gloss-repeat", "同一英文术语重复括注"),
)

GLOSS_PAREN = re.compile(
    r"[（(][ \t]*([A-Za-zﬀ-ﬆ][A-Za-zﬀ-ﬆ \t’'\-]*?)[ \t]*[）)]")
HAN_TAIL = re.compile(r"[一-鿿]+$")
# A rendering may be quoted, so a closing quote sits between it and the gloss.
GLOSS_CLOSERS = "”」』）)]】’" + "\"'"

_TRANSLATE = None


def translate_module():
    """Load translate.py so its glossary parser stays the only one."""
    global _TRANSLATE
    if _TRANSLATE is None:
        path = Path(__file__).resolve().parent / "translate.py"
        spec = importlib.util.spec_from_file_location("prose_lint_translate", path)
        if spec is None or spec.loader is None:
            raise OSError(f"cannot load {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _TRANSLATE = module
    return _TRANSLATE


def load_glossary_entries(paths: list[Path]) -> list[dict]:
    """Parse one or more glossary files, keeping the first rendering per term."""
    module = translate_module()
    entries: list[dict] = []
    seen: set[str] = set()
    for path in paths:
        for entry in module.parse_glossary_file(path):
            key = entry["en"].strip().lower()
            if key not in seen:
                seen.add(key)
                entries.append(entry)
    return entries

META_PHRASES = (
    "值得注意的是",
    "需要指出的是",
    "需要注意的是",
    "不难看出",
    "在这个意义上",
    "在此意义上",
    "这意味着",
    "问题在于",
    "关键在于",
)

HEDGES = (
    "可能",
    "或许",
    "在某种意义上",
    "至少",
    "不一定",
    "未必",
    "并不必然",
    "在一定程度上",
)

CONNECTIVES = (
    "首先",
    "其次",
    "再次",
    "最后",
    "然而",
    "但是",
    "因此",
    "所以",
    "换言之",
    "也就是说",
    "事实上",
    "实际上",
    "显然",
    "由此可见",
    "综上",
    "进一步",
    "总之",
)

LINKS = (
    "因此", "所以", "既然", "然而", "但", "而", "于是", "因为", "即使", "如果",
    "只要", "那么", "就", "却", "也就是说", "换言之", "相反", "同时", "可见",
    "由此", "否则", "只有", "才", "虽然", "尽管", "可是", "不过", "因而", "从而",
    "进而", "这样",
)

JUDGMENT = "Flags are prompts for judgment, not errors; the script never rewrites text."
EXCERPT_LIMIT = 40


def han_count(text: str) -> int:
    return len(HAN.findall(text))


def normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n")


def split_parts(text: str, pattern: re.Pattern[str], minimum_han: int = 0) -> list[tuple[str, int]]:
    """Split on a delimiter-excluding pattern, keeping each part's offset in text."""
    parts: list[tuple[str, int]] = []
    for match in pattern.finditer(text):
        raw = match.group()
        lead = len(raw) - len(raw.lstrip())
        part = raw.strip()
        if not part or han_count(part) < minimum_han:
            continue
        parts.append((part, match.start() + lead))
    return parts


def split_paragraphs(text: str) -> list[str]:
    text = normalize_newlines(text)
    chunks = BLANK_LINE.split(text) if BLANK_LINE.search(text) else text.split("\n")
    paragraphs = []
    for chunk in chunks:
        paragraph = chunk.strip()
        if han_count(paragraph) >= 10:
            paragraphs.append(paragraph)
    return paragraphs


def split_all_paragraphs(text: str) -> list[str]:
    """Every non-empty paragraph; glossary checks are not length-filtered."""
    text = normalize_newlines(text)
    chunks = BLANK_LINE.split(text) if BLANK_LINE.search(text) else text.split("\n")
    return [chunk.strip() for chunk in chunks if chunk.strip()]


def split_sentences(paragraph: str) -> list[tuple[str, int]]:
    return split_parts(paragraph, SENTENCE_PART, minimum_han=4)


def split_clauses(sentence: str) -> list[tuple[str, int]]:
    return split_parts(sentence, CLAUSE_PART)


def excerpt(text: str, start: int, end: int, limit: int = EXCERPT_LIMIT) -> str:
    """Return at most limit characters around text[start:end], on one line."""
    if len(text) <= limit:
        piece = text
    elif end - start >= limit:
        piece = text[start:start + limit]
    else:
        span = end - start
        pad = limit - span
        before = min(start, pad // 2)
        after = min(len(text) - end, pad - before)
        before = min(start, pad - after)
        piece = text[start - before:end + after]
    return re.sub(r"\s+", " ", piece).strip()


def record(
    found: dict[str, list[dict]],
    check_id: str,
    paragraph_number: int,
    paragraph: str,
    start: int,
    end: int,
) -> None:
    found[check_id].append({
        "paragraph": paragraph_number,
        "excerpt": excerpt(paragraph, start, end),
    })


def density(count: int, chars: int) -> float:
    return round(count * 1000 / chars, 1) if chars else 0.0


def glossary_excerpt(paragraph: str, start: int, end: int, note: str,
                     limit: int = EXCERPT_LIMIT) -> str:
    return f"{excerpt(paragraph, start, end, limit)} ⇢ {note}"


def inside_quotes(text: str, offset: int) -> bool:
    prefix = text[:offset]
    return (prefix.count("「") > prefix.count("」")
            or prefix.count("“") > prefix.count("”"))


def run_glossary_checks(found: dict[str, list[dict]], paragraphs: list[str],
                        entries: list[dict]) -> None:
    normalize = translate_module().normalize_ligatures
    by_en: dict[str, dict] = {}
    for entry in entries:
        by_en.setdefault(entry["en"].strip().lower(), entry)

    avoids: list[tuple[dict, str]] = []
    seen_avoids: set[tuple[str, str]] = set()
    for entry in entries:
        for variant in entry.get("avoid") or []:
            key = (variant, entry["zh"])
            if variant and key not in seen_avoids:
                seen_avoids.add(key)
                avoids.append((entry, variant))

    occurrences: dict[str, list[tuple[int, int, int, str]]] = {}
    for paragraph_number, paragraph in enumerate(paragraphs, start=1):
        for match in GLOSS_PAREN.finditer(paragraph):
            english = normalize(match.group(1)).strip().lower()
            entry = by_en.get(english)
            if entry is None:
                continue
            occurrences.setdefault(english, []).append(
                (paragraph_number, match.start(), match.end(), paragraph))
            before = paragraph[:match.start()].rstrip().rstrip(GLOSS_CLOSERS)
            tail = HAN_TAIL.search(before)
            chinese = tail.group(0) if tail else ""
            if not chinese.endswith(entry["zh"]):
                found["glossary-gloss"].append({
                    "paragraph": paragraph_number,
                    "excerpt": glossary_excerpt(
                        paragraph, match.start(), match.end(),
                        f"见「{chinese or '（无中文）'}」，应为「{entry['zh']}」"),
                })

    for english, items in occurrences.items():
        if len(items) < 2:
            continue
        entry = by_en[english]
        for paragraph_number, start, end, paragraph in items[1:]:
            found["glossary-gloss-repeat"].append({
                "paragraph": paragraph_number,
                "excerpt": glossary_excerpt(
                    paragraph, start, end,
                    f"「{entry['en']}」重复括注（首次在 ¶{items[0][0]}）"),
            })

    for entry, variant in avoids:
        pattern = re.compile(re.escape(variant))
        for paragraph_number, paragraph in enumerate(paragraphs, start=1):
            for match in pattern.finditer(paragraph):
                if inside_quotes(paragraph, match.start()):
                    continue
                found["glossary-avoid"].append({
                    "paragraph": paragraph_number,
                    "excerpt": glossary_excerpt(
                        paragraph, match.start(), match.end(),
                        f"禁用「{variant}」，应用「{entry['zh']}」"),
                })


def compare_metrics(old: dict, new: dict) -> dict:
    return {
        "old_chars": old["chars"],
        "new_chars": new["chars"],
        "net_change": new["chars"] - old["chars"],
        "old_sentence_mean": old["sentence_mean"],
        "new_sentence_mean": new["sentence_mean"],
        "old_over_limit_pct": old["over_limit_pct"],
        "new_over_limit_pct": new["over_limit_pct"],
    }


def analyze(text: str, max_sentence: int = 60, max_paragraph: int = 500,
            glossary: list[dict] | None = None) -> dict:
    text = normalize_newlines(text)
    paragraphs = split_paragraphs(text)
    sentences: list[tuple[int, str, str, int]] = []
    for paragraph_number, paragraph in enumerate(paragraphs, start=1):
        for sentence, offset in split_sentences(paragraph):
            sentences.append((paragraph_number, paragraph, sentence, offset))

    active_checks = list(CHECKS)
    if glossary is not None:
        active_checks.extend(GLOSSARY_CHECKS)
    found: dict[str, list[dict]] = {check_id: [] for check_id, _ in active_checks}

    for paragraph_number, paragraph in enumerate(paragraphs, start=1):
        if han_count(paragraph) > max_paragraph:
            record(found, "long-paragraph", paragraph_number, paragraph, 0, len(paragraph))
        for match in KEY_PLACEHOLDER.finditer(paragraph):
            record(found, "key-placeholder", paragraph_number, paragraph, match.start(), match.end())

    bare_total = 0
    bare_in_runs = 0
    for paragraph_number, paragraph in enumerate(paragraphs, start=1):
        parts = split_parts(paragraph, BARE_SENTENCE_PART, minimum_han=4)
        bare_total += len(parts)
        index = 0
        while index < len(parts):
            if any(link in parts[index][0] for link in LINKS):
                index += 1
                continue
            run_end = index
            while run_end < len(parts) and not any(link in parts[run_end][0] for link in LINKS):
                run_end += 1
            run_length = run_end - index
            if run_length >= 3:
                start = parts[index][1]
                end = parts[run_end - 1][1] + len(parts[run_end - 1][0])
                record(found, "bare-run", paragraph_number, paragraph, start, end)
                bare_in_runs += run_length
            index = run_end

    disclaimer_count = 0
    for paragraph_number, paragraph, sentence, offset in sentences:
        if han_count(sentence) > max_sentence:
            record(found, "long-sentence", paragraph_number, paragraph, offset, offset + len(sentence))

        for clause, clause_offset in split_clauses(sentence):
            if clause.count("的") >= 3:
                start = offset + clause_offset
                record(found, "de-chain", paragraph_number, paragraph, start, start + len(clause))

        for match in LIGHT_VERB.finditer(sentence):
            record(found, "light-verb", paragraph_number, paragraph, offset + match.start(), offset + match.end())

        for match in ZUOWEI_ZHIYI.finditer(sentence):
            record(found, "zuowei-zhiyi", paragraph_number, paragraph, offset + match.start(), offset + match.end())

        for match in YOUYU_SHIDE.finditer(sentence):
            record(found, "youyu-shide", paragraph_number, paragraph, offset + match.start(), offset + match.end())

        for match in NOT_BUT.finditer(sentence):
            record(found, "not-but", paragraph_number, paragraph, offset + match.start(), offset + match.end())

        if sentence.count("——") >= 2:
            record(found, "dash-insert", paragraph_number, paragraph, offset, offset + len(sentence))

        for match in LONG_PAREN.finditer(sentence):
            if han_count(match.group(1)) > 20:
                record(found, "long-paren", paragraph_number, paragraph, offset + match.start(), offset + match.end())

        meta_spans: list[tuple[int, int]] = []
        for phrase in META_PHRASES:
            for match in re.finditer(re.escape(phrase), sentence):
                meta_spans.append((match.start(), match.end()))
        for start, end in sorted(meta_spans):
            record(found, "meta-phrase", paragraph_number, paragraph, offset + start, offset + end)

        hedges = [term for term in HEDGES if term in sentence]
        if len(hedges) >= 2:
            record(found, "hedge-stack", paragraph_number, paragraph, offset, offset + len(sentence))

        for match in SIGNPOST.finditer(sentence):
            record(found, "signpost", paragraph_number, paragraph, offset + match.start(), offset + match.end())

        for match in DISCLAIMER.finditer(sentence):
            record(found, "disclaimer", paragraph_number, paragraph, offset + match.start(), offset + match.end())
            disclaimer_count += 1

    if glossary is not None:
        run_glossary_checks(found, split_all_paragraphs(text), glossary)

    lengths = [han_count(sentence) for _, _, sentence, _ in sentences]
    sentence_count = len(lengths)
    chars = sum(han_count(paragraph) for paragraph in paragraphs)
    body = "\n".join(paragraphs)
    connective_count = sum(body.count(term) for term in CONNECTIVES)
    over_limit = sum(1 for length in lengths if length > max_sentence)
    metrics = {
        "chars": chars,
        "paragraphs": len(paragraphs),
        "sentences": sentence_count,
        "sentence_mean": round(sum(lengths) / sentence_count, 1) if sentence_count else 0.0,
        "over_limit_pct": round(over_limit * 100 / sentence_count, 1) if sentence_count else 0.0,
        "longest_sentence": max(lengths) if lengths else 0,
        "connective_density": density(connective_count, chars),
        "de_density": density(body.count("的"), chars),
        "bare_run_pct": round(bare_in_runs * 100 / bare_total, 1) if bare_total else 0.0,
        "disclaimer_density": density(disclaimer_count, chars),
    }
    checks = {
        check_id: {
            "label": label,
            "count": len(found[check_id]),
            "matches": found[check_id],
        }
        for check_id, label in active_checks
    }
    return {"metrics": metrics, "checks": checks}


def read_text(path: Path) -> str:
    return normalize_newlines(path.read_text(encoding="utf-8"))


def format_text(result: dict, examples: int) -> str:
    metrics = result["metrics"]
    lines = [
        f"文件: {result['file']}",
        f"汉字数: {metrics['chars']}",
        f"段落数: {metrics['paragraphs']}",
        f"句子数: {metrics['sentences']}",
        f"平均句长: {metrics['sentence_mean']:.1f}",
        f"超限句占比: {metrics['over_limit_pct']:.1f}%",
        f"最长句长: {metrics['longest_sentence']}",
        f"连接词密度: {metrics['connective_density']:.1f} / 千字",
        f"“的”密度: {metrics['de_density']:.1f} / 千字",
        f"断续句占比: {metrics['bare_run_pct']:.1f}%",
        f"否定式澄清密度: {metrics['disclaimer_density']:.1f} / 千字",
    ]
    compare = result.get("compare")
    if compare is not None:
        lines.append(
            f"对比: 旧 {compare['old_chars']} → 新 {compare['new_chars']} 字"
            f"（{compare['net_change']:+d}）；"
            f"平均句长 {compare['old_sentence_mean']:.1f} → {compare['new_sentence_mean']:.1f}；"
            f"超限句占比 {compare['old_over_limit_pct']:.1f}% → {compare['new_over_limit_pct']:.1f}%"
        )
    for check_id, item in result["checks"].items():
        if not item["count"]:
            continue
        lines.append("")
        lines.append(f"{check_id} {item['label']}: {item['count']}")
        for match in item["matches"][:max(examples, 0)]:
            lines.append(f"  ¶{match['paragraph']} {match['excerpt']}")
    lines.append("")
    lines.append(JUDGMENT)
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Flag sentence-level patterns in Chinese academic prose."
    )
    parser.add_argument("file", type=Path)
    parser.add_argument("--compare", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--max-sentence", type=int, default=60)
    parser.add_argument("--max-paragraph", type=int, default=500)
    parser.add_argument("--examples", type=int, default=5)
    parser.add_argument("--glossary", type=Path, action="append",
                        help="project glossary Markdown; repeatable")
    args = parser.parse_args()

    try:
        text = read_text(args.file)
        old_text = read_text(args.compare) if args.compare is not None else None
        glossary = load_glossary_entries(args.glossary) if args.glossary else None
    except (OSError, UnicodeError) as error:
        print(f"ERROR {error}", file=sys.stderr)
        return 2

    analysis = analyze(text, args.max_sentence, args.max_paragraph, glossary)
    result: dict = {
        "file": str(args.file),
        "metrics": analysis["metrics"],
        "checks": analysis["checks"],
    }
    if old_text is not None:
        old = analyze(old_text, args.max_sentence, args.max_paragraph)
        result["compare"] = compare_metrics(old["metrics"], result["metrics"])

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_text(result, args.examples))
    return 0


if __name__ == "__main__":
    # Output carries ¶, ⇢ and CJK text; a GBK console or pipe on Windows cannot encode the first two.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    raise SystemExit(main())
