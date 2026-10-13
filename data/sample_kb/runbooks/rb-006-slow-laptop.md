---
doc_id: RB-006
title: Slow Laptop Performance
category: Hardware
owner: End User Computing
last_reviewed: 2026-08-20
applies_to: Company laptops
---

# RB-006: Slow Laptop Performance

## Quick checks (5 minutes)

1. **Restart** the laptop. Many laptops run for weeks without a restart, which causes slowdowns.
2. Close unused applications and browser tabs.
3. Check for pending OS or security updates and install them.
4. Check free disk space. Performance drops when less than 10% is free.

## Find what is using resources

**Windows:** Press `Ctrl + Shift + Esc` to open Task Manager. Sort by CPU, Memory, and Disk.
**macOS:** Open Activity Monitor and sort by CPU and Memory.

| Finding | Action |
|---|---|
| Browser using high memory | Close tabs; restart the browser |
| Cloud sync client using high disk | Let it finish; pause if urgent |
| Unknown process using high CPU | Do not end it; raise a ticket with a screenshot |
| Endpoint security scan running | Let it finish, typically under 30 minutes |

## Free up disk space

- Empty the Recycle Bin or Trash
- Remove old downloads
- Move large files to the company cloud drive
- Use the Software Portal to uninstall unused applications

## Do not

- Disable antivirus or the endpoint management agent to speed things up
- Install "cleaner" or "optimiser" tools

## Escalate when

- The laptop is slow even after restart and cleanup
- The fan runs constantly or the device is very hot
- The battery drains very quickly
- It has been more than 4 years since the laptop was issued (eligible for refresh)

Raise a **P3** ticket with the device name, the symptoms, and what you tried.
