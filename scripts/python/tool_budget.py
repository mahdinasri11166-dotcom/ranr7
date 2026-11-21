# -*- coding: utf-8 -*-
"""Limit tool calls per chat turn."""
from __future__ import annotations
import time
from typing import Any

_state: dict[str, Any] = {"count": 0, "window_start": 0.0, "max_per_window": 8, "window_sec": 120.0}

def reset_turn() -> None:
    _state["count"] = 0
    _state["window_start"] = time.time()

def allow_tool() -> tuple[bool, str]:
    now = time.time()
    if now - float(_state["window_start"]) > float(_state["window_sec"]):
        _state["count"] = 0
        _state["window_start"] = now
    if int(_state["count"]) >= int(_state["max_per_window"]):
        return False, f"سقف ابزار در این بازه ({_state['max_per_window']}) پر شد"
    _state["count"] = int(_state["count"]) + 1
    return True, ""
