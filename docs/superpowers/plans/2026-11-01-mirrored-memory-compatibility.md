# Android 6 mirrored-memory compatibility

Goal: correct the ENOSYS shared-memory initialization failure while retaining the original 11 audio capability records, media AAC, telephony and speech features. This is a compatibility candidate, not complete audio or CarPlay acceptance.

Evidence: the vendor ring initializer invokes ARM syscall385 (memfd_create) before decoding. On this television a separate native test returned fd=-1/errno38. The initializer propagates positive38 into MainAudio setup; recorded telephony requests then disconnect the session. The same television passed anonymous ashmem allocation, alias access across a double mapping and cleanup.

Implementation: call the original initializer first. Only a return38 invokes the own C adapter through existing resolved libc/libdl imports. Round capacity to pages, preserve optional next-power-of-two sizing and the exact six-word ring layout. Create anonymous ashmem using the existing system libcutils export; do not ftruncate ashmem. Reserve two contiguous regions, map the same fd into both, close the fd and keep only the mappings. Failure does not change ctx, and cleans fd/mappings/library. No audio data, images or credentials are persisted.

Native integration: exact Thumb entry bytes, immediate binding, RX padding and relocation guards. Original success and non-ENOSYS errors bypass the adapter. ASLR tests execute the actual original instructions and own linked code at two bases; assert return status, original-success preservation, ring layout, register/SP preservation, three map failures, descriptor cleanup and denied-error preservation.

Deliverables: own C/header, synthetic native platform test, actual-adapter native test, reproducible API23 runner, build flag --memory-probe ashmem, source documentation and release receipt. Only own source may be published; target libraries, binaries and logs remain ignored local/build.

Candidate audit43 retains the experimental spatial navigation and adds ashmem compatibility. The first-poll wait and delta-only wheel trials did not solve freezing and are omitted from this candidate. No performance inference can be attributed to one variable across those changes; test the memory initialization path specifically first. Default source remains audit38 until actual integration evidence permits promotion.

Acceptance: verify APK bytes, check live foreground before changing UI, inspect CnMirror/MainAudio setup and session state, and run safe remote traversal without real calls/messages or terms acceptance. User audio-quality/sync and final persistent-ADB checks remain last. Red果 MPV installation is independent and remains installed.
