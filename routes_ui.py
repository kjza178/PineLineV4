"""Trang UI chính thức V4: /, /ui3, /hongguo.

UI duy nhất: index3.html. (index.html đã archive → scripts/archive/ui_legacy/)
"""
from __future__ import annotations

from pathlib import Path
from fastapi.responses import HTMLResponse
from fastapi import APIRouter

router = APIRouter()

__all__ = [
    "_html_file",
    "find_index",
    "index",
    "ui3",
    "ui4",
    "ui_hongguo",
    "router",
]


def find_index() -> Path | None:
    """UI chính: index3.html cạnh server."""
    here = Path(__file__).parent
    for p in (here / "index3.html", Path("index3.html")):
        if p.exists():
            return p
    return None


@router.get("/", response_class=HTMLResponse)
def index():
    p = find_index()
    if not p:
        return HTMLResponse(
            "<h2>Không tìm thấy index3.html</h2>"
            "<p>Đặt file cạnh server.py.</p>",
            status_code=500,
        )
    return HTMLResponse(p.read_text(encoding="utf-8"))


@router.get("/ui3", response_class=HTMLResponse)
@router.get("/index3.html", response_class=HTMLResponse)
def ui3():
    return index()


@router.get("/ui4", response_class=HTMLResponse)
@router.get("/index4.html", response_class=HTMLResponse)
def ui4():
    # Alias lịch sử → UI chính
    return index()


def _html_file(name: str) -> HTMLResponse:
    here = Path(__file__).parent
    for p in (here / name, Path(name)):
        if p.exists():
            return HTMLResponse(p.read_text(encoding="utf-8"))
    return HTMLResponse(f"<h2>Không tìm thấy {name}</h2>", status_code=404)


@router.get("/hongguo", response_class=HTMLResponse)
@router.get("/ui-hg", response_class=HTMLResponse)
def ui_hongguo():
    return _html_file("hongguo.html")


@router.get("/workflow", response_class=HTMLResponse)
def ui_workflow():
    return _html_file("workflow.html")
