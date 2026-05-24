from __future__ import annotations

import json
import hashlib
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


DEFAULT_TEMPLATE_ID = "quick_note"
DEFAULT_TEMPLATE_VERSION = "1.0"
DEFAULT_FOLDER_TEMPLATE_ID = "note_folder"
DEFAULT_FOLDER_TEMPLATE_VERSION = "1.0"


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _now_iso() -> str:
    return _now_utc().replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _ts_for_name(dt: datetime | None = None) -> str:
    d = dt or _now_utc()
    return d.strftime("%Y%m%d_%H%M%S")


def _slugify(text: str, max_len: int = 40) -> str:
    s = text.lower()
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    if not s:
        s = "note"
    return s[:max_len].strip("_") or "note"


def _safe_filename(base: str) -> str:
    # Windows-illegal characters and trailing dots/spaces protections.
    bad = r'[<>:"/\\|?*\x00-\x1F]'
    cleaned = re.sub(bad, "_", base).strip(" .")
    return cleaned or "note"


def _split_tags(tags: str | None) -> List[str]:
    if not tags:
        return []
    out: List[str] = []
    for t in tags.split(","):
        tt = t.strip()
        if tt and tt not in out:
            out.append(tt)
    return out


def generate_note_filename(title: str, now: datetime | None = None, suffix: str | None = None) -> str:
    ts = _ts_for_name(now)
    slug = _slugify(title)
    base = _safe_filename(f"note_{ts}_{slug}")
    if suffix:
        base = _safe_filename(f"{base}_{suffix}")
    return f"{base}.md"


def _select_unique_path(root: Path, filename: str) -> Path:
    candidate = root / filename
    if not candidate.exists():
        return candidate
    stem = candidate.stem
    for i in range(1, 1000):
        p = root / f"{stem}_{i:03d}.md"
        if not p.exists():
            return p
    raise RuntimeError("Unable to find non-colliding note filename")


def _select_unique_dir(root: Path, dirname: str) -> Path:
    candidate = root / dirname
    if not candidate.exists():
        return candidate
    for i in range(1, 1000):
        p = root / f"{dirname}_{i:03d}"
        if not p.exists():
            return p
    raise RuntimeError("Unable to find non-colliding note folder name")


def _render_frontmatter(meta: Dict[str, Any]) -> str:
    lines = ["---"]
    for key in [
        "title",
        "vault_item_type",
        "template_id",
        "template_version",
        "lifecycle_status",
        "sensitivity_level",
        "retention_policy_id",
        "tags",
        "story",
        "created_at",
    ]:
        val = meta.get(key)
        if key == "tags":
            rendered = "[" + ", ".join(val or []) + "]"
        else:
            rendered = "" if val is None else str(val)
        lines.append(f"{key}: {rendered}")
    lines.append("---")
    return "\n".join(lines)


def _render_frontmatter_pairs(pairs: List[tuple[str, Any]]) -> str:
    lines = ["---"]
    for key, val in pairs:
        if key == "tags":
            rendered = "[" + ", ".join(val or []) + "]"
        else:
            rendered = "" if val is None else str(val)
        lines.append(f"{key}: {rendered}")
    lines.append("---")
    return "\n".join(lines)


def create_note(
    title: str,
    story: str | None,
    tags: str | None,
    body: str,
    notes_root: str | Path,
    note_folder_path: str | Path | None = None,
    requested_filename: str | None = None,
) -> Dict[str, Any]:
    root = Path(notes_root)
    root.mkdir(parents=True, exist_ok=True)
    write_root = root
    if note_folder_path:
        folder_path = Path(note_folder_path)
        notes_dir = folder_path / "notes"
        if not notes_dir.exists():
            raise FileNotFoundError(f"note folder notes path does not exist: {notes_dir}")
        write_root = notes_dir
    meta = {
        "title": title,
        "vault_item_type": "note",
        "template_id": DEFAULT_TEMPLATE_ID,
        "template_version": DEFAULT_TEMPLATE_VERSION,
        "lifecycle_status": "hot",
        "sensitivity_level": "normal",
        "retention_policy_id": "default_lifetime_user_use",
        "tags": _split_tags(tags),
        "story": story or "",
        "created_at": _now_iso(),
    }

    if requested_filename:
        fn = _safe_filename(requested_filename)
        if not fn.lower().endswith(".md"):
            fn = f"{fn}.md"
        note_path = _select_unique_path(write_root, fn)
    else:
        fn = generate_note_filename(title)
        note_path = _select_unique_path(write_root, fn)
    content = _render_frontmatter(meta) + "\n\n" + (body or "") + "\n"
    note_path.write_text(content, encoding="utf-8")
    return {
        "note_path": str(note_path),
        "title": title,
        "filename": note_path.name,
        "lifecycle_status": meta["lifecycle_status"],
        "sensitivity_level": meta["sensitivity_level"],
    }


