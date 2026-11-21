# -*- coding: utf-8 -*-
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
ok = fail = 0

def check(name, cond, detail=""):
    global ok, fail
    if cond:
        ok += 1
        print(f"  [OK]  {name}")
    else:
        fail += 1
        print(f"  [FAIL] {name}  {detail}")

def main():
    print("=== GGUF selftest v2.6 ===")
    mods = [
        "desktop_chat", "app_hub", "engine", "model_meta", "audit_log", "session_memory", "backup_tools", "update_check", "model_router", "load_advisor", "tool_budget", "app_logging", "agent_tools", "osint_tools", "osint_advanced",
        "report_engine", "plugin_system", "browser_readonly", "rag_local",
        "doctor", "policy_guards", "case_manager", "session_store", "ingest_books", "openai_api_server", "first_run_wizard", "elevated_tools", "builder_tools", "system_named_tools", "agent_memory", "browser_tools", "coding_tools",
    ]
    for m in mods:
        check(m, (ROOT / "scripts/python" / f"{m}.py").exists())
    from agent_tools import TOOLS, execute_tool
    check("tools>=30", len(TOOLS) >= 30, str(len(TOOLS)))
    check("session_list tool", "session_list" in TOOLS)
    check("session_export_md", "session_export_md" in TOOLS)
    check("case_create", "case_create" in TOOLS)
    r = execute_tool("session_list", {})
    check("session_list runs", r.get("ok") is True)
    r2 = execute_tool("case_list", {})
    check("case_list runs", r2.get("ok") is True)
    r3 = execute_tool("bruteforce", {})
    check("bruteforce blocked", r3.get("blocked") is True)
    r4 = execute_tool("list_dir", {"path": "../.."})
    check("path escape blocked", r4.get("ok") is False)
    from report_engine import render_graph_svg
    svg = render_graph_svg({"nodes":[{"id":"a","type":"apex"}], "edges":[]})
    check("graph svg", "<svg" in svg)
    import openai_api_server
    check("openai api port", openai_api_server.PORT == 8787)
    r5 = execute_tool("sys_run_cmd", {"command": "echo test"})
    check("elevated off blocks cmd", r5.get("blocked") is True or r5.get("ok") is False)
    check("sys_run_cmd registered", "sys_run_cmd" in TOOLS)
    check("build_scaffold registered", "build_scaffold" in TOOLS)
    r6 = execute_tool("build_list_templates", {})
    check("templates list", r6.get("ok") is True)
    check("search_code registered", "search_code" in TOOLS)
    check("large_files_scan registered", "large_files_scan" in TOOLS)
    check("model_inspect registered", "model_inspect" in TOOLS)
    check("audit_list registered", "audit_list" in TOOLS)
    check("load_advise registered", "load_advise" in TOOLS)
    check("session_restore_last registered", "session_restore_last" in TOOLS)
    check("git_ensure_gitignore registered", "git_ensure_gitignore" in TOOLS)
    check("todo_plan registered", "todo_plan" in TOOLS)
    check("process_list registered", "process_list" in TOOLS)
    check("browser_fetch registered", "browser_fetch" in TOOLS)
    r7 = execute_tool("todo_plan", {"tasks": ["a", "b"]})
    check("todo_plan works", r7.get("ok") is True)
    r8 = execute_tool("search_code", {"query": "def ", "path": "."})
    check("search_code works", r8.get("ok") is True)
    r9 = execute_tool("process_list", {})
    check("process_list needs elevated", r9.get("blocked") is True or r9.get("ok") is False)

    print(f"\nResult: {ok} ok, {fail} fail")
    return 0 if fail == 0 else 1

if __name__ == "__main__":
    sys.exit(main())

# extra checks appended safely only if run as script - skip if duplicate
