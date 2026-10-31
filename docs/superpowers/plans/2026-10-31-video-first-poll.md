# Controlled first output-poll wait

Evidence: audit40 real device captured648 queue and642 release calls with status0. A settings DOWN at21:15:03 produced4 queue/3 release, no calls04-07, then08 produced8 queue/9 release. The selected next row became confirmed after5.25s. This supports the already-found drain-after-input zero-wait tail window; it does not prove every stall has the same cause.

Intervention: hook only the four-byte fallback-pointer setup at0x14c8f6. Earlier original code has already initialized tag/format pointers and BufferInfo. The stub writes the exact original fallback pointer to originalSP+0x24, calls the same decoder dequeue with timeout5000us, and rejoins result handling0x14c924. Original subsequent polls0x14c918 retain timeout0. No new local-stack flag, output thread, codec selection, input format, release timestamp, pairing or audio capability change.

Owned code is confined to the last256 verified zero bytes before.rodata, inside existing RX permissions, outside allocated sections and relocation targets. Return-status trace uses the separate front of that padding. Immediate import binding and exact displaced bytes are required. No source overwrite.

Verification: the real original Thumb first poll failed the expected5000us check. The new stub passed6 ASLR/status cases, each exercising first5000us then original loop0, preserving result/SP/callee registers/fallback and original LR. Real hardware remains required, including initial connection, static tail, directions, app changes, resource pressure and audio contention. Results later than5ms can still miss this bounded window; do not claim a complete independent output pump or all stalls fixed.

Build: --input-probe spatial-navigation --video-probe first-poll-wait-return-status --label audit41-video-first-poll. Default audit38 remains unchanged. User audio and final ADB verification remain last.
