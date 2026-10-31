# Delivery status - 2026-11-01

This is a status-only closeout requested by the user, not authorization to resume adaptation. CarPlay work stays shelved; its unresolved results remain documented rather than marked passed.

| Item | Verified outcome | Remaining boundary |
|---|---|---|
| Aerial desktop | Version1.74 is installed, currently foreground. User confirmed Home returns to the desktop and icon names display normally. | This is an Apple-style Android desktop, not the Apple tvOS operating system. |
| Boot to Aerial | Prior real reboot observations and user confirmation showed automatic entry to Aerial. | No additional reboot was performed for this closeout. |
| Hongguo | MPV0.2.136, versionCode87, package rocks.aston.hongguotv.mpv installed and launched; installed APK bytes verified against the downloaded release. | Real episode playback, audio/sync, continuous episode changes and full remote traversal have NOT passed acceptance. The earlier Up/Down check did not establish movement because the reported focus stayed on the same recommendation node. |
| Source handoff | Own source and reproducible build/test materials are in the user-requested project directory. Last development commit221302b was pushed to the public GitHub repository. | Do not publish target logs, credentials, APKs, system libraries or complete third-party decompilations. This closeout adds only own status documentation. |
| Persistent ADB | Existing keep_adb setting enabled; the previously authorized computer could query the television during this closeout. | Reboot-plus-duration authorization persistence remains UNVERIFIED; no security-setting changes or reboot tests were performed. |
| AirPlay/screen mirroring | Receiver menus include these modes. | Menu presence does not prove end-to-end iPhone mirroring or casting; no comprehensive acceptance evidence is recorded. |
| CarPlay | SHELVED per user request. Current installed candidate audit44. Preview and test monitoring stopped; television returned to Aerial. | Directions, Siri, audio latency/quality, stale video, all-app coverage and full recovery remain incomplete. No further adaptation is running. |

Repository: https://github.com/Mars535821089-ops/Carplay-XiaoMi-MiTV4-ANSM0-601-API23
Branch: codex/tv-carplay-adaptation

Conclusion: desktop setup and application installation are delivered. It would be inaccurate to say all other functions have completed full acceptance.
