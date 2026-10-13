---
doc_id: RB-005
title: Office Wi-Fi and Network Issues
category: Network
owner: Network Operations
last_reviewed: 2026-09-01
applies_to: Office locations
---

# RB-005: Office Wi-Fi and Network Issues

## Which network should I use?

| Network | For | Notes |
|---|---|---|
| `Nimbus-Corp` | Company laptops and approved devices | Certificate-based, no password to type |
| `Nimbus-Guest` | Visitors | Internet only; password changes weekly |
| `Nimbus-IoT` | Scanners and printers | IT managed |

Employees must use `Nimbus-Corp` for work. Do not use `Nimbus-Guest` to reach internal systems.

## Problem: Cannot connect to Nimbus-Corp

1. Turn Wi-Fi off and on.
2. Forget the network and reconnect.
3. Check that your device certificate is valid: open the Software Portal and run **Refresh Device Certificate**.
4. If your laptop was recently re-imaged or you changed your password, restart the laptop.
5. If still failing, raise a **P3** ticket with the device name and location.

## Problem: Connected but slow

1. Run a speed test and note the result.
2. Move closer to an access point or try a different floor or room.
3. Check whether others nearby are affected. If many users are affected, notify `#it-help` on Slack and raise **P2**.
4. Pause large downloads and cloud sync during the test.

## Problem: Wi-Fi drops during video meetings

1. Close unused browser tabs and apps.
2. Turn off your camera if bandwidth is limited.
3. Use a wired connection at your desk if available.

## Problem: Websites blocked

Web filtering blocks categories such as malware, adult content, and file-sharing. Do not try to bypass it. If a legitimate business site is blocked, raise a **P4** request with the URL and justification.

## Do not

- Plug in your own routers, switches, or access points
- Run network scans without authorisation from Security
