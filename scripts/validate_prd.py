#!/usr/bin/env python3
"""Validate the structural contract of a Chinese Lean or Standard PRD."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SECTION_RULES = {
    "decision_summary": ["管理层决策摘要", "决策摘要", "executive summary"],
    "problem": ["问题", "背景", "why now", "产品判断"],
    "users": ["目标用户", "用户与场景", "用户场景", "核心场景"],
    "goals": ["目标与成功", "产品目标", "成功标准", "成功指标"],
    "scope": ["范围", "本期范围"],
    "out_of_scope": ["非范围", "不包含", "非目标"],
    "flow_or_features": ["核心流程", "用户流程", "功能需求", "功能地图", "核心功能"],
    "acceptance": ["验收标准", "acceptance criteria"],
    "risk": ["风险", "依赖"],
    "open_questions": ["待确认", "开放问题", "open questions", "决策记录"],
    "product_judgment": ["产品原则", "关键判断", "why now"],
    "state_exception_permission": ["状态", "异常", "权限", "失败", "恢复"],
    "release_measurement": ["发布", "灰度", "回滚", "衡量", "复盘"]
}

LEAN_REQUIRED = [
    "decision_summary", "problem", "users", "goals", "scope", "out_of_scope",
    "flow_or_features", "acceptance", "risk", "open_questions"
]
STANDARD_REQUIRED = LEAN_REQUIRED + [
    "product_judgment", "state_exception_permission", "release_measurement"
]


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value.lower()).strip()


def has_any(text: str, phrases: list[str]) -> bool:
    normalized = normalize(text)
    return any(normalize(phrase) in normalized for phrase in phrases)


def infer_profile(text: str) -> str:
    # Fail safe: only an explicitly labelled Lean document receives the lighter gate.
    # Otherwise use Standard so a structurally incomplete PRD cannot evade checks.
    first_screen = text[:800]
    return "lean" if re.search(r"\bLean\s+PRD\b|轻量(?:版)?\s*PRD", first_screen, flags=re.I) else "standard"


def validate(text: str, requested_profile: str) -> dict[str, object]:
    profile = infer_profile(text) if requested_profile == "auto" else requested_profile
    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    headings = "\n".join(re.findall(r"^#{2,4}\s+(.+)$", text, flags=re.M))

    if not re.search(r"^#\s+\S+", text, flags=re.M):
        errors.append({"code": "missing_h1", "message": "缺少文档一级标题。"})

    required = STANDARD_REQUIRED if profile == "standard" else LEAN_REQUIRED
    for key in required:
        if not has_any(headings, SECTION_RULES[key]):
            errors.append({"code": f"missing_{key}", "message": f"缺少可识别的章节标题：{key}。"})

    if profile == "standard" and not re.search(r"\bFR[-_ ]?\d{1,4}\b", text, flags=re.I):
        errors.append({"code": "missing_requirement_ids", "message": "Standard PRD 缺少稳定的功能需求编号（如 FR-001）。"})

    if not re.search(r"\bAC[-_ ]?\d{1,4}\b|验收标准", text, flags=re.I):
        errors.append({"code": "missing_acceptance_ids", "message": "缺少验收标准或可识别的 AC 编号。"})

    vague_terms = sorted(set(re.findall(r"简单|快速|友好|灵活|智能|显著提升|体验更好", text)))
    if vague_terms:
        warnings.append({
            "code": "vague_language",
            "message": "发现可能不可验证的措辞：" + "、".join(vague_terms) + "；请补充观察方式或阈值。"
        })

    numeric_claim_lines = [
        line for line in text.splitlines()
        if re.search(r"(?:提升|降低|达到|不少于|不超过|至少|至多)[^。]{0,20}\d+(?:\.\d+)?%?", line)
        and not has_any(line, ["来源", "基线", "【假设】", "【建议】", "【待确认】", "示例"])
    ]
    if numeric_claim_lines:
        warnings.append({
            "code": "unqualified_numeric_claim",
            "message": f"有 {len(numeric_claim_lines)} 行目标数字未在同一行标出来源、基线或不确定性。"
        })

    if "【待确认】" in text and not has_any(text, SECTION_RULES["open_questions"]):
        warnings.append({"code": "scattered_tbd", "message": "存在待确认标记，但缺少集中管理的待确认项章节。"})

    return {
        "ok": not errors,
        "status": "ready_for_review" if not errors else "needs_revision",
        "profile": profile,
        "errors": errors,
        "warnings": warnings,
        "evidence_boundary": "structural_validation_only"
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a Markdown PRD against qiaomu-prd-writer structure rules.")
    parser.add_argument("file", help="Markdown PRD file to validate.")
    parser.add_argument("--profile", choices=["auto", "lean", "standard"], default="auto")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as a failing exit status.")
    parser.add_argument("--output", "-o", help="Optional JSON report path.")
    args = parser.parse_args()

    path = Path(args.file)
    result = validate(path.read_text(encoding="utf-8"), args.profile)
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    if not result["ok"] or (args.strict and result["warnings"]):
        raise SystemExit(2)


if __name__ == "__main__":
    main()
