# Install FFideo 1.0.0

> RC local only. The current artifact is ad-hoc signed and not notarized.

1. Verify `SHA256SUMS` from the release directory.
2. Extract `FFideo-1.0.0.zip`.
3. Move `FFideo.app` to `/Applications` or another folder owned by the current user.
4. Launch FFideo.

Enable **Open at Login** only after moving FFideo to its final location. This ad-hoc build uses a per-user LaunchAgent fallback when macOS does not expose the main app through `SMAppService`; if the app is moved later, launch it manually once so Launch Services sees its new location.

For a future non-notarized private beta, macOS may require an explicit owner-approved exception through **System Settings → Privacy & Security → Open Anyway**. Do not disable Gatekeeper globally.

Public distribution remains blocked until the owner chooses and verifies an approved trust path.
