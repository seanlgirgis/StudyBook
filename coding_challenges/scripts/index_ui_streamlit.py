#!/usr/bin/env python3
"""
Local Streamlit UI for editing coding_challenges/index.csv.
"""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEX_PATH = ROOT / "index.csv"
DEFAULT_COLUMNS = ["id", "path", "primary", "tags", "title", "source"]


def load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=DEFAULT_COLUMNS)
    df = pd.read_csv(path, dtype=str).fillna("")
    for col in DEFAULT_COLUMNS:
        if col not in df.columns:
            df[col] = ""
    return df


def save_csv(path: Path, df: pd.DataFrame) -> None:
    out = df.copy()
    out = out.fillna("")
    out = out.sort_values(by=["path", "id"], kind="stable")
    out.to_csv(path, index=False)


def open_local_path(target: Path) -> tuple[bool, str]:
    try:
        if not target.exists():
            return False, f"Path does not exist: {target}"
        os.startfile(str(target))  # type: ignore[attr-defined]
        return True, f"Opened: {target}"
    except Exception as exc:  # pragma: no cover
        return False, f"Failed to open path: {exc}"


def ensure_session_df(index_path: Path) -> None:
    if "index_df" not in st.session_state:
        st.session_state.index_df = load_csv(index_path)


def app() -> None:
    st.set_page_config(page_title="StudyBook Index Editor", layout="wide")
    st.title("StudyBook Index Editor")
    st.caption("CSV source of truth: coding_challenges/index.csv")

    index_path = DEFAULT_INDEX_PATH
    ensure_session_df(index_path)
    df: pd.DataFrame = st.session_state.index_df

    with st.sidebar:
        st.subheader("Actions")
        if st.button("Reload From CSV", use_container_width=True):
            st.session_state.index_df = load_csv(index_path)
            st.success("Reloaded from disk.")
            st.rerun()

        if st.button("Save CSV", use_container_width=True, type="primary"):
            save_csv(index_path, st.session_state.index_df)
            st.success(f"Saved {len(st.session_state.index_df)} rows to {index_path}")

        st.divider()
        st.subheader("Open Record Path")
        row_ids = st.session_state.index_df["id"].astype(str).tolist() if "id" in st.session_state.index_df.columns else []
        selected_open_id = st.selectbox("Select id", [""] + row_ids, index=0)
        if st.button("Open Path", use_container_width=True, disabled=(selected_open_id == "")):
            row = st.session_state.index_df[st.session_state.index_df["id"] == selected_open_id]
            if row.empty:
                st.error(f"id '{selected_open_id}' not found")
            else:
                rel = str(row.iloc[0].get("path", "")).strip()
                target = ROOT / rel
                ok, msg = open_local_path(target)
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)

    st.subheader("Search")
    col1, col2 = st.columns([2, 1])
    with col1:
        needle = st.text_input("Contains text")
    with col2:
        fields = st.multiselect("Fields", options=list(df.columns), default=list(df.columns))

    filtered = df
    if needle.strip():
        q = needle.strip().lower()
        search_cols = fields if fields else list(df.columns)
        if search_cols:
            mask = pd.Series(False, index=df.index)
            for c in search_cols:
                mask = mask | df[c].astype(str).str.lower().str.contains(q, regex=False)
            filtered = df[mask]

    st.caption(f"Showing {len(filtered)} / {len(df)} rows")
    st.dataframe(filtered, use_container_width=True, hide_index=True)

    st.subheader("Edit Table")
    edited = st.data_editor(
        st.session_state.index_df,
        use_container_width=True,
        num_rows="dynamic",
        hide_index=True,
        key="index_editor_grid",
    )
    st.session_state.index_df = edited.fillna("")

    st.subheader("Delete Row")
    delete_id = st.selectbox("Delete by id", [""] + st.session_state.index_df["id"].astype(str).tolist(), index=0)
    if st.button("Delete Selected id", disabled=(delete_id == "")):
        st.session_state.index_df = st.session_state.index_df[st.session_state.index_df["id"] != delete_id].reset_index(drop=True)
        st.success(f"Deleted id '{delete_id}' (not saved yet).")
        st.rerun()


if __name__ == "__main__":
    app()
