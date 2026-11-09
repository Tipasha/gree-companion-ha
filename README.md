# Gree Direct Discovery

Companion to Home Assistant's built-in Gree integration for networks that drop
Wi-Fi broadcast discovery. It sends Gree discovery probes directly to configured
IPv4 addresses at setup and every 60 seconds. The built-in integration still owns
pairing, polling, controls, devices, and entity IDs. No AC settings are changed.

## Installation

Keep Home Assistant's built-in **Gree Climate** integration configured and enabled.
The companion supplements discovery; it does not replace Gree Climate.

### HACS (recommended)

1. Open HACS in Home Assistant.
2. Click the three dots in the top right corner and select **Custom repositories**.
3. Add `https://github.com/Tipasha/gree-companion-ha` with category **Integration**.
4. Find **Gree Direct Discovery** and select **Download**.
5. Restart Home Assistant.
6. Go to **Settings → Devices & Services → Add Integration**.
7. Search for **Gree Direct Discovery** and follow the setup wizard.

### Manual

1. Download the [repository](https://github.com/Tipasha/gree-companion-ha).
2. Create `/config/custom_components/gree_direct/` on your Home Assistant instance.
3. Copy the repository's integration files and folders into that directory, so
   `manifest.json` is at `/config/custom_components/gree_direct/manifest.json`.
4. Restart Home Assistant.
5. Go to **Settings → Devices & Services → Add Integration**.
6. Search for **Gree Direct Discovery** and follow the setup wizard.

## Configuration

Enter the AC IPv4 addresses separated by commas. Reserve these addresses in your
router's DHCP settings. If addresses change, use the companion integration's
**Reconfigure** action to update them. Keep **Gree Climate** enabled.

This works around broadcast filtering; it does not repair Wi-Fi/router settings.
It uses the built-in Gree runtime discovery API (verified with HA 2026.9.3 and
greeclimate 2.1.4), which may need adaptation after future Home Assistant changes.
It resolves the current Gree runtime on every scan, including after a Gree reload.
Removing the companion stops direct probes without deleting Gree devices.

## Data and privacy

AC addresses are entered through Home Assistant's config flow and persisted by
Home Assistant in its config-entry storage, outside this integration directory.
The source contains no configured AC addresses, credentials, or device IDs.
The companion does not write configuration, logs, or device data into its source
directory and does not send telemetry or contact a cloud service. It sends local
discovery requests through the built-in Gree integration, which handles device
communication and may include addresses and device IDs in Home Assistant logs.

Do not publish Home Assistant's config-entry storage, logs, or diagnostics as part
of the integration repository.
