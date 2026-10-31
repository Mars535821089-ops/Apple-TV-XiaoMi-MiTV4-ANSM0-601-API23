# Video return-status diagnostic

Goal: distinguish native codec errors from the observed video tail/drain timing window. This is telemetry only, not a decoder fix.

Evidence: video queueInputBuffer and releaseOutputBufferAtTime return values are ignored before in/out counters increment. Input callbacks queue then drain outputs with timeout0; no independent video pump has been located. Monotonic clock units were verified correct. Current visible focus may advance only after an older displayed frame remains for seconds.

Scope: separate --video-probe return-status build label, preserving default audit38 and all pairing/audio/network settings. Hook only the four-byte non-PC-relative LDRD immediately after each video call (0x14cba6 and 0x14c940). Own trace stubs log status through the existing Android logging import, preserve live registers/stack, replay the exact displaced instruction, and return to the next original instruction. Do not change arguments, timing thresholds, return values, authentication or codec selection. Reuse only verified zero-filled padding between allocated sections inside the original read/execute mapping; no segment permission changes, writable executable mapping or vendor source publication.

Steps:
1. Implement exact-byte/ELF checks and two trace stubs in experiments/video_return_probe.py. Run Unicorn at two relocated bases with success/error returns; assert log argument, register/SP preservation and original counter update. No real transport.
2. Add explicit build flag, protect baseline labels, preserve resources and signing checks. Enable only own CnVideoReturn metadata in bounded private monitoring.
3. Independently build and verify candidate, install once, inspect existing session before reconnecting. Reproduce safe direction/setting navigation; capture statuses and native surface/output events. Never Select unknown contacts or retry unknown installations.
4. If nonzero queue/release is observed, trace that failure before changing behavior. If both succeed but output is held, isolate drain timing. Do not infer all failures from one successful frame or automatically recreate every static page.

No screenshots/recordings/pixels are written. Device logs stay ignored local/. Audio and final ADB acceptance remain last. Full compatibility remains unachieved.

Ruling: the existing owned RX bridge is more than16MiB from the return sites, outside Thumb branch range. The alternative is the verified4088-byte zero gap after .ARM.extab and before .rodata, with no allocated section or relocation target in it. The first candidate gap was correctly rejected because .rel.plt occupies it. No installed package used that rejected attempt. Both hook branches, logger calls, original instruction replay, stack/register preservation and 64-bit counter increments passed12 Unicorn cases at two ASLR bases. Output cannot equal source.
