---
doc_id: RB-001
title: VPN Connection Troubleshooting
category: Network
owner: Network Operations
last_reviewed: 2026-09-15
applies_to: Windows, macOS
---

# RB-001: VPN Connection Troubleshooting

## Symptoms

- VPN client shows "Connecting..." and never completes
- Error: "Authentication failed"
- Error: "Gateway unreachable" or timeout
- VPN connects but internal sites (Jira, Confluence) do not load

## Step 1: Check basic connectivity

1. Open any public website (for example, a search engine). If it does not load, your internet is down; fix that first.
2. If you are on public or hotel Wi-Fi, try a mobile hotspot. Some public networks block VPN traffic.

## Step 2: Check authentication

1. Confirm your password works by signing in to Nimbus Mail.
2. Approve the MFA prompt promptly. MFA prompts expire after 60 seconds.
3. If you see "Authentication failed" and email works, your VPN certificate may have expired. Go to Step 4.
4. If your account is locked (5 failed attempts), wait 15 minutes or use the self-service reset at `reset.nimbus-logistics.example`.

## Step 3: Restart the client

1. Fully quit the VPN client (system tray or menu bar icon, then Quit).
2. Reopen it and try again.
3. If it still fails, restart the laptop.

## Step 4: Reinstall or repair the VPN profile

1. Open the **Software Portal** on your laptop.
2. Select **Nimbus VPN Client** and choose **Repair** (or Reinstall).
3. Sign in again and re-enrol MFA if prompted.

## Step 5: Connected but internal sites do not load

1. Disconnect and reconnect.
2. Flush DNS:
   - Windows: open Command Prompt and run `ipconfig /flushdns`
   - macOS: run `sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder`
3. Try opening the site by its full address, such as `wiki.nimbus-logistics.example`.
4. Check whether the issue affects one site or all sites. If only one site fails, raise a ticket for that application instead.

## When to escalate

Raise a **P3** ticket if steps 1 to 5 do not work. Raise a **P2** ticket if several users in the same office report VPN failure. Attach:

- Screenshot of the error
- Time the issue started
- Your location (home, office, public Wi-Fi)
- Device name (Settings > About)

## Notes

- Do not disable the VPN to "test" access to internal systems.
- Split tunnelling is not permitted for production access.
