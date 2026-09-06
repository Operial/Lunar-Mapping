#!/usr/bin/env python3
"""Aggregates LunarClient/ServerMappings' per-server metadata.json files
into a single compact servers.json - the format serverdiscovery's
ServerMappingsClient.java expects. Only text metadata (name, address,
description) is kept; logos/backgrounds are intentionally not mirrored
(they'd be gigabytes across ~2500 servers) - the mod uses each server's
own live favicon instead.
"""
import json
import os
import sys


def main():
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} <path-to-cloned-ServerMappings-repo> <output-servers.json>")
        sys.exit(1)
    repo_dir, out_path = sys.argv[1], sys.argv[2]

    with open(os.path.join(repo_dir, "inactive.json"), encoding="utf-8") as f:
        inactive = set(json.load(f))

    servers_dir = os.path.join(repo_dir, "servers")
    servers = []
    for entry_id in sorted(os.listdir(servers_dir)):
        if entry_id in inactive:
            continue
        meta_path = os.path.join(servers_dir, entry_id, "metadata.json")
        if not os.path.isfile(meta_path):
            continue
        try:
            with open(meta_path, encoding="utf-8") as f:
                meta = json.load(f)
        except Exception:
            continue

        address = meta.get("primaryAddress")
        if not address:
            addrs = meta.get("addresses") or []
            address = addrs[0] if addrs else None
        if not address:
            continue

        servers.append({
            "id": meta.get("id", entry_id),
            "name": meta.get("name") or meta.get("id") or entry_id,
            "address": address,
            "description": meta.get("description", ""),
        })

    out = {
        "source": "https://github.com/LunarClient/ServerMappings",
        "note": "Self-hosted static mirror of public server metadata - no images, no CDN calls to Lunar Client.",
        "servers": servers,
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    print(f"Wrote {len(servers)} servers to {out_path}")


if __name__ == "__main__":
    main()
