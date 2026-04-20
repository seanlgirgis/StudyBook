#!/usr/bin/env python3
"""
Local Streamlit UI for editing coding_challenges/index.csv.

Focused UX:
- compact table view (id, title, primary, tags)
- pick one record
- edit in a popup dialog ("another window" feel)
"""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEX_PATH = ROOT / "index.csv"
DEFAULT_COLUMNS = [
    "id",
    "path",
    "primary",
    "tags",
    "title",
    "source",
    "difficulty",
    "status",
    "pattern",
    "data_structures",
    "my_impression",
    "key_nugget",
]
SUMMARY_COLUMNS = ["id", "title", "primary", "tags"]


def load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=DEFAULT_COLUMNS)
    df = pd.read_csv(path, dtype=str).fillna("")
    for col in DEFAULT_COLUMNS:
        if col not in df.columns:
            df[col] = ""
    return df


def save_csv(path: Path, df: pd.DataFrame) -> None:
    out = df.copy().fillna("")
    out = out.sort_values(by=["path", "id"], kind="stable").reset_index(drop=True)
    out.to_csv(path, index=False)


def open_local_path(target: Path) -> tuple[bool, str]:
    try:
        if not target.exists():
            return False, f"Path does not exist: {target}"
        os.startfile(str(target))  # type: ignore[attr-defined]
        return True, f"Opened: {target}"
    except Exception as exc:  # pragma: no cover
        return False, f"Failed to open path: {exc}"


def ensure_state(index_path: Path) -> None:
    if "index_df" not in st.session_state:
        st.session_state.index_df = load_csv(index_path)
    if "selected_id" not in st.session_state:
        st.session_state.selected_id = ""


def upsert_row(df: pd.DataFrame, row: dict[str, str]) -> pd.DataFrame:
    row_id = row["id"]
    existing_idx = df.index[df["id"] == row_id].tolist()
    if existing_idx:
        i = existing_idx[0]
        for k, v in row.items():
            df.at[i, k] = v
        return df
    return pd.concat([df, pd.DataFrame([row])], ignore_index=True)


def dialog_fields(columns: list[str], record: dict[str, str], disable_id: bool) -> dict[str, str]:
    values: dict[str, str] = {}
    preferred_order = DEFAULT_COLUMNS + [c for c in columns if c not in DEFAULT_COLUMNS]
    ordered_columns = [c for c in preferred_order if c in columns]
    for col in ordered_columns:
        values[col] = st.text_input(col, value=str(record.get(col, "")), disabled=(disable_id and col == "id"))
    return values


@st.dialog("Edit Record")
def edit_record_dialog(record: dict[str, str]) -> None:
    columns = list(st.session_state.index_df.columns)
    values = dialog_fields(columns, record, disable_id=True)
    row_id = values.get("id", "").strip()

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Apply Changes", type="primary"):
            updated = {k: v.strip() for k, v in values.items()}
            st.session_state.index_df = upsert_row(st.session_state.index_df, updated).fillna("")
            st.session_state.ui_message = f"Updated '{row_id}' (not saved to CSV yet)."
            st.rerun()
    with c2:
        if st.button("Cancel"):
            st.rerun()


@st.dialog("Add Record")
def add_record_dialog() -> None:
    columns = list(st.session_state.index_df.columns)
    defaults = {c: "" for c in columns}
    if "source" in defaults:
        defaults["source"] = "leetcode"
    values = dialog_fields(columns, defaults, disable_id=False)
    row_id = values.get("id", "").strip()

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Create", type="primary"):
            if not row_id:
                st.error("id is required.")
                return
            if (st.session_state.index_df["id"] == row_id).any():
                st.error(f"id '{row_id}' already exists.")
                return
            new_row = {k: v.strip() for k, v in values.items()}
            st.session_state.index_df = upsert_row(st.session_state.index_df, new_row).fillna("")
            st.session_state.selected_id = row_id
            st.session_state.ui_message = f"Added '{row_id}' (not saved to CSV yet)."
            st.rerun()
    with c2:
        if st.button("Cancel"):
            st.rerun()


