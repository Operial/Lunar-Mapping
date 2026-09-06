# Server Discovery data mirror

A static, self-hosted mirror of the server metadata that
[serverdiscovery](../serverdiscovery) uses to populate its directory -
names, addresses, and descriptions only, sourced from
[LunarClient/ServerMappings](https://github.com/LunarClient/ServerMappings)
(public data, freely reusable per their docs). No images are mirrored, and
once this is hosted, the mod never contacts Lunar Client's CDN or repo at
runtime - only this page.

## One-time setup

1. Create a new **public** GitHub repository (e.g. `server-mappings-mirror`).
2. Upload every file in this folder (`servers.json`, `index.html`,
   `refresh.sh`, `aggregate.py`, this README) to that repo - drag-and-drop
   on the repo's "Add file → Upload files" page works fine, no `git`
   required for this step.
3. In the repo, go to **Settings → Pages**. Under "Build and deployment",
   set **Source** to "Deploy from a branch", **Branch** to `main` and
   folder to `/ (root)`, then **Save**.
4. GitHub shows the live URL at the top of that same Pages settings
   section a minute or two later - it looks like
   `https://<your-username>.github.io/<repo-name>/`.
5. Send that URL back and the mod's `ServerMappingsClient.java` gets
   pointed at `<that-url>servers.json` instead of Lunar's CDN.

## Keeping it fresh (optional, whenever you like)

This is a snapshot, not a live sync - re-run it whenever you want newer
data:

```
./refresh.sh
git add servers.json
git commit -m "Refresh server list"
git push
```

Requires `git` and `python3` on whatever machine you run it from (does
not need to be the same machine running Minecraft). GitHub Pages picks up
the new `servers.json` automatically within a minute or two of the push -
no settings to touch again.
