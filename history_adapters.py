from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, Protocol

SUPPORTED_SCOPES = {"conversations", "files", "plans", "sessions", "memories", "all"}


class HistoryAdapter(Protocol):
    def search(self, scope: str, query: str, limit: int = 20) -> list[dict]: ...
    def inspect(self, session_id: str) -> dict | None: ...


def _text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, tuple, set)):
        return " ".join(_text(x) for x in value)
    if isinstance(value, dict):
        return " ".join(f"{k} {_text(v)}" for k, v in value.items())
    return str(value)


def normalize_session(raw: dict) -> dict:
    item = dict(raw)
    sid = item.get("session_id") or item.get("id") or item.get("chat_id")
    if not sid:
        raise ValueError("history session requires session_id/id/chat_id")
    item["session_id"] = str(sid)
    item.setdefault("chat_id", item["session_id"])
    item.setdefault("title", item.get("name") or item["chat_id"])
    item.setdefault("repositories", [])
    item.setdefault("paths", [])
    item.setdefault("files", [])
    item.setdefault("text", item.get("content") or "")
    stable = []
    for value in [item.get("project_id"), item.get("chat_id"), *item["repositories"], *item["paths"]]:
        if value and value not in stable:
            stable.append(value)
    item["stable_ids"] = stable
    return item


def _haystack(item: dict, scope: str) -> str:
    if scope == "files":
        return _text(item.get("files"))
    if scope == "plans":
        return _text(item.get("plans")) + " " + _text(item.get("text"))
    if scope == "memories":
        return _text(item.get("memories")) + " " + _text(item.get("files"))
    if scope == "sessions":
        return _text([item.get("session_id"), item.get("title"), item.get("project_id"), item.get("started_at")])
    if scope == "conversations":
        return _text([item.get("title"), item.get("text"), item.get("project_id"), item.get("chat_id")])
    return _text(item)


class InMemoryHistoryAdapter:
    def __init__(self, sessions: Iterable[dict]):
        self.sessions = [normalize_session(x) for x in sessions]

    def search(self, scope: str, query: str, limit: int = 20) -> list[dict]:
        if scope not in SUPPORTED_SCOPES:
            raise ValueError(f"unsupported history scope: {scope}")
        q = (query or "").casefold().strip()
        scored = []
        for index, item in enumerate(self.sessions):
            text = _haystack(item, scope).casefold()
            if q and q not in text:
                continue
            score = 0
            if q:
                if q == str(item.get("title", "")).casefold():
                    score += 100
                if q in str(item.get("title", "")).casefold():
                    score += 20
                if q in str(item.get("project_id", "")).casefold():
                    score += 10
                score += text.count(q)
            scored.append((score, index, dict(item)))
        scored.sort(key=lambda x: (-x[0], x[1]))
        return [item for _, _, item in scored[: max(0, limit)]]

    def inspect(self, session_id: str) -> dict | None:
        sid = str(session_id)
        for item in self.sessions:
            if item.get("session_id") == sid:
                return dict(item)
        return None