def create_note_folder(
    title: str,
    story: str | None,
    tags: str | None,
    notes_root: str | Path,
) -> Dict[str, Any]:
    root = Path(notes_root)
    root.mkdir(parents=True, exist_ok=True)
    created_at = _now_iso()
    dirname = _safe_filename(f"note_folder_{_ts_for_name()}_{_slugify(title)}")
    folder_path = _select_unique_dir(root, dirname)
    notes_dir = folder_path / "notes"
    reports_dir = folder_path
    notes_dir.mkdir(parents=True, exist_ok=False)

    folder_meta = {
        "schema_version": "1.0",
        "folder_id": folder_path.name,
        "title": title,
        "vault_item_type": "note_folder",
        "template_id": DEFAULT_FOLDER_TEMPLATE_ID,
        "template_version": DEFAULT_FOLDER_TEMPLATE_VERSION,
        "lifecycle_status": "hot",
        "sensitivity_level": "normal",
        "retention_policy_id": "default_lifetime_user_use",
        "tags": _split_tags(tags),
        "story": story or "",
        "created_at": created_at,
    }
    (reports_dir / "_folder_manifest.json").write_text(
        json.dumps(folder_meta, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    readme_frontmatter = _render_frontmatter(
        {
            "title": title,
            "vault_item_type": "note_folder",
            "template_id": DEFAULT_FOLDER_TEMPLATE_ID,
            "template_version": DEFAULT_FOLDER_TEMPLATE_VERSION,
            "lifecycle_status": "hot",
            "sensitivity_level": "normal",
            "retention_policy_id": "default_lifetime_user_use",
            "tags": _split_tags(tags),
            "story": story or "",
            "created_at": created_at,
        }
    )
    readme_body = "\n\n# Note Folder\n\nManaged LifeVault note folder.\n"
    (reports_dir / "README.md").write_text(readme_frontmatter + readme_body, encoding="utf-8")
    return {
        "folder_title": title,
        "folder_path": str(folder_path),
        "folder_name": folder_path.name,
        "tags": _split_tags(tags),
        "story": story or "",
    }


def create_sensitive_note_phase0(
    title: str,
    public_hint: str,
    story: str | None,
    tags: str | None,
    demo_protected_body: str,
    notes_root: str | Path,
) -> Dict[str, Any]:
    root = Path(notes_root)
    root.mkdir(parents=True, exist_ok=True)
    created_at = _now_iso()
    folder_name = _safe_filename(f"sensitive_note_{_ts_for_name()}_{_slugify(title)}")
    folder_path = _select_unique_dir(root, folder_name)
    protected_dir = folder_path / "protected"
    protected_dir.mkdir(parents=True, exist_ok=False)

    placeholder_token = hashlib.sha256(demo_protected_body.encode("utf-8")).hexdigest()
    placeholder = f"PHASE0_PLACEHOLDER_NOT_ENCRYPTION:{placeholder_token}"
    lvenc_path = protected_dir / "encrypted_body.lvenc"
    lvenc_path.write_text(placeholder + "\n", encoding="utf-8")

    manifest = {
        "encrypted_body_id": f"enc_{_ts_for_name()}_{_slugify(title, max_len=16)}",
        "version": "1.0",
        "created_at": created_at,
        "ciphertext_sha256": hashlib.sha256(placeholder.encode("utf-8")).hexdigest(),
        "size_bytes": len(placeholder.encode("utf-8")),
        "phase": "phase0_placeholder",
    }
    (protected_dir / "encrypted_body_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )

    note_md = _render_frontmatter_pairs(
        [
            ("title", title),
            ("vault_item_type", "note"),
            ("sensitivity_level", "sensitive"),
            ("public_hint", public_hint),
            ("tags", _split_tags(tags)),
            ("story", story or ""),
            ("lifecycle_status", "hot"),
            ("retention_policy_id", "default_lifetime_user_use"),
            ("encrypted_body_ref", "protected/encrypted_body.lvenc"),
            ("created_at", created_at),
        ]
    ) + "\n\n# Sensitive Note (Phase 0)\n\nProtected payload placeholder is stored under `protected/`.\n"
    (folder_path / "note.md").write_text(note_md, encoding="utf-8")
    return {
        "sensitive_note_path": str(folder_path),
        "note_path": str(folder_path / "note.md"),
        "title": title,
        "public_hint": public_hint,
        "sensitivity_level": "sensitive",
        "phase": "phase0_placeholder_not_encryption",
    }


def _parse_note(path: Path) -> Dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    meta: Dict[str, Any] = {}
    body = text
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            fm = text[4:end].splitlines()
            body = text[end + 5 :]
            for line in fm:
                if ":" not in line:
                    continue
                k, v = line.split(":", 1)
                k = k.strip()
                v = v.strip()
                if k == "tags":
                    if v.startswith("[") and v.endswith("]"):
                        tags = [t.strip() for t in v[1:-1].split(",") if t.strip()]
                    else:
                        tags = [t.strip() for t in v.split(",") if t.strip()]
                    meta[k] = tags
                else:
                    meta[k] = v
    return {"path": str(path), "meta": meta, "body": body}


def search_notes(notes_root: str | Path, query: str) -> List[Dict[str, Any]]:
    q = (query or "").strip().lower()
    root = Path(notes_root)
    if not root.exists():
        return []
    results: List[Dict[str, Any]] = []
    for path in root.rglob("*.md"):
        n = _parse_note(path)
        m = n["meta"]
        title = (m.get("title") or "").lower()
        story = (m.get("story") or "").lower()
        public_hint = (m.get("public_hint") or "").lower()
        tags = [t.lower() for t in m.get("tags", [])]
        body = (n.get("body") or "").lower()

        match_types: List[str] = []
        if q in title:
            match_types.append("title")
        if q in story:
            match_types.append("story")
        if any(q in t for t in tags):
            match_types.append("tag")
        if q in public_hint:
            match_types.append("public_hint")
        if q in body:
            match_types.append("body")
        if match_types:
            parent_note_folder = ""
            if path.parent.name == "notes":
                candidate = path.parent.parent
                if (candidate / "_folder_manifest.json").exists():
                    parent_note_folder = str(candidate)
            results.append(
                {
                    "title": m.get("title", path.stem),
                    "path": str(path),
                    "tags": m.get("tags", []),
                    "story": m.get("story", ""),
                    "match_type": ",".join(match_types),
                    "parent_note_folder": parent_note_folder,
                    "sensitivity_level": m.get("sensitivity_level", "normal"),
                    "unlock_required": (m.get("sensitivity_level", "normal") == "sensitive"),
                }
            )
    return results


def list_note_folders(notes_root: str | Path) -> List[Dict[str, Any]]:
    root = Path(notes_root)
    if not root.exists():
        return []
    rows: List[Dict[str, Any]] = []
    for manifest in root.rglob("_folder_manifest.json"):
        folder = manifest.parent
        readme = folder / "README.md"
        if not readme.exists():
            continue
        parsed = _parse_note(readme)
        meta = parsed["meta"]
        note_count = len(list((folder / "notes").rglob("*.md"))) if (folder / "notes").exists() else 0
        rows.append(
            {
                "folder_title": meta.get("title", folder.name),
                "folder_path": str(folder),
                "tags": meta.get("tags", []),
                "story": meta.get("story", ""),
                "note_count": note_count,
            }
        )
    return rows
