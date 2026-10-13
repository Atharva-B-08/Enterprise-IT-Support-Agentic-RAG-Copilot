---
doc_id: RB-002
title: MFA Lockout and Device Change Recovery
category: Identity
owner: Identity and Access Team
last_reviewed: 2026-09-20
applies_to: All employees
---

# RB-002: MFA Lockout and Device Change Recovery

## Scenarios covered

- You got a new phone and lost your authenticator app
- Your phone was lost, stolen, or reset
- MFA prompts are not arriving
- Codes are rejected as invalid

## Scenario A: MFA prompts not arriving or codes rejected

1. Check that your phone has internet access and the correct date and time set to **automatic**. One-time codes fail if the phone clock is wrong.
2. Open the authenticator app and check for a pending notification.
3. Try a one-time code instead of push approval, or the other way round.
4. Use your **hardware security key**, if one was issued to you.

If none of these work, move to Scenario B.

## Scenario B: New phone (old phone still available)

1. On the old phone, open the authenticator app and keep it signed in.
2. On your laptop, go to the security settings page and select **Add a new device**.
3. Scan the QR code with the authenticator app on the new phone.
4. Test a sign-in, then remove the old device.

## Scenario C: Lost, stolen, or unavailable phone

1. If the phone was lost or stolen, **report it immediately** (see the Incident Reporting section of the handbook). Critical incidents go to the Security Hotline.
2. Contact the IT Service Desk. You must verify your identity before IT can reset MFA:
   - Video call with the Service Desk, showing your company ID badge or government photo ID
   - Or confirmation from your manager through a separate channel
3. IT will reset your MFA enrolment. This takes about 15 minutes after verification.
4. Enrol the new device on first login.
5. Change your password after MFA is reset.

## Rules

- IT will **never** reset MFA based on an email or chat message alone.
- Privileged accounts cannot use SMS as a fallback.
- Backup hardware keys can be requested through a standard request ticket.

## Escalation

- Locked out of MFA with an urgent business need: raise **P2**.
- Suspected account compromise: call the Security Hotline (see handbook Section 13).