class JsonlHistoryAdapter:
    def __init__(self, path: Path | str):
        self.path = Path(path)

    def _iter(self):
        with self.path.open("r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                if not line.strip():
                    continue
                try:
                    yield normalize_session(json.loads(line))
                except (json.JSONDecodeError, ValueError) as exc:
                    raise ValueError(f"invalid history JSONL line {line_no}: {exc}") from exc

    def search(self, scope: str, query: str, limit: int = 20) -> list[dict]:
        return InMemoryHistoryAdapter(self._iter()).search(scope, query, limit)

    def inspect(self, session_id: str) -> dict | None:
        sid = str(session_id)
        for item in self._iter():
            if item.get("session_id") == sid:
                return item
        return None


def _extract_text(value: Any) -> list[str]:
    out: list[str] = []
    if value is None:
        return out
    if isinstance(value, str):
        if value.strip():
            out.append(value)
        return out
    if isinstance(value, (list, tuple)):
        for item in value:
            out.extend(_extract_text(item))
        return out
    if isinstance(value, dict):
        for key in ("text", "parts", "content"):
            if key in value:
                out.extend(_extract_text(value.get(key)))
        return out
    return out


def _extract_file_paths(value: Any) -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if key in {"file_path", "filepath", "path"} and isinstance(item, str) and item.strip():
                if item not in found:
                    found.append(item)
            else:
                for nested in _extract_file_paths(item):
                    if nested not in found:
                        found.append(nested)
    elif isinstance(value, (list, tuple)):
        for item in value:
            for nested in _extract_file_paths(item):
                if nested not in found:
                    found.append(nested)
    elif isinstance(value, str):
        try:
            parsed = json.loads(value)
        except Exception:
            parsed = None
        if parsed is not None:
            found.extend(_extract_file_paths(parsed))
    return found


def _first_user_text(rows: list[dict]) -> str:
    for row in rows:
        message = row.get("message") if isinstance(row, dict) else None
        if isinstance(message, dict) and message.get("role") == "user":
            parts = _extract_text(message.get("content"))
            if parts:
                return parts[0][:120]
        payload = row.get("payload") if isinstance(row, dict) else None
        if isinstance(payload, dict) and payload.get("role") == "user":
            parts = _extract_text(payload.get("content"))
            if parts:
                return parts[0][:120]
    return ""


class _FilesystemJsonlAdapter:
    provider = "unknown"

    def __init__(self, root: Path | str):
        self.root = Path(root).expanduser()

    def _files(self) -> list[Path]:
        if self.root.is_file():
            return [self.root]
        if not self.root.exists():
            return []
        return sorted(p for p in self.root.rglob("*.jsonl") if p.is_file())

    def _parse_file(self, path: Path) -> dict | None:
        raise NotImplementedError

    def _sessions(self) -> list[dict]:
        sessions: list[dict] = []
        for path in self._files():
            item = self._parse_file(path)
            if item is not None:
                sessions.append(normalize_session(item))
        return sessions

    def search(self, scope: str, query: str, limit: int = 20) -> list[dict]:
        return InMemoryHistoryAdapter(self._sessions()).search(scope, query, limit)

    def inspect(self, session_id: str) -> dict | None:
        sid = str(session_id)
        for item in self._sessions():
            if item.get("session_id") == sid:
                return item
        return None


class ClaudeCodeHistoryAdapter(_FilesystemJsonlAdapter):
    provider = "claude-code"

    def _parse_file(self, path: Path) -> dict | None:
        rows: list[dict] = []
        with path.open("r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                if not line.strip():
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"invalid Claude Code JSONL {path}:{line_no}: {exc}") from exc
                if isinstance(obj, dict):
                    rows.append(obj)
        if not rows:
            return None
        sid = next((r.get("sessionId") for r in rows if r.get("sessionId")), None) or path.stem
        paths: list[str] = []
        files: list[str] = []
        text: list[str] = []
        started_at = None
        for row in rows:
            cwd = row.get("cwd")
            if isinstance(cwd, str) and cwd and cwd not in paths:
                paths.append(cwd)
            if started_at is None and row.get("timestamp"):
                started_at = row.get("timestamp")
            message = row.get("message")
            if isinstance(message, dict):
                text.extend(_extract_text(message.get("content")))
                for fp in _extract_file_paths(message.get("content")):
                    if fp not in files:
                        files.append(fp)
            for fp in _extract_file_paths(row.get("toolUseResult")):
                if fp not in files:
                    files.append(fp)
        return {"session_id": str(sid), "chat_id": str(sid), "title": _first_user_text(rows) or path.stem, "provider": self.provider, "source_locator": str(path), "started_at": started_at, "text": "\n".join(text), "repositories": [], "paths": paths, "files": files}


class CodexHistoryAdapter(_FilesystemJsonlAdapter):
    provider = "codex"

    def _parse_file(self, path: Path) -> dict | None:
        rows: list[dict] = []
        with path.open("r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                if not line.strip():
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"invalid Codex JSONL {path}:{line_no}: {exc}") from exc
                if isinstance(obj, dict):
                    rows.append(obj)
        if not rows:
            return None
        meta = next((r.get("payload") for r in rows if r.get("type") == "session_meta" and isinstance(r.get("payload"), dict)), {})
        sid = meta.get("id") or meta.get("session_id") or path.stem
        cwd = meta.get("cwd")
        git = meta.get("git") if isinstance(meta.get("git"), dict) else {}
        repo = git.get("repository_url") or git.get("repo_url")
        text: list[str] = []
        files: list[str] = []
        started_at = next((r.get("timestamp") for r in rows if r.get("timestamp")), None)
        for row in rows:
            payload = row.get("payload")
            if not isinstance(payload, dict):
                continue
            if payload.get("type") == "message" or payload.get("role") in {"user", "assistant", "system"}:
                text.extend(_extract_text(payload.get("content")))
            if payload.get("type") in {"function_call", "tool_call"}:
                args = payload.get("arguments") or payload.get("input")
                for fp in _extract_file_paths(args):
                    if fp not in files:
                        files.append(fp)
        return {"session_id": str(sid), "chat_id": str(sid), "title": _first_user_text(rows) or path.stem, "provider": self.provider, "source_locator": str(path), "started_at": started_at, "text": "\n".join(text), "repositories": [repo] if isinstance(repo, str) and repo else [], "paths": [cwd] if isinstance(cwd, str) and cwd else [], "files": files, "git_branch": git.get("branch"), "git_sha": git.get("commit_hash") or git.get("sha")}


class ChatGPTExportHistoryAdapter:
    def __init__(self, conversations_json: Path | str):
        self.path = Path(conversations_json).expanduser()

    def _sessions(self) -> list[dict]:
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid ChatGPT export JSON {self.path}: {exc}") from exc
        if not isinstance(data, list):
            raise ValueError("ChatGPT conversations export must be a JSON list")
        sessions: list[dict] = []
        for conv in data:
            if not isinstance(conv, dict):
                continue
            sid = conv.get("conversation_id") or conv.get("id")
            if not sid:
                continue
            mapping = conv.get("mapping") if isinstance(conv.get("mapping"), dict) else {}
            messages: list[tuple[float, str]] = []
            files: list[str] = []
            for node in mapping.values():
                if not isinstance(node, dict):
                    continue
                message = node.get("message")
                if not isinstance(message, dict):
                    continue
                content = message.get("content")
                parts = _extract_text(content)
                ts = message.get("create_time")
                try:
                    order = float(ts) if ts is not None else 0.0
                except (TypeError, ValueError):
                    order = 0.0
                for part in parts:
                    messages.append((order, part))
                for fp in _extract_file_paths(content):
                    if fp not in files:
                        files.append(fp)
            messages.sort(key=lambda x: x[0])
            item = {"session_id": str(sid), "chat_id": str(sid), "title": conv.get("title") or str(sid), "provider": "chatgpt-export", "source_locator": str(self.path), "started_at": conv.get("create_time"), "text": "\n".join(text for _, text in messages), "repositories": [], "paths": [], "files": files}
            sessions.append(normalize_session(item))
        return sessions

    def search(self, scope: str, query: str, limit: int = 20) -> list[dict]:
        return InMemoryHistoryAdapter(self._sessions()).search(scope, query, limit)

    def inspect(self, session_id: str) -> dict | None:
        sid = str(session_id)
        for item in self._sessions():
            if item.get("session_id") == sid:
                return item
        return None


class CompositeHistoryAdapter:
    def __init__(self, adapters: Iterable[HistoryAdapter]):
        self.adapters = list(adapters)

    def search(self, scope: str, query: str, limit: int = 20) -> list[dict]:
        merged: list[dict] = []
        seen: set[str] = set()
        for adapter in self.adapters:
            for item in adapter.search(scope, query, limit=limit):
                key = str(item.get("session_id") or item.get("chat_id"))
                if key in seen:
                    continue
                seen.add(key)
                merged.append(item)
                if len(merged) >= limit:
                    return merged
        return merged

    def inspect(self, session_id: str) -> dict | None:
        for adapter in self.adapters:
            item = adapter.inspect(session_id)
            if item is not None:
                return item
        return None
