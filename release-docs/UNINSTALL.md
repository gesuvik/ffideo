# Uninstall FFideo

1. In FFideo Settings, turn off **Open at Login** if it is enabled.
2. Quit FFideo and wait for any active conversion to finish or cancel.
3. Delete `FFideo.app` from its installation location.
4. Empty Trash if desired.

FFideo does not install system services, kernel extensions, privileged helpers, browser extensions, or system-wide daemons. The ad-hoc website build may create the per-user file `~/Library/LaunchAgents/lol.gesuvik.ffideo.login.plist` for **Open at Login**; turning the setting off removes it. If the app was deleted first, remove that file manually after logging out, or run `launchctl bootout gui/$(id -u)/lol.gesuvik.ffideo.login` before deleting it.

A future activated build may keep trial or license state in the user's secure/local application storage. The final public uninstaller documentation must name the exact storage identifiers after the production license integration is approved. Deactivating this Mac before deletion is recommended when that feature is enabled.

Converted media files are user documents and are never removed by uninstalling the app.
