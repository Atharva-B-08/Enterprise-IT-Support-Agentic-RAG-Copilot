---
doc_id: RB-004
title: Lost or Stolen Device Response
category: Security
owner: Security Operations
last_reviewed: 2026-09-25
applies_to: Laptops, phones, tablets, security keys
---

# RB-004: Lost or Stolen Device Response

## Employee actions (first 60 minutes)

1. **Call the Security Hotline: +91-22-5555-0199** (24x7) immediately. Report within 1 hour of noticing the loss.
2. Tell the agent:
   - Device type and asset tag (if known)
   - When and where it was last seen
   - Whether it was locked and powered off
   - What data it may have held
3. If the device was stolen, file a police complaint and keep the reference number. Share it with the Security team.
4. Do not try to track or retrieve the device yourself.

## What Security and IT will do

| Action | Owner | Timing |
|---|---|---|
| Disable the user's sessions and tokens | Security | Immediately |
| Lock or remotely wipe the device | Endpoint team | Within 1 hour of report |
| Reset the user's password and MFA | Identity team | After the device is secured |
| Check access logs for suspicious activity | Security | Within 24 hours |
| Assess data exposure and notify Legal if required | Security + Legal | Within 24 hours |
| Issue replacement device | End User Computing | Within 1 business day |

## BYOD devices

For personal phones with the work profile installed, IT can wipe the **work profile only**. Personal data is not touched.

## Laptop encryption

All company laptops use full-disk encryption. A powered-off, locked laptop is considered lower risk, but it must still be reported.

## Restricted data exposure

If the device may have held Restricted data (customer personal data, credentials, financial records), the incident is treated as **Critical** and Legal is notified.

## No-blame reminder

Nimbus does not penalise good-faith loss reported promptly. Delayed reporting is treated more seriously than the loss itself.
