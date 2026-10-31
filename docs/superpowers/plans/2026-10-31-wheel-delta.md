# Relative-wheel delta-only contrast

Evidence: vendor Wheel descriptor Input=0x06 (Data/Variable/Relative), signed8-bit delta. Known construction and client enqueue paths copy data and do not compare it to a previous report. Current probe sends one nonzero delta plus a redundant zero wheel report100ms later. Removing the latter is an opt-in protocol contrast, not a proven fix for the client/phone delay.

Scope: --wheel-probe delta-only is valid only with a separate spatial input probe label. It removes only the zero report in CnProbeHost.send. Normal button/absolute-axis releases and CnInput cancellation neutral remain unchanged. Candidate42 retains the same first-poll and codec-return modes as41 for comparison. Independent light-appearance polarity support was also added to the pure geometry class; it preserves the current dark-frame predicate and is covered by17 synthetic cases, not yet light-theme device acceptance.

API23 validation: actual Host.send and actual CnInput queue with isolated native sink. Original emits2 reports and fails expected1; delta-only emits1 report and passes. Calling normal cancellation then emits the expected neutral as report2. No real phone input is used in this isolation test.

Real acceptance: inspect session before pairing, then compare safe direction/list/tab operations and latency with source receipts. Keep failure cases. No screenshots/recordings, no network/audio capability changes, no real calls/messages. Sound and final ADB remain last. If delta-only does not improve behavior, do not claim message count reduction solved compatibility.