def app() -> None:
    st.set_page_config(page_title="StudyBook Index Editor", layout="wide")
    st.title("StudyBook Index Editor")
    st.caption("Source of truth: coding_challenges/index.csv")

    index_path = DEFAULT_INDEX_PATH
    ensure_state(index_path)
    df: pd.DataFrame = st.session_state.index_df

    with st.sidebar:
        st.subheader("Data")
        st.code(str(index_path))
        if st.button("Reload From CSV", use_container_width=True):
            st.session_state.index_df = load_csv(index_path)
            st.session_state.ui_message = "Reloaded from disk."
            st.rerun()

        if st.button("Save CSV", use_container_width=True, type="primary"):
            save_csv(index_path, st.session_state.index_df)
            st.session_state.ui_message = f"Saved {len(st.session_state.index_df)} rows."
            st.rerun()

        csv_bytes = st.session_state.index_df.fillna("").to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Source CSV",
            data=csv_bytes,
            file_name="index.csv",
            mime="text/csv",
            use_container_width=True,
        )

    if st.session_state.get("ui_message"):
        st.success(st.session_state["ui_message"])
        st.session_state["ui_message"] = ""

    c1, c2 = st.columns([2, 1])
    with c1:
        needle = st.text_input("Search (id/title/primary/tags)")
    with c2:
        primary_options = ["All"] + sorted([p for p in df["primary"].astype(str).unique().tolist() if p])
        selected_primary = st.selectbox("Primary", primary_options, index=0)

    filtered = df.copy()
    if selected_primary != "All":
        filtered = filtered[filtered["primary"] == selected_primary]

    if needle.strip():
        q = needle.strip().lower()
        mask = (
            filtered["id"].astype(str).str.lower().str.contains(q, regex=False)
            | filtered["title"].astype(str).str.lower().str.contains(q, regex=False)
            | filtered["primary"].astype(str).str.lower().str.contains(q, regex=False)
            | filtered["tags"].astype(str).str.lower().str.contains(q, regex=False)
        )
        filtered = filtered[mask]

    st.caption(f"Showing {len(filtered)} of {len(df)} rows")
    summary = filtered[SUMMARY_COLUMNS].copy() if len(filtered) else pd.DataFrame(columns=SUMMARY_COLUMNS)
    summary = summary.reset_index(drop=True)
    filtered_ids = filtered["id"].astype(str).tolist()

    table_event = st.dataframe(
        summary,
        width="stretch",
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
    )

    selected_rows: list[int] = []
    try:
        selected_rows = list(getattr(table_event.selection, "rows", []))
    except Exception:
        selected_rows = []

    if selected_rows:
        row_idx = selected_rows[0]
        if 0 <= row_idx < len(filtered_ids):
            st.session_state.selected_id = filtered_ids[row_idx]
    elif st.session_state.selected_id not in filtered_ids:
        st.session_state.selected_id = filtered_ids[0] if filtered_ids else ""

    st.caption(f"Selected: {st.session_state.selected_id or '(none)'}")

    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("Edit Selected", type="primary", disabled=(st.session_state.selected_id == "")):
            row = df[df["id"] == st.session_state.selected_id].iloc[0].to_dict()
            edit_record_dialog(row)
    with b2:
        if st.button("Add New"):
            add_record_dialog()
    with b3:
        if st.button("Delete Selected", disabled=(st.session_state.selected_id == "")):
            st.session_state.index_df = st.session_state.index_df[
                st.session_state.index_df["id"] != st.session_state.selected_id
            ].reset_index(drop=True)
            st.session_state.ui_message = f"Deleted '{st.session_state.selected_id}' (not saved to CSV yet)."
            st.session_state.selected_id = ""
            st.rerun()

    if st.session_state.selected_id:
        row = df[df["id"] == st.session_state.selected_id]
        if not row.empty:
            rel = str(row.iloc[0].get("path", "")).strip()
            abs_path = ROOT / rel if rel else None
            st.code(str(abs_path) if abs_path else "(no path)")
            if st.button("Open Selected Path"):
                if abs_path is None:
                    st.error("No path set for selected record.")
                else:
                    ok, msg = open_local_path(abs_path)
                    if ok:
                        st.success(msg)
                    else:
                        st.error(msg)

    with st.expander("Underlying Source List (Raw index.csv rows)", expanded=False):
        st.caption("Direct view of all rows and columns from the in-memory index dataset.")
        st.dataframe(st.session_state.index_df, width="stretch", hide_index=True)


if __name__ == "__main__":
    app()
