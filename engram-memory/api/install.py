"""Serves install scripts with the correct content type for each platform."""

from __future__ import annotations

from pathlib import Path

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Route

_ROOT = Path(__file__).parent.parent

_SCRIPTS = {
    "install.sh": _ROOT / "install.sh",
    "install.ps1": _ROOT / "install.ps1",
    "install.cmd": _ROOT / "install.cmd",
}


async def serve_install(request: Request) -> PlainTextResponse:
    path = request.path_params.get("path", "")
    # Map /install.ps1 → install.ps1, /install.cmd → install.cmd, else → install.sh
    if path.endswith(".ps1"):
        script = _SCRIPTS["install.ps1"]
    elif path.endswith(".cmd"):
        script = _SCRIPTS["install.cmd"]
    else:
        script = _SCRIPTS["install.sh"]

    if script.exists():
        content = script.read_text()
    else:
        content = "#!/bin/sh\necho 'Install script not found.'\n"
    return PlainTextResponse(content, headers={"Content-Type": "text/plain; charset=utf-8"})


app = Starlette(routes=[Route("/{path:path}", serve_install, methods=["GET"])])
