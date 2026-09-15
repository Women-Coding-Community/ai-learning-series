"""LinkedIn MCP server (FastMCP, stdio).

Tools:
    get_profile()                      -> member id/name via OpenID userinfo
    create_post(text, image_path=None) -> publish a post via the LinkedIn Posts API

Env:
    LINKEDIN_ACCESS_TOKEN  3-legged OAuth token (scopes: openid profile w_member_social)
    DRY_RUN                "true" (default): log the payload, return a fake URL, post nothing.

See README.md in this directory for the LinkedIn Developer app setup.
"""

# /// script
# dependencies = [
#     "fastmcp>=2.0",
#     "httpx>=0.27",
# ]
# ///

import logging
import os
import sys
import time
import uuid

import httpx
from fastmcp import FastMCP

API_BASE = "https://api.linkedin.com"
LINKEDIN_VERSION = "202506"  # Posts API versioned header, YYYYMM

logging.basicConfig(stream=sys.stderr, level=logging.INFO, format="[linkedin-mcp] %(message)s")
log = logging.getLogger(__name__)

mcp = FastMCP("linkedin")


def _dry_run() -> bool:
    return os.environ.get("DRY_RUN", "true").lower() != "false"


def _headers() -> dict:
    token = os.environ.get("LINKEDIN_ACCESS_TOKEN", "")
    return {
        "Authorization": f"Bearer {token}",
        "LinkedIn-Version": LINKEDIN_VERSION,
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json",
    }


def _userinfo() -> dict:
    resp = httpx.get(f"{API_BASE}/v2/userinfo", headers=_headers(), timeout=30)
    resp.raise_for_status()
    return resp.json()


@mcp.tool
def get_profile() -> dict:
    """Returns the authenticated LinkedIn member's profile (id, name)."""
    if _dry_run():
        log.info("DRY_RUN get_profile")
        return {"status": "success", "sub": "dry-run-member-id", "name": "Dry Run User"}
    info = _userinfo()
    return {"status": "success", "sub": info["sub"], "name": info.get("name", "")}


def _upload_image(author_urn: str, image_path: str) -> str:
    """Registers and uploads a local image, returns the image URN."""
    init = httpx.post(
        f"{API_BASE}/rest/images?action=initializeUpload",
        headers=_headers(),
        json={"initializeUploadRequest": {"owner": author_urn}},
        timeout=30,
    )
    init.raise_for_status()
    value = init.json()["value"]
    with open(image_path, "rb") as f:
        up = httpx.put(
            value["uploadUrl"],
            content=f.read(),
            headers={"Authorization": _headers()["Authorization"]},
            timeout=60,
        )
    up.raise_for_status()
    return value["image"]


@mcp.tool
def create_post(text: str, image_path: str | None = None) -> dict:
    """Publishes a post to the authenticated member's LinkedIn feed.

    Args:
        text: The full post text.
        image_path: Optional absolute path to a local image to attach.
    """
    if _dry_run():
        fake_urn = f"urn:li:share:dryrun-{uuid.uuid4().hex[:12]}"
        log.info("DRY_RUN create_post payload: text=%r image_path=%r", text, image_path)
        return {
            "status": "success",
            "dry_run": True,
            "post_url": f"https://www.linkedin.com/feed/update/{fake_urn}/",
            "note": "DRY_RUN=true, nothing was posted.",
        }

    author_urn = f"urn:li:person:{_userinfo()['sub']}"
    payload = {
        "author": author_urn,
        "commentary": text,
        "visibility": "PUBLIC",
        "distribution": {"feedDistribution": "MAIN_FEED", "targetEntities": [], "thirdPartyDistributionChannels": []},
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }
    if image_path:
        image_urn = _upload_image(author_urn, image_path)
        payload["content"] = {"media": {"id": image_urn, "altText": "Post illustration"}}

    resp = httpx.post(f"{API_BASE}/rest/posts", headers=_headers(), json=payload, timeout=30)
    resp.raise_for_status()
    post_urn = resp.headers.get("x-restli-id", "")
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    log.info("posted %s at %s", post_urn, ts)
    return {"status": "success", "dry_run": False, "post_url": f"https://www.linkedin.com/feed/update/{post_urn}/"}


if __name__ == "__main__":
    mcp.run()  # stdio transport
