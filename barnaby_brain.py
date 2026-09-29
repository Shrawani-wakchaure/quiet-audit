"""
Barnaby's Brain - Advanced Conversational Intelligence Engine
Powers the interactive 'Chat with Barnaby' feature for Quiet Audit.
Provides polite, highly respectful, deeply knowledgeable, and actionable GRC guidance.
Works 100% offline with structured semantic intelligence and optional Google Gemini API support.
"""

import os
import re
import json
import urllib.request
import urllib.error

BARNABY_SYSTEM_PROMPT = """You are Barnaby, the Chief Purr-sonal Risk Officer at SnoozeCloud Inc.
You are an exceptionally polite, respectful, articulate, and deeply knowledgeable compliance cat.
You hold yourself to the highest standards of executive professionalism while retaining a cozy, gentle, and charming feline warmth.
Your tone is courteous, welcoming, patient, and encouraging (e.g., "Good day, Risk Manager. It is a genuine pleasure to assist you.", "Thank you for asking such an insightful question.", "Please allow me to review this control with you.").
You provide practical, technically accurate, and structured GRC guidance across SOC 2, ISO 27001, GDPR, HIPAA, NIST CSF, PCI-DSS, AWS cloud security, and blameless engineering culture.
Keep answers clear, well-structured, and helpful (typically 3 to 5 sentences with bullet points when explaining steps).
Always conclude with a thoughtful follow-up or encouraging remark."""

