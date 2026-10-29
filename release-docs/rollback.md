# FFideo rollback procedure

## Code rollback

- Approved 0.1.0 baseline commit: `ad71b7a6e5db04f836cac9e9fd70d053cf7719c6`.
- Production-readiness work remains on the local `production-readiness` branch.
- No remote or push is part of this procedure.

To inspect or rebuild a prior state, create a separate local worktree at the desired commit rather than rewriting the active branch.

## Artifact rollback

Keep every released directory immutable with its `SHA256SUMS`, source package, verification evidence, and Git commit identifier. Never replace a published file at the same version URL. A corrected build must use a higher build number or version.

## User rollback

Quit FFideo, preserve user-created outputs, replace the app bundle with the previously verified bundle, and re-run its checksum/signature verification. Trial/license storage migrations must be backward-compatible or explicitly documented before any public update.

## External release block

No upload, appcast publication, notarization submission, checkout change, or customer communication may occur without explicit owner approval.
