---
doc_id: ESC-001
title: IT Escalation Matrix
category: Process
owner: IT Service Management
last_reviewed: 2026-09-28
---

# ESC-001: IT Escalation Matrix

## Priority levels

| Priority | Definition | Response | Target resolution |
|---|---|---|---|
| P1 | Business-wide outage or security breach | 15 min | 4 hours |
| P2 | Major function down for a team or office | 1 hour | 8 hours |
| P3 | Single user affected, workaround exists | 4 hours | 3 business days |
| P4 | Request, question, or minor issue | 1 business day | 5 business days |

## Who handles what

| Issue type | First line | Second line | Third line |
|---|---|---|---|
| Password, MFA, access | Service Desk | Identity and Access Team | Security Team |
| Laptop, peripherals, printers | Service Desk | End User Computing | Vendor |
| Wi-Fi, VPN, network | Service Desk | Network Operations | Network vendor |
| Email, Slack, Zoom | Service Desk | Collaboration Team | SaaS vendor |
| Security incidents | Security Hotline | Security Operations | CISO |
| Production systems | On-Call Engineer | Platform Team | Engineering Manager |

## Escalation triggers

| Condition | Action |
|---|---|
| P1 not acknowledged in 15 minutes | Escalate to IT Operations Manager |
| P1 unresolved after 2 hours | Notify Head of IT |
| P2 unresolved after 6 hours | Escalate to IT Operations Manager |
| P3 breaches its target | Team Lead reviews and reprioritises |
| Any ticket involving Restricted data | Notify Security Team immediately |
| Any ticket with a suspected breach | Treat as P1 and call the Security Hotline |

## Contacts

| Team | Contact |
|---|---|
| Service Desk | +91-22-5555-0100, `itsupport@nimbus-logistics.example` |
| Security Hotline (24x7) | +91-22-5555-0199 |
| Security Team | `security@nimbus-logistics.example` |

## After-hours

Support hours are Monday to Friday, 9:00 AM to 7:00 PM IST. Outside these hours, only Critical issues are handled, through the Security Hotline or the On-Call rota.