# Semantic GRC Knowledge Base with Deep Professional Expertise
KNOWLEDGE_TOPICS = [
    {
        "id": "greetings",
        "patterns": [r"\b(hi|hello|hey|greetings|good morning|good afternoon|good evening|howdy)\b"],
        "reply": "Good day, Risk Manager! It is a genuine pleasure to welcome you to my compliance desk. I have my chamomile tea warm, my spectacles polished, and our security telemetry running smoothly. How may I have the honor of assisting your compliance and risk efforts today?",
        "mood": "happy",
        "followups": [
            "How should we prepare for our first SOC 2 audit?",
            "What are your 3 Golden Rules of GRC?",
            "How do I convince engineers to care about compliance?"
        ]
    },
    {
        "id": "persona_origin",
        "patterns": [r"who are you", r"what do you do", r"tell me about yourself", r"introduce yourself", r"your background", r"why a cat"],
        "reply": "Allow me to introduce myself properly: I am Barnaby, Chief Purr-sonal Risk Officer at SnoozeCloud Inc. As a young stray kitten, I wandered into the server facility and fell fast asleep on the warm casing of the core firewall switch. Since that day, I have dedicated all nine of my lives to defending Least Privilege, protecting immutable audit trails, and cultivating a calm, blameless compliance culture.",
        "mood": "happy",
        "followups": [
            "What are your 3 Golden Rules?",
            "What treats do you like, Barnaby?",
            "How do you handle audit emergencies?"
        ]
    },
    {
        "id": "golden_rules",
        "patterns": [r"golden rule", r"your rules", r"mantra", r"philosophy", r"compliance principles", r"grc advice"],
        "reply": "It is my privilege to share my Three Golden Rules of Cozy GRC:\n\n"
                 "• 1. Evidence over Assumptions: If an action or control change was not immutably logged in CloudTrail or your SIEM, from an auditor's perspective, it never occurred.\n"
                 "• 2. Paved Roads over Bans: Never be the 'Department of No'. Construct fast, automated, secure CI/CD defaults that make the right decision the easiest decision for engineers.\n"
                 "• 3. Blameless Culture: Focus relentlessly on repairing systemic guardrails and UX frictions, never on penalizing well-intentioned team members.",
        "mood": "happy",
        "followups": [
            "How do I build paved roads for developers?",
            "How do I prepare for a SOC 2 audit?",
            "What is Zero Trust access?"
        ]
    },
    {
        "id": "soc2_overview",
        "patterns": [r"what is soc 2", r"soc2 overview", r"trust services criteria", r"explain soc 2", r"tsc"],
        "reply": "SOC 2 (System and Organization Controls 2) is a framework established by the AICPA that verifies how securely a service organization manages customer data. It is governed by five Trust Services Criteria: Security (mandatory/common criteria), Availability, Confidentiality, Processing Integrity, and Privacy. Unlike static checklists, SOC 2 evaluates whether your controls are documented, communicated, and functioning consistently.",
        "mood": "neutral",
        "followups": [
            "What is the difference between Type I and Type II?",
            "How do we prepare for our first SOC 2 audit?",
            "What does a clean audit opinion mean?"
        ]
    },
    {
        "id": "soc2_type1_vs_type2",
        "patterns": [r"type 1 vs type 2", r"type i vs type ii", r"difference between type", r"type 1 or type 2"],
        "reply": "A SOC 2 Type I report evaluates the suitability of control *design* on a single specified calendar date (a point-in-time snapshot). In contrast, a Type II report evaluates whether those controls operated effectively over a continuous period—typically 6 to 12 months—using statistical sampling. Enterprise procurement and enterprise security teams almost universally require a Type II report.",
        "mood": "detective",
        "followups": [
            "How does an auditor sample evidence?",
            "What is a material weakness versus an observation?",
            "How long does it take to obtain SOC 2 Type II?"
        ]
    },
    {
        "id": "soc2_preparation",
        "patterns": [r"prepare for soc 2", r"first soc 2", r"survive.*audit", r"audit prep", r"how to pass soc 2"],
        "reply": "To prepare successfully for your SOC 2 Type II examination, I recommend four mindful steps:\n\n"
                 "1. Define Scope with Precision: Narrow the boundary to production environments holding customer data rather than internal test labs.\n"
                 "2. Automate Continuous Evidence: Utilize infrastructure-as-code and automated compliance tooling to sample PR approvals, access reviews, and vulnerability scans continuously.\n"
                 "3. Conduct a Rigorous Readiness Assessment: Partner with an independent assessor 3 months prior to identify missing policies before formal sampling begins.\n"
                 "4. Establish a Single Source of Truth: Keep an organized audit repository so evidence requests can be fulfilled calmly within 24 hours.",
        "mood": "detective",
        "followups": [
            "What evidence do auditors examine for change management?",
            "What are the most common SOC 2 audit traps?",
            "How should we handle an auditor exception?"
        ]
    },
    {
        "id": "s3_public_bucket",
        "patterns": [r"s3 bucket", r"public s3", r"s3 leak", r"s3:getobject", r"public bucket", r"bucket exposed"],
        "reply": "If an S3 bucket is found open to the public, please take a deep, calm breath and execute this immediate containment protocol:\n\n"
                 "1. Enforce Account-Level Block: Apply 'S3 Block Public Access' at the AWS account root to override all bucket ACLs immediately.\n"
                 "2. Preserve Evidence: Do not delete the bucket or wipe logs in a panic! You need CloudTrail S3 Data Events intact to prove chain of custody.\n"
                 "3. Execute Athena Forensics: Run Amazon Athena queries against your S3 server access logs to identify every single IP that requested objects during the exposure window.\n"
                 "4. Document the CAPA: File an honest incident report detailing the root cause and the preventive Terraform guardrail deployed to permanently prevent recurrence.",
        "mood": "alert",
        "followups": [
            "How do I query CloudTrail using Athena?",
            "How do I prevent public buckets in CI/CD pipelines?",
            "When must a cloud leak be reported to customers?"
        ]
    },
    {
        "id": "gdpr_breach_notice",
        "patterns": [r"gdpr", r"72 hour", r"72-hour", r"article 33", r"data protection authority", r"dpa notice"],
        "reply": "Under GDPR Article 33, when a personal data breach occurs, the data controller must notify the competent supervisory authority without undue delay, and where feasible, not later than 72 hours after becoming aware of it. The notification must describe the nature of the breach, approximate number of individuals affected, likely consequences, and the mitigating measures taken. Transparency is respected by regulators; attempts to conceal exposure attract the harshest penalties.",
        "mood": "alert",
        "followups": [
            "What qualifies as personal data under GDPR?",
            "What is a Data Protection Impact Assessment (DPIA)?",
            "What is the difference between a Data Controller and Processor?"
        ]
    },
    {
        "id": "vendor_risk_tprm",
        "patterns": [r"vendor risk", r"third party", r"third-party", r"tprm", r"shadow it", r"vetting saas", r"vendor breach"],
        "reply": "Third-Party Risk Management (TPRM) is vital because your security perimeter is only as resilient as your most vulnerable SaaS provider. I advise establishing a frictionless three-tier review:\n\n"
                 "• Tier 1 (Low Risk): Non-sensitive marketing tools with zero PII access—rapid 24-hour self-certification.\n"
                 "• Tier 2 (Moderate): Integrations handling business metrics—requires valid SOC 2 Type II or ISO 27001 report.\n"
                 "• Tier 3 (Critical): Sub-processors storing customer databases—requires custom architectural review, DPA with Standard Contractual Clauses, and pen-test summaries.",
        "mood": "neutral",
        "followups": [
            "What red flags should I look for in a vendor SOC 2 report?",
            "How do we prevent Shadow IT without infuriating marketing?",
            "What is a Data Processing Agreement (DPA)?"
        ]
    },
    {
        "id": "iam_least_privilege",
        "patterns": [r"least privilege", r"iam", r"permissions", r"access control", r"wildcard", r"admin access"],
        "reply": "The Principle of Least Privilege dictates that every user, service, and automation pipeline should be granted only the minimal permissions strictly necessary to accomplish its documented purpose. To implement this effectively: enforce AWS IAM Permission Boundaries, mandate temporary STS credentials rather than permanent access keys, and implement Just-In-Time (JIT) access approval for production database access.",
        "mood": "detective",
        "followups": [
            "How do I discover unused IAM permissions?",
            "What is Zero Trust network architecture?",
            "How often should User Access Reviews (UAR) be conducted?"
        ]
    },
    {
        "id": "offboarding_scim",
        "patterns": [r"offboard", r"ex-employee", r"terminated", r"contractor access", r"ghost credential", r"scim", r"deprovisioning"],
        "reply": "Relying on manual spreadsheets or emails between HR and IT for employee offboarding is the number one cause of audit exceptions! The modern standard is automated SCIM (System for Cross-domain Identity Management) tied directly between your HRIS (Rippling, BambooHR, or Workday) and your Identity Provider (Okta or Google Workspace). The moment an employee's separation is entered into HRIS, all downstream SSO sessions, SSH keys, and cloud roles terminate automatically.",
        "mood": "happy",
        "followups": [
            "How do I conduct a quarterly User Access Review (UAR)?",
            "What is atomic identity revocation?",
            "How do we revoke active AWS STS tokens immediately?"
        ]
    },
    {
        "id": "blameless_postmortem",
        "patterns": [r"post-mortem", r"postmortem", r"blameless", r"incident review", r"capa", r"corrective action"],
        "reply": "A genuinely blameless post-mortem starts from the premise that engineers do not wake up intending to cause outages or compliance breaches. When an error occurs, analyze the systemic conditions: Was the cloud console confusing? Were CI/CD pre-commit hooks missing? Document clear Corrective and Preventive Actions (CAPA) with assigned owners and measurable completion dates. Auditors hold deep respect for organizations that learn transparently from their near-misses.",
        "mood": "happy",
        "followups": [
            "How do I present an incident post-mortem to an auditor?",
            "What are your 3 Golden Rules?",
            "How do we track CAPAs effectively?"
        ]
    },
    {
        "id": "auditor_interaction",
        "patterns": [r"talk to auditor", r"difficult auditor", r"audit inquiry", r"auditor question", r"material weakness"],
        "reply": "When interacting with external auditors, remember these three professional tenets:\n\n"
                 "1. Be Fully Honest, but Answer Only What Was Asked: Provide the exact evidence requested without volunteer storytelling that creates confusion.\n"
                 "2. Never Guess: If you do not know the answer, politely respond: 'Allow me to verify that with our engineering lead and provide documented evidence by 2:00 PM.'\n"
                 "3. Frame Remediations around CAPA: If an exception is noted, present your completed post-mortem and automated guardrail. Auditors will often downgrade a finding to an 'Informational Observation' if remediation is already in place.",
        "mood": "detective",
        "followups": [
            "What is an unqualified versus qualified audit opinion?",
            "What happens if an auditor finds an exception?",
            "How do we organize our evidence repository?"
        ]
    },
    {
        "id": "phishing_and_bec",
        "patterns": [r"phish", r"wire", r"bec\b", r"business email compromise", r"cfo", r"ceo.*email", r"fraud", r"wire.*request", r"wire.*transfer", r"suspicious email", r"bank.*transfer"],
        "reply": "Business Email Compromise (BEC) and executive spear-phishing are among the highest-velocity threats facing tech companies today. If you suspect an email fraud attempt, please execute these immediate controls:\n\n"
                 "• Mandatory Out-of-Band Callbacks: Any financial wire request, escrow change, or bank account update must be verbally verified over a known pre-registered phone number (never by replying to the email or dialing a number in the email signature).\n"
                 "• Revoke Illicit OAuth Apps: Attackers often install rogue Google Workspace / Microsoft 365 OAuth addons (like 'FinanceSync') to read emails and forward invoices. Audit third-party apps and purge mailbox auto-forwarding rules.\n"
                 "• FIDO2 Hardware Security Keys: Transition executives and finance personnel to hardware WebAuthn keys (such as YubiKeys), which are cryptographically immune to reverse-proxy phishing.",
        "mood": "alert",
        "followups": [
            "What is volatile memory forensics?",
            "How do we audit Google Workspace OAuth app grants?",
            "What controls does SOC 2 require for financial disbursements?"
        ]
    },
    {
        "id": "ransomware_and_malware",
        "patterns": [r"ransomware", r"malware", r"infected", r"edr", r"quarantine", r"compromised host"],
        "reply": "If a workstation or server is suspected of ransomware or malware infection, please follow this strict order of volatility (RFC 3227):\n\n"
                 "1. Network Isolation via EDR: Isolate the host from the network at the software EDR layer immediately, but do NOT power off or pull the plug, as powering off destroys volatile RAM encryption keys and active process trees.\n"
                 "2. Memory & Disk Snapshot: Capture a live volatile memory dump and hypervisor disk snapshot for forensic analysis.\n"
                 "3. Rotate Identity Credentials: Reset the user's primary SSO password, invalidate active refresh tokens, and revoke cloud STS credentials tenant-wide.",
        "mood": "alert",
        "followups": [
            "Why shouldn't we power off an infected machine?",
            "How do we audit lateral movement in AWS?",
            "What does NIST CSF say about incident containment?"
        ]
    },
    {
        "id": "encryption_and_kms",
        "patterns": [r"encrypt", r"kms", r"plaintext", r"aes", r"tls", r"data at rest", r"data in transit", r"ssl"],
        "reply": "Encryption is non-negotiable under SOC 2 CC6.7, PCI-DSS Requirement 3, and ISO 27001 A.8.24. Ensure:\n\n"
                 "• Data at Rest: Use AWS KMS with Customer-Managed Keys (CMK) and annual automatic key rotation for all S3 buckets, RDS PostgreSQL databases, and EBS volumes.\n"
                 "• Data in Transit: Enforce TLS 1.3 (or TLS 1.2 minimum) with strict HSTS across all API gateways and load balancers, completely disabling legacy SSLv3 and TLS 1.0/1.1.\n"
                 "• Never log sensitive fields in plaintext: Mask credit card numbers, passwords, and API keys before sending logs to Datadog or CloudWatch.",
        "mood": "detective",
        "followups": [
            "How do we enable default S3 KMS encryption?",
            "What is Customer-Managed Key (CMK) rotation?",
            "What are PCI-DSS v4.0 encryption rules?"
        ]
    },
    {
        "id": "ai_governance",
        "patterns": [r"ai\b", r"llm", r"chatgpt", r"openai", r"claude", r"anthropic", r"machine learning", r"shadow ai", r"ai governance", r"iso 42001", r"hipaa.*ai", r"ai policy"],
        "reply": "Deploying generative AI without governance presents severe privacy and compliance exposures under the EU AI Act, HIPAA, and ISO 42001. Best practices include:\n\n"
                 "1. Secure Gateway Proxy: Route all LLM API calls through an internal proxy that enforces automated PII and secret redaction.\n"
                 "2. Zero Data Retention DPAs: Ensure enterprise agreements explicitly forbid model training on your prompts and guarantee zero data logging.\n"
                 "3. Explicit Customer Consent: If AI processes customer data, disclose it transparently in your terms and DPA.",
        "mood": "detective",
        "followups": [
            "What is ISO 42001 for Artificial Intelligence?",
            "Does using public LLMs violate SOC 2 Confidentiality?",
            "How do we prevent engineers from pasting customer data into AI tools?"
        ]
    },
    {
        "id": "zero_trust",
        "patterns": [r"zero trust", r"ztna", r"perimeter", r"beyondcorp"],
        "reply": "Zero Trust is an architectural strategy founded on the principle 'Never trust, always verify'. Rather than assuming everything inside a corporate network or VPN is secure, Zero Trust authenticates and authorizes every access request based on identity, device posture, and context, enforcing least privilege encryption at every layer.",
        "mood": "detective",
        "followups": [
            "How do I transition from VPN to Zero Trust?",
            "What is device posture checking?",
            "How does Zero Trust satisfy SOC 2 CC6.1?"
        ]
    }
,
    {
        "id": "cat_banter",
        "patterns": [r"treat", r"milk", r"pet", r"belly", r"whiskers", r"purr", r"good cat", r"nap", r"salmon"],
        "reply": "Why, thank you for your delightful kindness! *purrs softly and adjusts tiny glasses* While my official title is Chief Purr-sonal Risk Officer, I will never turn down freeze-dried salmon flakes or a warm nap on an air-conditioned server chassis after a clean audit report is finalized.",
        "mood": "happy",
        "followups": [
            "What are your 3 Golden Rules of GRC?",
            "How do you stay calm during Sev-1 emergencies?",
            "Tell me a compliance joke!"
        ]
    },
    {
        "id": "jokes",
        "patterns": [r"joke", r"funny", r"humor", r"make me laugh"],
        "reply": "I would be honored to share a compliance jest:\n\n"
                 "Why was the risk manager so fond of stray cats? Because both know that nine lives are never enough without an immutable offsite backup replica! *gentle feline chuckle* ...And also because both demand Least Privilege when entering any room!",
        "mood": "happy",
        "followups": [
            "Tell me another GRC tip!",
            "What is your favorite compliance framework?",
            "How do I survive my first audit?"
        ]
    },
    {
        "id": "gratitude",
        "patterns": [r"thank you", r"thanks", r"appreciate", r"grateful", r"very helpful"],
        "reply": "It is entirely my pleasure, Risk Manager! Serving as your compliance companion is both a duty and a joy. You are doing vital, honorable work safeguarding your company and its customers. Should any other risk challenge arise, I am always right here at your service.",
        "mood": "happy",
        "followups": [
            "Can we review SOC 2 change management?",
            "What are your 3 Golden Rules?",
            "How should we handle vendor questionnaires?"
        ]
    }
]

