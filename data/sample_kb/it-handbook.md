---
doc_id: HANDBOOK-2.4
title: Nimbus Logistics IT Handbook
category: Policy
owner: IT Department
status: active
published: 2026-10-01
---

# Nimbus Logistics Pvt. Ltd. — IT Handbook

**Document Owner:** IT Department
**Version:** 2.4
**Effective Date:** 1 October 2026
**Applies To:** All employees, contractors, and interns

> This is a sample document for a fictional company, created for illustration and template purposes.

---

## Table of Contents

1. [Welcome and Purpose](#1-welcome-and-purpose)
2. [Getting Started: Onboarding](#2-getting-started-onboarding)
3. [Accounts and Access Management](#3-accounts-and-access-management)
4. [Passwords and Authentication](#4-passwords-and-authentication)
5. [Hardware and Equipment](#5-hardware-and-equipment)
6. [Software and Licensing](#6-software-and-licensing)
7. [Network, Wi-Fi, and VPN](#7-network-wi-fi-and-vpn)
8. [Email and Collaboration Tools](#8-email-and-collaboration-tools)
9. [Information Security Policy](#9-information-security-policy)
10. [Acceptable Use Policy](#10-acceptable-use-policy)
11. [Remote Work and BYOD](#11-remote-work-and-byod)
12. [Data Backup and Retention](#12-data-backup-and-retention)
13. [Incident Reporting](#13-incident-reporting)
14. [IT Support and Service Desk](#14-it-support-and-service-desk)
15. [Offboarding](#15-offboarding)
16. [FAQ](#16-faq)
17. [Appendix: Quick Reference](#17-appendix-quick-reference)

---

## 1. Welcome and Purpose

Nimbus Logistics Pvt. Ltd. is a Mumbai-headquartered supply chain and freight-tech company with offices in Mumbai, Pune, and Bengaluru, and a warehouse network across India.

This handbook explains how technology is provided, used, and protected at Nimbus. It helps you:

- Get set up quickly in your first week
- Know what you can and cannot do with company systems
- Keep company and customer data safe
- Get help fast when something breaks

**Our IT principles**

| Principle | What it means |
|---|---|
| Secure by default | Security controls are on unless there is an approved reason to turn them off |
| Least privilege | You get the access you need for your role, and no more |
| Self-service first | Common tasks should be doable without raising a ticket |
| One source of truth | Tools, assets, and documentation live in approved systems only |

---

## 2. Getting Started: Onboarding

### 2.1 Before Day 1

IT prepares the following once HR confirms your joining date:

- Corporate email account and directory profile
- Laptop, imaged and encrypted
- Role-based access groups (see Section 3)
- Welcome email with your temporary credentials and joining instructions

### 2.2 Day 1 Checklist

- [ ] Collect your laptop and accessories from the IT desk (or courier, for remote hires)
- [ ] Sign the Equipment Acknowledgement Form
- [ ] Log in and change your temporary password
- [ ] Enrol in Multi-Factor Authentication (MFA)
- [ ] Install the Nimbus VPN client from the Software Portal
- [ ] Join the `#it-help` channel on Slack
- [ ] Complete the mandatory Security Awareness training (within 7 days)

### 2.3 First-Week Tools

| Tool | Purpose | How to access |
|---|---|---|
| Nimbus Mail | Email and calendar | mail.nimbus-logistics.example |
| Slack | Team chat | Desktop or mobile app |
| Zoom | Video meetings | Software Portal |
| Jira | Tickets and project tracking | jira.nimbus-logistics.example |
| Confluence | Documentation | wiki.nimbus-logistics.example |
| HR Portal | Payslips, leave, policies | hr.nimbus-logistics.example |
| Software Portal | Approved software installs | Self-service app on laptop |

---

## 3. Accounts and Access Management

### 3.1 Account Types

- **Standard account:** Issued to every employee, tied to a single named individual.
- **Privileged account:** For administrators only, issued separately and monitored.
- **Service account:** For applications and automation, owned by a named team.
- **Guest account:** For visitors and short-term vendors, limited to 30 days.

### 3.2 Requesting Access

1. Raise an **Access Request** ticket in the Service Desk.
2. Specify the system, access level, and business justification.
3. Your manager approves; for sensitive systems, the system owner also approves.
4. IT provisions access within **2 business days**.

### 3.3 Access Reviews

Managers review team access every quarter. Access that is no longer needed is removed. Accounts unused for 90 days are automatically disabled.

### 3.4 Rules

- Never share your account with anyone, including your manager or IT staff.
- Do not use another person's credentials, even if offered.
- Privileged access must be requested separately and expires after 12 months unless renewed.

---

## 4. Passwords and Authentication

### 4.1 Password Requirements

| Requirement | Standard |
|---|---|
| Minimum length | 14 characters |
| Complexity | Passphrases recommended (e.g., four unrelated words) |
| Reuse | Cannot reuse your last 10 passwords |
| Expiry | Every 365 days, or immediately if compromise is suspected |
| Lockout | 5 failed attempts locks the account for 15 minutes |

### 4.2 Multi-Factor Authentication (MFA)

MFA is **mandatory** for email, VPN, cloud consoles, and all admin systems.

- **Preferred:** Authenticator app (push or one-time code)
- **Backup:** Hardware security key (issued on request)
- **Not allowed for privileged accounts:** SMS codes

### 4.3 Password Manager

Nimbus provides a company password manager. Use it to generate and store unique passwords for every work system. Do not store passwords in spreadsheets, notes apps, or browsers.

### 4.4 If You Forget Your Password

Use the self-service reset at `reset.nimbus-logistics.example`. If you are locked out of MFA, contact the Service Desk with ID verification.

---

## 5. Hardware and Equipment

### 5.1 Standard Issue

| Role | Device | Accessories |
|---|---|---|
| Engineering | 16" laptop, 32 GB RAM | Monitor, keyboard, mouse, headset |
| Operations / Business | 14" laptop, 16 GB RAM | Mouse, headset |
| Warehouse supervisors | Rugged tablet | Scanner, protective case |

### 5.2 Your Responsibilities

- Keep devices physically secure; never leave them unattended in public or in a vehicle.
- Do not remove or disable disk encryption, antivirus, or the endpoint management agent.
- Report loss or theft **within 1 hour** (see Section 13).
- Return all equipment on exit (see Section 15).

### 5.3 Refresh Cycle

Laptops are refreshed every **4 years**. Earlier replacement is available for hardware faults. Request via the Service Desk.

### 5.4 Personal Peripherals

Personal keyboards, mice, and monitors are fine. Personal USB storage devices are **blocked** by default. Request an exception if you have a legitimate need.

---

## 6. Software and Licensing

### 6.1 Approved Software

Install software only from the **Software Portal**. It contains pre-approved, licensed, and security-reviewed applications.

### 6.2 Requesting New Software

1. Search the Software Portal first.
2. If not listed, raise a **Software Request** with the business need.
3. IT and Security review for licensing, cost, and risk (typically 5 business days).

### 6.3 Not Allowed

- Pirated or cracked software
- Unapproved file-sharing or remote-access tools
- Browser extensions that read all page data without approval
- Cryptocurrency miners or similar software

### 6.4 Developer Tools

Engineers may install IDEs, language runtimes, and containers from approved sources. Open-source dependencies must pass the automated licence and vulnerability scan in CI before release.

### 6.5 AI Tools

Use only AI assistants approved by Nimbus. Do **not** paste customer data, credentials, source code marked Confidential, or contract details into unapproved AI tools. See the AI Usage Guideline on Confluence for the approved list.

---

## 7. Network, Wi-Fi, and VPN

### 7.1 Office Wi-Fi

| Network | Who | Notes |
|---|---|---|
| `Nimbus-Corp` | Employees | Company devices only; certificate-based |
| `Nimbus-Guest` | Visitors | Internet only; password changes weekly |
| `Nimbus-IoT` | Scanners, printers | Managed by IT; do not connect personal devices |

### 7.2 VPN

Use the company VPN whenever you access internal systems from outside an office. Do not disable it while working. Split tunnelling is not permitted for production access.

### 7.3 Public Networks

Avoid public Wi-Fi where possible. If you must use it, connect to the VPN first.

### 7.4 Network Rules

- Do not connect unapproved routers, switches, or access points.
- Do not scan or probe the network unless you are authorised by Security.
- Do not bypass web filtering.

---

## 8. Email and Collaboration Tools

### 8.1 Email

- Use your company email for all work communication.
- Do not auto-forward work email to personal accounts.
- Be cautious with attachments and links; see the phishing guidance in Section 9.4.
- Mailbox size limit: 50 GB. Retention rules are in Section 12.

### 8.2 Slack

- Use public channels by default; use private channels or DMs only when needed.
- Do not share passwords, keys, or customer personal data in Slack.
- Customer data may be shared only in channels approved for that purpose.

### 8.3 Video Meetings

- Use waiting rooms for external meetings.
- Do not record meetings without informing participants.
- Do not share meeting links publicly.

### 8.4 File Sharing

Store work files in the company cloud drive. Share by link with named people, not "anyone with the link". External sharing of Confidential or Restricted files needs manager approval.

---

## 9. Information Security Policy

### 9.1 Data Classification

| Level | Description | Examples | Handling |
|---|---|---|---|
| **Public** | Approved for anyone | Marketing material, job posts | No restrictions |
| **Internal** | For employees only | Org charts, internal wikis | Do not share externally |
| **Confidential** | Business sensitive | Contracts, pricing, source code | Need-to-know; encrypted in transit and at rest |
| **Restricted** | Highest sensitivity | Customer personal data, credentials, financial records | Strict access control; logged; no local copies |

### 9.2 Core Rules

- Lock your screen when you step away (`Win + L` or `Ctrl + Cmd + Q`).
- Do not store Restricted data on laptops, phones, or personal storage.
- Use encrypted channels only (HTTPS, SFTP, VPN).
- Dispose of printed Confidential material by shredding.

### 9.3 Secure Development Basics

- Never commit secrets (API keys, tokens, passwords) to code repositories.
- Use the secrets manager for credentials.
- Code that handles Restricted data requires a security review before release.
- Dependencies are scanned automatically; critical findings must be fixed before deployment.

### 9.4 Spotting Phishing

Be suspicious of messages that:

- Create urgency ("pay now", "account will be closed")
- Ask for credentials, OTPs, or gift cards
- Come from a lookalike domain or unexpected sender
- Contain unexpected attachments or shortened links

**What to do:** Do not click. Use the **Report Phish** button in your mail client, or forward to `security@nimbus-logistics.example`.

### 9.5 Physical Security

- Wear your ID badge visibly in the office.
- Do not let unknown people follow you through access-controlled doors.
- Escort visitors at all times.

---

## 10. Acceptable Use Policy

### 10.1 Permitted Use

Company systems are provided for business use. Limited, reasonable personal use is allowed if it does not affect work, security, or company reputation.

### 10.2 Prohibited Activities

- Accessing, storing, or sharing illegal, offensive, or discriminatory content
- Harassing or threatening others using company systems
- Attempting to gain access to systems or data you are not authorised for
- Installing malware or deliberately disrupting services
- Using company systems for personal business or political campaigns
- Violating copyright or software licensing terms

### 10.3 Monitoring

Nimbus may monitor use of company systems, including email, web traffic, and device activity, to protect security and ensure compliance, consistent with applicable Indian law and the Company Privacy Notice.

### 10.4 Consequences

Violations may lead to access suspension, disciplinary action, or termination, and in serious cases, legal action.

---

## 11. Remote Work and BYOD

### 11.1 Working Remotely

- Use a company laptop and the VPN.
- Work from a private location where screens cannot be seen by others.
- Do not use shared or public computers for work.
- Keep home Wi-Fi secured with WPA2/WPA3 and a strong password.

### 11.2 Bring Your Own Device (BYOD)

Personal phones and tablets may access email, Slack, and calendar only, under these conditions:

| Requirement | Detail |
|---|---|
| Enrolment | Install the Mobile Device Management (MDM) work profile |
| Screen lock | PIN, fingerprint, or face unlock required |
| OS updates | Supported, up-to-date OS version |
| Jailbroken or rooted devices | Not permitted |
| Lost device | Report within 1 hour; IT may remotely wipe the **work profile only** |

Personal laptops may **not** be used to access Confidential or Restricted data.

### 11.3 Working from Abroad

Notify your manager and IT before working outside India. Some countries have restrictions on encryption or data access, and access from certain regions may be blocked.

---

## 12. Data Backup and Retention

### 12.1 Backups

| Data | Backup frequency | Retention |
|---|---|---|
| Production databases | Continuous + daily snapshot | 35 days |
| File shares and cloud drive | Daily | 90 days |
| Email | Continuous | 7 years (legal hold applies) |
| Laptops | **Not backed up** | Store work files in the cloud drive |

### 12.2 Your Responsibility

Save work to the cloud drive, not only to your local disk. If your laptop fails, files stored only locally may be lost.

### 12.3 Retention Rules

- Retain business records per the Records Retention Schedule (HR portal).
- Do not delete data that is subject to a legal hold, even if the schedule would otherwise allow it.
- Request restoration of deleted files via the Service Desk within the retention window.

---

## 13. Incident Reporting

### 13.1 What Counts as an Incident

- Lost or stolen device
- Suspected phishing or malware
- Unauthorised access to an account or system
- Accidental sharing of Confidential or Restricted data
- Unusual system behaviour (ransom notes, unexpected pop-ups, locked files)

### 13.2 How to Report

| Urgency | Action | Time limit |
|---|---|---|
| **Critical** (data breach, ransomware, lost device with data) | Call the Security Hotline: **+91-22-5555-0199** (24x7) | Immediately, within 1 hour |
| **High / Medium** | Email `security@nimbus-logistics.example` or raise a Security Incident ticket | Same day |
| **Low** (suspicious email) | Use **Report Phish** button | When noticed |

### 13.3 What to Do While Waiting

1. Disconnect from the network if you suspect malware (turn off Wi-Fi; do not shut down).
2. Do not delete anything or try to "fix" it yourself.
3. Write down what happened and when.
4. Follow instructions from the Security team.

### 13.4 No-Blame Reporting

Report quickly and honestly. Nimbus encourages early reporting and does not penalise good-faith mistakes reported promptly.

---

## 14. IT Support and Service Desk

### 14.1 Contact Options

| Channel | Details | Best for |
|---|---|---|
| Service Portal | support.nimbus-logistics.example | Tickets, requests, tracking |
| Email | `itsupport@nimbus-logistics.example` | Non-urgent issues |
| Slack | `#it-help` | Quick questions |
| Phone | +91-22-5555-0100 | Urgent issues |
| Walk-up desk | Mumbai HQ, 3rd Floor | Hardware, in person |

**Support hours:** Monday to Friday, 9:00 AM to 7:00 PM IST. After-hours support for Critical issues only, via the Security or On-Call hotline.

### 14.2 Priority and Response Targets

| Priority | Definition | Response | Target resolution |
|---|---|---|---|
| **P1 Critical** | Business-wide outage or security breach | 15 minutes | 4 hours |
| **P2 High** | Major function down for a team | 1 hour | 8 hours |
| **P3 Medium** | Single user issue, workaround exists | 4 hours | 3 business days |
| **P4 Low** | Request, question, minor issue | 1 business day | 5 business days |

### 14.3 Tips for a Faster Resolution

- Describe the problem and what you were doing when it happened.
- Include screenshots and exact error messages.
- Mention your device name (found in **Settings > About**).
- One issue per ticket.

### 14.4 Common Self-Service Fixes

| Problem | Try this first |
|---|---|
| Slow laptop | Restart; close unused apps; check for pending updates |
| Can't connect to VPN | Check internet; restart VPN client; verify MFA |
| Can't print | Confirm you are on `Nimbus-Corp`; re-add printer from Software Portal |
| Locked out | Use the self-service password reset |
| Meeting audio issues | Check Zoom audio settings; try a headset |

---

## 15. Offboarding

### 15.1 Your Last Week

- Transfer ownership of files, repositories, and shared documents to your manager or a named colleague.
- Return all company equipment and accessories (laptop, charger, badge, security keys, scanners).
- Remove company data from any personal devices.

### 15.2 On Your Last Day

IT will:

- Disable your accounts and revoke VPN and MFA access
- Remove you from groups and shared channels
- Wipe the work profile from any enrolled personal device
- Forward your email to your manager for 30 days (when applicable)

### 15.3 After You Leave

Your mailbox and files are retained per the Retention Schedule. You must not access or retain any Nimbus data after your last day.

---

## 16. FAQ

**Can I install Chrome extensions?**
Only those listed in the Software Portal. Request others via a Software Request.

**Can I use my personal laptop for work?**
No for Confidential or Restricted data. Personal phones can access email and Slack via MDM.

**I got a suspicious email. What should I do?**
Do not click anything. Use **Report Phish** or forward it to `security@nimbus-logistics.example`.

**How long does a new laptop take?**
Standard requests take 5 business days. Urgent replacements for faults are prioritised.

**Can I connect my own USB drive?**
USB storage is blocked by default. Raise an exception request with a business justification.

**Can I use ChatGPT or other AI tools with work data?**
Only approved AI tools, and never with Confidential or Restricted data in unapproved tools.

**Who do I contact if I lose my laptop on a weekend?**
Call the Security Hotline at +91-22-5555-0199 immediately.

---

## 17. Appendix: Quick Reference

### Key Contacts

| Team | Contact |
|---|---|
| IT Service Desk | +91-22-5555-0100 / `itsupport@nimbus-logistics.example` |
| Security Hotline (24x7) | +91-22-5555-0199 |
| Security Team | `security@nimbus-logistics.example` |
| HR Helpdesk | `hr@nimbus-logistics.example` |

### Golden Rules

1. **Lock your screen** when you walk away.
2. **Use MFA** everywhere it is offered.
3. **Think before you click.** Report anything suspicious.
4. **Keep Restricted data** off laptops and personal tools.
5. **Report incidents fast**, within one hour for anything serious.
6. **Use only approved software and AI tools.**

### Document Control

| Version | Date | Author | Change |
|---|---|---|---|
| 2.4 | 01 Oct 2026 | IT Department | Added AI tools guidance and BYOD update |
| 2.3 | 01 Apr 2026 | IT Department | Updated password policy |
| 2.0 | 01 Oct 2025 | IT Department | Major revision |

---

*This handbook is reviewed every six months. Suggestions? Post in `#it-help` or email `itsupport@nimbus-logistics.example`.*
