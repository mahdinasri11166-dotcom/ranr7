# -*- coding: utf-8 -*-
"""Explicit refusals for dangerous capabilities."""
from __future__ import annotations

from typing import Any


def refuse_bruteforce(**kwargs) -> dict[str, Any]:
    return {
        "ok": False,
        "blocked": True,
        "error": "brute-force و حدس رمز عبور / credential stuffing در این محصول پیاده‌سازی و مجاز نیست.",
        "policy": "security_policy_v1",
        "allowed_alternative": "از osint_username_parallel فقط برای بررسی حضور عمومی پروفایل استفاده کنید.",
    }


def refuse_aggressive_vuln_scan(**kwargs) -> dict[str, Any]:
    return {
        "ok": False,
        "blocked": True,
        "error": "اسکنر آسیب‌پذیری تهاجمی (exploit، اسکن پورت تهاجمی، fuzz فعال) عمداً اضافه نشده است.",
        "policy": "security_policy_v1",
        "allowed_alternative": (
            "ابزارهای غیرفعال: osint_domain، osint_domain_graph، osint_crtsh، "
            "osint_email_dns (MX/SPF/DMARC)، browser_read، osint_file_metadata"
        ),
    }