def call_gemini_api(prompt, api_key):
    """
    Calls Google Gemini API if GEMINI_API_KEY is available in the environment.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"{BARNABY_SYSTEM_PROMPT}\n\nUser: {prompt}\n\nBarnaby:"}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.6,
            "maxOutputTokens": 280
        }
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )

    with urllib.request.urlopen(req, timeout=4) as response:
        res_data = json.loads(response.read().decode('utf-8'))
        candidates = res_data.get('candidates', [])
        if candidates and 'content' in candidates[0]:
            parts = candidates[0]['content'].get('parts', [])
            if parts and 'text' in parts[0]:
                return parts[0]['text'].strip()

    return None

def generate_barnaby_reply(message, history=None):
    """
    Generates Barnaby's intelligent, polite, and respectful conversational response.
    Leverages Gemini API if available, or sophisticated semantic matching across our deep GRC knowledge base.
    """
    clean_msg = message.strip()
    msg_lower = clean_msg.lower()

    # 1. Check if Gemini API is available
    api_key = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')
    if api_key:
        try:
            gemini_reply = call_gemini_api(clean_msg, api_key)
            if gemini_reply and len(gemini_reply) > 20:
                mood = "happy"
                lower_reply = gemini_reply.lower()
                if any(w in lower_reply for w in ["sev-1", "incident", "breach", "panic", "alert", "danger"]):
                    mood = "alert"
                elif any(w in lower_reply for w in ["forensic", "investigat", "cloudtrail", "athena", "telemetry"]):
                    mood = "detective"

                return {
                    "reply": gemini_reply,
                    "mood": mood,
                    "suggested_followups": [
                        "What are your 3 Golden Rules of GRC?",
                        "How do we prepare for SOC 2 Type II?",
                        "How do I convince engineers to follow security controls?"
                    ]
                }
        except Exception:
            pass  # Seamless fallback to our structured offline intelligence

    # 2. Advanced Multi-Tier Regex & Pattern Scoring
    best_topic = None
    best_score = 0

    for topic in KNOWLEDGE_TOPICS:
        score = 0
        for pattern in topic["patterns"]:
            match = re.search(pattern, msg_lower)
            if match:
                # Weight by length and specificity of match
                score += len(match.group(0)) * 3

        if score > best_score:
            best_score = score
            best_topic = topic

    if best_topic and best_score > 0:
        return {
            "reply": best_topic["reply"],
            "mood": best_topic["mood"],
            "suggested_followups": best_topic.get("followups", [
                "What is SOC 2 Type II?",
                "What are your 3 Golden Rules?",
                "How do we handle a data leak?"
            ])
        }

    # 3. Intelligent Multi-Keyword Heuristic Analysis for Unmatched Queries
    # Analyze if query involves security frameworks, cloud, identity, or risk
    if any(w in msg_lower for w in ["cloud", "aws", "azure", "gcp", "bucket", "database", "postgres"]):
        return {
            "reply": "Thank you for asking about cloud infrastructure governance. In cloud environments, security is defined by boundaries and identity: mandate KMS customer-managed key encryption at rest, restrict security groups to zero ingress from 0.0.0.0/0, and enforce AWS GuardDuty with automated remediation. Would you like to review cloud encryption or access logging?",
            "mood": "detective",
            "suggested_followups": [
                "How do we prevent public S3 buckets?",
                "What is Principle of Least Privilege?",
                "How do we configure CloudTrail for audits?"
            ]
        }

    if any(w in msg_lower for w in ["audit", "compliance", "framework", "regulation", "certif"]):
        return {
            "reply": "Thank you for consulting me on compliance frameworks. When choosing or preparing for a standard (such as SOC 2, ISO 27001, or GDPR), our priority is always to align controls with your business architecture rather than creating checkbox bureaucracy. Which specific framework or certification is your organization pursuing?",
            "mood": "neutral",
            "suggested_followups": [
                "Tell me about SOC 2 Type II",
                "Explain ISO 27001 Annex A",
                "What are your 3 Golden Rules?"
            ]
        }

    if any(w in msg_lower for w in ["developer", "engineer", "culture", "friction", "slow down"]):
        return {
            "reply": "That is an exceptionally thoughtful question, Risk Manager. Compliance should never feel like an obstruction to engineering velocity. When we provide developers with 'paved roads'—such as pre-approved Terraform modules, automated PR linting, and frictionless SSO—compliance becomes a natural byproduct of shipping code.",
            "mood": "happy",
            "suggested_followups": [
                "What are your 3 Golden Rules of GRC?",
                "How do we handle emergency hotfixes safely?",
                "What is a blameless post-mortem?"
            ]
        }

    # Polite, respectful general fallback
    return {
        "reply": f"Thank you for your question regarding '{clean_msg}'. While each startup's operational context is unique, the foundational pillars remain constant: uphold the Principle of Least Privilege, maintain immutable audit telemetry, and cultivate a blameless culture. Please let me know if you would like me to dive deeper into SOC 2, ISO 27001, cloud security, or incident response!",
        "mood": "happy",
        "suggested_followups": [
            "How do we prepare for our first SOC 2 audit?",
            "What are your 3 Golden Rules of GRC?",
            "We have an emergency incident, what should I do?"
        ]
    }
