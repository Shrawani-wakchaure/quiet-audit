import json

with open("scenarios.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Ensure only up to Chapter 3 currently exists
scenarios = [s for s in data["scenarios"] if s["id"] not in ["boardroom-phish", "shadow-ai-leak"]]

# Chapter 4: The Boardroom Phish
ch4 = {
    "id": "boardroom-phish",
    "chapter": 4,
    "title": "The Boardroom Phish",
    "subtitle": "Executive Wire Fraud & Illicit OAuth Apps",
    "category": "Phishing Defense & Financial Controls",
    "compliance_framework": "SOC 2 CC6.8 (Malware Defense) / NIST CSF DE.CM-1",
    "badge": "badge_incident",
    "difficulty": "Challenging",
    "summary": "At 4:45 PM on Friday, the CFO receives an urgent email from the 'CEO' requesting an immediate $350k wire, while an unauthorized OAuth app hijacks corporate email.",
    "briefing": {
        "context": "It is Friday at 4:45 PM. SnoozeCloud is closing its crucial $20M Series B round. CFO Evelyn receives an urgent email appearing to come from the CEO's personal iCloud account: 'Evelyn, the escrow bank account changed at the last second! Please wire $350,000 immediately to this overseas account before the wires cut off at 5:00 PM, or we lose the lead investor.' Simultaneously, Barnaby's security telemetry detects a suspicious Google Workspace OAuth authorization: an unverified app called 'FinanceAutoSync' was granted read-write access to Evelyn's corporate inbox.",
        "urgency": "CRITICAL (Active Wire Fraud & Phishing)",
        "companion_intro": "Hold onto your tea mugs, Risk Manager! This is an executive spear-phish and Business Email Compromise (BEC) in progress! The attacker is using an illicit OAuth app to monitor the CFO's inbox while impersonating the CEO. One wrong click and our company bank account gets drained by $350,000! Let's handle this with ironclad financial controls.",
        "initial_state": {
            "audit_readiness": 65,
            "company_trust": 75,
            "budget": 85000
        }
    },
    "phases": {
        "phase_1": {
            "phase_id": "phase_1",
            "title": "Phase 1: The Urgent $350k Wire Request",
            "story": "CFO Evelyn is panicked on Slack in #finance-urgent: 'I have the bank portal open on my laptop right now! Should I click send? If I don't send this wire in 12 minutes, the Series B might fall through!' What is your immediate executive counsel?",
            "companion_tip": "Never authorize financial disbursements based on email alone. Execute a mandatory out-of-band voice callback to the CEO over a known pre-registered phone number.",
            "companion_mood": "alert",
            "choices": [
                {
                    "id": "out_of_band_verification",
                    "title": "Halt Wire & Perform Out-of-Band Voice Verification with CEO",
                    "description": "Instruct Evelyn to freeze the bank portal immediately, call the CEO directly on his verified personal cell phone, and isolate Evelyn's laptop.",
                    "type": "good",
                    "effects": {
                        "audit_readiness": 15,
                        "company_trust": 15,
                        "budget": -500
                    },
                    "consequence": "The CEO answers immediately: 'I never sent any wire request! I am sitting with the lead investor right now, our escrow account has not changed!' Wire halted, $350k saved, and Evelyn sighs with immense gratitude.",
                    "companion_reaction": "Purr-fect verification! Out-of-band voice verification is the ultimate antidote to Business Email Compromise. You just saved the company $350,000!",
                    "companion_mood": "happy",
                    "next_phase_id": "phase_2"
                },
                {
                    "id": "approve_wire_under_pressure",
                    "title": "Approve the Wire to Avoid Delaying the Series B",
                    "description": "Tell Evelyn: 'It's the CEO during a critical deal closing, we can't afford to delay—click send!'",
                    "type": "bad",
                    "effects": {
                        "audit_readiness": -30,
                        "company_trust": -35,
                        "budget": -350000
                    },
                    "consequence": "CATASTROPHE! The wire transfers instantly to an offshore bank account in Eastern Europe and is routed into crypto mixers within 4 minutes. The company's payroll reserve is wiped out!",
                    "companion_reaction": "HISSSSSS! Barnaby knocks his coffee mug off the desk in sheer shock! You just wired $350,000 to an overseas attacker without verbal authorization!",
                    "companion_mood": "alert",
                    "remediation": {
                        "trigger_reason": "Failure to enforce dual-custody authorization for high-value financial transactions.",
                        "situation": "The $350k wire left the company account. Attacker is laundering it. You need emergency wire recall and fraud response.",
                        "remediation_choices": [
                            {
                                "id": "rem_fbi_ic3_recall",
                                "title": "Emergency FBI IC3 & SWIFT Bank Fraud Recall",
                                "description": "Trigger the bank's fraud kill-switch, submit an FBI Internet Crime Complaint (IC3) priority freeze, and file an emergency insurance claim.",
                                "effects": {
                                    "audit_readiness": 10,
                                    "company_trust": 5,
                                    "budget": -25000
                                },
                                "consequence": "The FBI Financial Fraud Kill Chain successfully froze $220,000 before it left the intermediary correspondent bank. Devastating loss, but partial recovery achieved.",
                                "companion_reaction": "A harrowing escape. Dual authorization must be hardcoded into banking portals so no single human can ever bypass it again.",
                                "companion_mood": "detective",
                                "next_phase_id": "phase_2"
                            }
                        ]
                    }
                }
            ]
        },
        "phase_2": {
            "phase_id": "phase_2",
            "title": "Phase 2: Illicit OAuth Grant & Inbox Forwarding",
            "story": "The wire crisis is managed, but the attacker is still inside Evelyn's Google Workspace via the 'FinanceAutoSync' OAuth token. Cloud audit logs reveal the app created an automated inbox rule to forward all emails containing 'escrow', 'wire', or 'invoice' to an external anonymous address.",
            "companion_tip": "OAuth token theft bypasses passwords and MFA! Revoke the token tenant-wide via Google Workspace Admin API and audit all mailbox forwarding rules.",
            "companion_mood": "detective",
            "choices": [
                {
                    "id": "revoke_oauth_and_forwarding",
                    "title": "Tenant-Wide OAuth App Revocation & Purge Forwarding Rules",
                    "description": "Revoke the malicious OAuth grant across the entire domain, purge all hidden inbox forwarding rules, and restrict third-party app installations to admin-approved list only.",
                    "type": "good",
                    "effects": {
                        "audit_readiness": 15,
                        "company_trust": 10,
                        "budget": -2000
                    },
                    "consequence": "The attacker's persistent access is severed instantly. The malicious forwarding rule is deleted, and automated DLP alerts are deployed to block unauthorized email routing.",
                    "companion_reaction": "Brilliant log forensics! Attackers love OAuth persistence because users forget to audit third-party apps. The domain perimeter is sealed tight.",
                    "companion_mood": "happy",
                    "next_phase_id": "phase_3"
                },
                {
                    "id": "just_change_password",
                    "title": "Just Change Evelyn's Password and Move On",
                    "description": "Have Evelyn change her Google password and assume the hacker has been locked out.",
                    "type": "risky",
                    "effects": {
                        "audit_readiness": -10,
                        "company_trust": -10,
                        "budget": 0
                    },
                    "consequence": "A dangerous oversight! OAuth tokens remain valid even after password resets. The attacker continues monitoring the CFO's inbox for 48 hours until caught during audit review.",
                    "companion_reaction": "Risk Manager... OAuth refresh tokens do NOT expire upon password reset! You must revoke the token itself in Google Workspace Admin!",
                    "companion_mood": "alert",
                    "next_phase_id": "phase_3"
                }
            ]
        },
        "phase_3": {
            "phase_id": "phase_3",
            "title": "Phase 3: Dual-Custody & FIDO2 Policy",
            "story": "The crisis is contained, but the Board of Directors wants permanent controls to ensure an executive phishing attack can never threaten the company again. What systemic control framework do you implement?",
            "companion_tip": "Dual-custody workflows and FIDO2 WebAuthn hardware keys render credential phishing mathematically obsolete.",
            "companion_mood": "happy",
            "choices": [
                {
                    "id": "implement_dual_custody_and_fido2",
                    "title": "Mandate Banking Dual-Custody & FIDO2 YubiKeys for All Execs",
                    "description": "Enforce strict bank dual-authorization for wires >$10k requiring physical hardware token approval from two separate officers, and issue FIDO2 YubiKeys company-wide.",
                    "type": "good",
                    "effects": {
                        "audit_readiness": 20,
                        "company_trust": 15,
                        "budget": -4000
                    },
                    "consequence": "The Board of Directors is thrilled! Dual custody eliminates single points of human failure, and hardware FIDO2 keys eliminate credential harvesting permanently.",
                    "companion_reaction": "Purr-fect defense-in-depth! Dual custody turns financial integrity into an unbreakable institutional standard.",
                    "companion_mood": "happy",
                    "next_phase_id": "conclusion"
                },
                {
                    "id": "mandatory_all_hands_quiz",
                    "title": "Send an All-Hands Email with a Mandatory 10-Question Quiz",
                    "description": "Blame human error, scold the team, and assign a mandatory 30-minute compliance video and quiz.",
                    "type": "risky",
                    "effects": {
                        "audit_readiness": 5,
                        "company_trust": -15,
                        "budget": -1000
                    },
                    "consequence": "Engineering and executive morale dips. Everyone clicks through the video on 2x speed without learning, while systemic financial vulnerabilities remain unaddressed.",
                    "companion_reaction": "Compliance theater at its finest! Scolding employees does not fix architecture. Build paved roads and technical dual custody instead!",
                    "companion_mood": "detective",
                    "next_phase_id": "conclusion"
                }
            ]
        }
    },
    "conclusion": {
        "success_threshold": {
            "audit_readiness": 75,
            "company_trust": 65,
            "budget": 35000
        },
        "takeaway": "Real GRC Lesson: Business Email Compromise (BEC) cannot be solved by user awareness alone. Strict financial dual-custody controls, out-of-band verification, and OAuth app governance are required to protect company treasury."
    }
}

# Chapter 5: The Shadow AI Data Leak
ch5 = {
    "id": "shadow-ai-leak",
    "chapter": 5,
    "title": "The Shadow AI Data Leak",
    "subtitle": "Confidential Patient Data in Public LLMs",
    "category": "AI Governance & Healthcare Privacy",
    "compliance_framework": "HIPAA Security Rule / ISO 42001 (AIMS) / SOC 2 Privacy Criteria",
    "badge": "badge_soc2",
    "difficulty": "Expert",
    "summary": "Product engineers secretly connected a public generative AI endpoint to summarize hospital patient consultations. Proprietary patient data begins leaking in public model outputs.",
    "briefing": {
        "context": "SnoozeCloud recently signed a major pilot contract with a regional healthcare network to process patient intake forms. In a push to launch an AI summarization feature ahead of schedule, the growth engineering team secretly piped live patient intake notes—including medical histories and Social Security numbers—into a consumer LLM API ('QuickSummarize AI') using a personal credit card. A security researcher contacts you: confidential patient medical diagnoses are appearing in the public completions of QuickSummarize's model because the vendor trains directly on free API prompts!",
        "urgency": "CRITICAL (HIPAA & Privacy Violation)",
        "companion_intro": "Sweet mother of catnip! Shadow AI has struck our production pipeline! The growth team sent actual patient medical records into an unvetted LLM that trains on prompt data. We are facing catastrophic HIPAA penalties and immediate contract termination if we don't execute strict AI governance right now!",
        "initial_state": {
            "audit_readiness": 60,
            "company_trust": 70,
            "budget": 95000
        }
    },
    "phases": {
        "phase_1": {
            "phase_id": "phase_1",
            "title": "Phase 1: API Gateway Egress Lockdown",
            "story": "Live consultation notes are still streaming to QuickSummarize AI's public endpoint. The hospital's CISO is requesting a scheduled security sync tomorrow morning. What is your immediate containment action?",
            "companion_tip": "Sever the API connection at the proxy/gateway level immediately. Stop the data outflow before drafting remediation notices.",
            "companion_mood": "alert",
            "choices": [
                {
                    "id": "block_egress_and_rotate",
                    "title": "Deploy API Gateway Egress Block & Revoke Rogue LLM Key",
                    "description": "Block all outbound network traffic to QuickSummarize AI in your API Gateway, flush pending queue buffers, and revoke the rogue developer API token.",
                    "type": "good",
                    "effects": {
                        "audit_readiness": 15,
                        "company_trust": 10,
                        "budget": -3000
                    },
                    "consequence": "The data outflow is completely halted in under 90 seconds. Zero further patient consultation notes leave SnoozeCloud's encrypted boundary.",
                    "companion_reaction": "Sharp claws, clean severance! Halting the egress pipeline at the network layer saved thousands of patients from unauthorized exposure.",
                    "companion_mood": "happy",
                    "next_phase_id": "phase_2"
                },
                {
                    "id": "threaten_ai_vendor_lawsuit",
                    "title": "Spend 8 Hours Drafting Threatening Legal Letters to the AI Vendor",
                    "description": "Wait for Corporate Counsel to review demand letters while leaving the production API integration streaming data live.",
                    "type": "bad",
                    "effects": {
                        "audit_readiness": -30,
                        "company_trust": -30,
                        "budget": -35000
                    },
                    "consequence": "A regulatory nightmare! Over the 8 hours, 3,200 additional patient records were sent to the AI vendor. The regional healthcare network discovers the leak and files a formal HIPAA violation notice!",
                    "companion_reaction": "Barnaby gasps in horror! You cannot litigate an active leak! Technical containment must always happen before legal drafting!",
                    "companion_mood": "alert",
                    "remediation": {
                        "trigger_reason": "Failure to sever active HIPAA data leakage before pursuing legal avenues.",
                        "situation": "Thousands of patient records were ingested into the model. Healthcare network triggers a Sev-0 audit inquiry.",
                        "remediation_choices": [
                            {
                                "id": "rem_retain_hipaa_counsel",
                                "title": "Retain Specialized HIPAA Counsel & Formal OCR Breach Notification",
                                "description": "Retain healthcare privacy legal specialists ($22,000), execute formal OCR self-disclosure, and offer credit monitoring to impacted patients.",
                                "effects": {
                                    "audit_readiness": 10,
                                    "company_trust": -5,
                                    "budget": -22000
                                },
                                "consequence": "The Office for Civil Rights (OCR) notes your comprehensive self-reporting and corrective action, downgrading penalties to a resolution agreement.",
                                "companion_reaction": "A narrow escape from maximum tier civil monetary penalties. Now let's fix the AI pipeline permanently.",
                                "companion_mood": "detective",
                                "next_phase_id": "phase_2"
                            }
                        ]
                    }
                }
            ]
        },
        "phase_2": {
            "phase_id": "phase_2",
            "title": "Phase 2: Model Weights & Zero-Retention DPA",
            "story": "The connection is blocked, but patient data remains cached in QuickSummarize's training buffer. You need legal and technical guarantees that SnoozeCloud patient data is scrubbed from the vendor's infrastructure.",
            "companion_tip": "Under HIPAA and ISO 42001, you must require written certification of data purge and execute an Enterprise Business Associate Agreement (BAA) with Zero Data Retention.",
            "companion_mood": "detective",
            "choices": [
                {
                    "id": "secure_purge_and_enterprise_baa",
                    "title": "Obtain Certified Data Purge & Sign Enterprise BAA with Zero Retention",
                    "description": "Require QuickSummarize's leadership to execute a cryptographic data purge of training buffers and sign an Enterprise Business Associate Agreement guaranteeing zero data retention.",
                    "type": "good",
                    "effects": {
                        "audit_readiness": 15,
                        "company_trust": 15,
                        "budget": -6000
                    },
                    "consequence": "The vendor signs the HIPAA BAA and provides third-party verification that the training buffer was securely overwritten. The healthcare network partner is reassured by your rigorous remediation.",
                    "companion_reaction": "Superb contract governance! Turning a rogue tool into a legally bound, zero-retention enterprise integration is masterclass GRC.",
                    "companion_mood": "happy",
                    "next_phase_id": "phase_3"
                },
                {
                    "id": "trust_vendor_tweet",
                    "title": "Trust an Informal Email from Support saying 'It's Probably Deleted'",
                    "description": "Accept a brief informal email from a support rep without signing a formal Business Associate Agreement.",
                    "type": "risky",
                    "effects": {
                        "audit_readiness": -15,
                        "company_trust": -10,
                        "budget": 0
                    },
                    "consequence": "During the annual audit, Margaret asks for the signed BAA and data deletion certificate. You have nothing to show, resulting in a formal HIPAA non-compliance finding.",
                    "companion_reaction": "Informal support emails are not compliance evidence! HIPAA requires signed Business Associate Agreements (BAAs) with explicit breach notification clauses.",
                    "companion_mood": "alert",
                    "next_phase_id": "phase_3"
                }
            ]
        },
        "phase_3": {
            "phase_id": "phase_3",
            "title": "Phase 3: The Enterprise AI Gateway (ISO 42001)",
            "story": "The Board acknowledges that AI summarization is vital for product success, but demands institutional guardrails so sensitive patient data can never be leaked again. How do you govern generative AI?",
            "companion_tip": "Don't ban AI; build an internal AI Privacy Proxy with automated regex PII masking and synthetic tokenization.",
            "companion_mood": "happy",
            "choices": [
                {
                    "id": "deploy_ai_privacy_proxy",
                    "title": "Deploy Internal AI Privacy Gateway with Automated PII Masking",
                    "description": "Implement an internal AI Gateway that enforces automated regex tokenization, strips healthcare identifiers (ePHI) prior to egress, and logs all AI queries for auditability.",
                    "type": "good",
                    "effects": {
                        "audit_readiness": 20,
                        "company_trust": 15,
                        "budget": -5000
                    },
                    "consequence": "Engineering loves the low-latency internal AI gateway, and the Healthcare CISO endorses SnoozeCloud as an industry benchmark for secure healthcare AI adoption!",
                    "companion_reaction": "Barnaby is purring contentedly! Automated PII masking with synthetic tokens is the gold standard of AI Governance (ISO 42001). Brilliant work, Risk Manager!",
                    "companion_mood": "happy",
                    "next_phase_id": "conclusion"
                },
                {
                    "id": "blanket_ban_on_ai",
                    "title": "Issue a Blanket Corporate Ban on All AI Tools",
                    "description": "Send an executive memo forbidding any engineer or product manager from ever using AI.",
                    "type": "risky",
                    "effects": {
                        "audit_readiness": 0,
                        "company_trust": -25,
                        "budget": -2000
                    },
                    "consequence": "Product velocity collapses. Competitors surpass SnoozeCloud, while engineers quietly route around the ban using their personal smartphones.",
                    "companion_reaction": "Banning technology never works! Paved roads, automated sanitization, and enterprise BAAs are the only sustainable path forward.",
                    "companion_mood": "detective",
                    "next_phase_id": "conclusion"
                }
            ]
        }
    },
    "conclusion": {
        "success_threshold": {
            "audit_readiness": 75,
            "company_trust": 65,
            "budget": 35000
        },
        "takeaway": "Real GRC Lesson: Generative AI cannot be governed by draconian bans. Sustainable AI Governance (ISO 42001 / HIPAA) requires internal proxy gateways with automated PII masking, tokenization, and enterprise Zero Data Retention agreements."
    }
}

scenarios.append(ch4)
scenarios.append(ch5)
data["scenarios"] = scenarios

with open("scenarios.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"Successfully updated scenarios.json! Total scenarios now: {len(scenarios)}")
