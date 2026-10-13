---
doc_id: RB-007
title: Password Reset and Account Lockout
category: Identity
owner: Identity and Access Team
last_reviewed: 2026-09-10
applies_to: All employees
---

# RB-007: Password Reset and Account Lockout

## Self-service reset

1. Go to `reset.nimbus-logistics.example`.
2. Enter your work email.
3. Verify with MFA.
4. Choose a new password that meets the requirements below.

## Password requirements

- Minimum 14 characters
- Passphrases recommended
- Cannot match your last 10 passwords

## Account locked

- After 5 failed sign-ins, the account locks for 15 minutes.
- Wait 15 minutes, or use the self-service reset.
- If you do not know why your account locked, check for old saved passwords on a phone or laptop mail app, which often cause repeated failures.

## Cannot use self-service

Contact the Service Desk if:

- You cannot receive MFA prompts (see RB-002)
- You are a new joiner and your temporary credentials expired
- Your account was disabled after 90 days of inactivity

Identity verification is required before IT resets credentials.

## After a reset

1. Sign out of all devices and sign back in.
2. Update the saved password on your phone mail app and VPN client.
3. Update the password in the company password manager.

## Suspicious lockouts

If your account locks repeatedly and you did not cause it, someone may be trying to guess your password. Report it to `security@nimbus-logistics.example`.
