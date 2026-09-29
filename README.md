# 🌲 Quiet Audit — Where Calm Meets Compliance

> A narrative-driven GRC (Governance, Risk, and Compliance) crisis management web game featuring a **cozy, pixel-art, pastel aesthetic** and an adorable compliance companion character.

Inspired by the calm, grounding design of *"Quiet Place"* (`https://pin.it/6BQOHyegy`), **Quiet Audit** places you in the role of a GRC Risk Manager at a high-growth tech startup (*SnoozeCloud*). With your faithful companion **Barnaby the Cat (Chief Purr-sonal Risk Officer)** by your side, you must navigate live security crises under pressure, preserve immutable audit trails, protect corporate trust, and manage company budgets.

---

## ✨ Features & Highlights

- **Cozy, Pastel Aesthetic & Elevated Hero Scenery:** Soft mint/sage background canvas (`#d2e3dc`), warm cream/off-white content cards, elegant serif typography (`Playfair Display` & `Cinzel`), and gentle coral/salmon action buttons (`#e07a5f`). The pixel-art shoreline scenery is showcased right under the hero section matching the Pinterest reference image layout!
- **Interactive 1-on-1 "Chat with Barnaby" Console:** Have a live, real-time conversation with Barnaby about any GRC topic (SOC 2, ISO 27001, GDPR Art. 33, S3 containment, least privilege, vendor risk, blameless post-mortems, or cat treats!). Powered by a built-in offline GRC intelligence engine with dynamic emotion avatar updates, retro speech blips, quick prompt chips, and optional Google Gemini API support.
- **Dedicated Companion Introduction (Meet Barnaby):** Click *"Meet Barnaby 🐾"* to open an interactive character modal featuring Barnaby's backstory (*stray kitten curled on the firewall switch*), interactive mood/voice switcher (*Cozy & Happy*, *Sev-1 Panic*, *Log Detective*, *Policy Scholar*), and his 3 Golden Rules of GRC.
- **Mindful "About GRC" Section:** An interactive educational section explaining Governance, Risk, and Compliance for startups, along with a quick-reference guide for SOC 2 Type II, ISO 27001, GDPR Article 33, and NIST CSF.
- **Scroll-Driven Animations & Ambient Effects:** As you scroll, cards reveal with smooth fade-and-rise transitions using CSS View Timelines with `IntersectionObserver` fallback. Floating ambient mint leaves and sparkles drift gently across the background.
- **Real-Time Status Meters:** Live dynamic meters tracking **Audit Readiness %**, **Company Trust %**, and **Incident Budget ($)** with animated progress bars, color-coded health states, and floating change indicators (`+15%`, `-$3,000`).
- **Branching Engine & Remediation Loops:** Correct choices advance the incident smoothly. Risky or catastrophic blunders (e.g. deleting production buckets to hide evidence, sweeping breaches under the rug, or tipping off intruders) trigger a dedicated **Backlash / Remediation Loop** where you must contain the fallout before proceeding.
- **Web Audio API Sound Synthesizer:** Fully self-contained retro audio synthesis (Animal Crossing-style dialogue blips, soft click pops, harmonic success arpeggios, gentle retro alert chimes, and audit victory fanfare) with an in-navbar mute toggle.
- **Auditor Report Card & Badges:** Final examination review featuring letter grades (`A+`, `A`, `B`, `C`, `F`), official auditor verdicts from Senior Auditor Margaret, compliance badges (*Clean SOC 2 Gold Stamp*, *Pragmatic Risk Defender*), and real-world GRC takeaways.

---

## 📂 The 3 Included Crisis Scenarios

1. **Chapter 1: The Midnight Hotfix**
   - *Framework:* SOC 2 Type II (Trust Services Criteria CC6.1, CC6.6)
   - *Setting:* 11:42 PM on audit eve. Lead developer Dave applied a wildcard policy to an S3 bucket containing database backups and KYC docs.
   - *Key Concepts:* S3 Block Public Access, least privilege, CloudTrail data event logging via Amazon Athena, blameless post-mortems, and CAPA (Corrective and Preventive Action).

2. **Chapter 2: The Third-Party Vendor Breach**
   - *Framework:* ISO 27001:2022 (A.5.19 & A.5.20) / GDPR Art. 28 & 33
   - *Setting:* An unvetted marketing AI widget (*ClickPixie AI*) suffered a credential leak on GitHub. Attackers are probing customer endpoints while the 72-hour regulatory notification clock ticks.
   - *Key Concepts:* Shadow IT, CDN edge kill-switches, Data Protection Impact Assessments (DPIA), GDPR Article 33 disclosure windows, and automated TPRM (Third-Party Risk Management) workflows.

3. **Chapter 3: The Ex-Employee Access Loop**
   - *Framework:* SOC 2 CC6.2, CC6.3 / NIST CSF PR.AC-1
   - *Setting:* A star backend contractor finished their term two weeks ago, but HR forgot to notify IT. Active AWS STS assume-role calls are detected originating from Lisbon.
   - *Key Concepts:* Ghost credentials, atomic identity revocation across Okta and AWS IAM, forensic bastion host snapshots, and automated SCIM deprovisioning webhooks.

---

## 🛠️ Tech Stack & Architecture

- **Backend:** Python 3 (Flask) — stateless RESTful API handling action evaluation, metric clamping, remediation transitions, and grade calculations.
- **Frontend:** HTML5, CSS3, Vanilla JavaScript (ES6+) — zero heavy node frameworks, semantic `<dialog>` overlays, accessible buttons, and responsive layout.
- **Visuals:** Handcrafted SVG pixel-art sprites (`barnaby_*.svg`, `pixel_scenery.svg`, `badge_*.svg`) using crisp edges.
- **Data Storage:** `scenarios.json` — structured JSON schema defining scenarios, phases, choices, and remediation branches.

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- Flask (`pip install flask`)

### 2. Run the Application
From the project root:
```bash
python3 app.py
```
*(By default, the server runs on port 5050 to avoid macOS AirPlay Receiver port conflicts)*.

To specify a custom port:
```bash
PORT=8080 python3 app.py
```

### 3. Open in Browser
Visit:
```
http://127.0.0.1:5050
```

### 4. Run Unit Tests
To verify all scenario transitions, remediation loops, and grading calculations:
```bash
python3 -m unittest discover -s tests
```

---

## 📝 How to Add New Scenarios

All scenario content is stored in [`scenarios.json`](file:///scenarios.json). To add a new chapter (e.g. Chapter 4: *The Ransomware Phish* or *The Insider Trading Leak*), add a new object to the `"scenarios"` array:

```json
{
  "id": "ransomware-phish",
  "chapter": 4,
  "title": "The Phishing Hook",
  "subtitle": "Executive Spear-Phishing & Lateral Movement",
  "category": "Incident Response & Malware Defense",
  "compliance_framework": "NIST CSF RS.CO-1 / ISO 27001 A.5.24",
  "badge": "badge_incident",
  "difficulty": "Challenging",
  "summary": "The CFO clicked a malicious link mimicking docu-sign, executing an infostealer payload on the corporate network.",
  "briefing": {
    "context": "At 2:15 PM, Endpoint Detection & Response (EDR) raises an alert on the CFO's laptop...",
    "urgency": "CRITICAL (Sev-1)",
    "companion_intro": "Oh whiskers! The CFO thought they were reviewing executive compensation, but they just ran an obfuscated PowerShell macro!",
    "initial_state": {
      "audit_readiness": 65,
      "company_trust": 75,
      "budget": 80000
    }
  },
  "phases": {
    "phase_1": {
      "phase_id": "phase_1",
      "title": "Phase 1: Network Isolation",
      "story": "The infected machine is attempting ARP scans across the finance subnet. What is your containment move?",
      "companion_tip": "Isolate the host at the EDR layer immediately, but do not power it off so RAM forensic artifacts are preserved!",
      "companion_mood": "alert",
      "choices": [
        {
          "id": "edr_network_quarantine",
          "title": "Network-Isolate via EDR & Capture Memory Dump",
          "description": "Quarantine the host from the network while maintaining remote telemetry and taking a memory dump for analysis.",
          "type": "good",
          "effects": {
            "audit_readiness": 15,
            "company_trust": 10,
            "budget": -2000
          },
          "consequence": "Lateral movement blocked immediately! Volatile RAM artifacts saved.",
          "companion_reaction": "Purr-fect containment! Memory forensics will reveal the C2 server without letting the worm spread.",
          "companion_mood": "happy",
          "next_phase_id": "phase_2"
        },
        {
          "id": "unplug_and_ignore",
          "title": "Yank the Power Cable Out of the Wall",
          "description": "Run into the CFO's office and violently pull the power cord.",
          "type": "bad",
          "effects": {
            "audit_readiness": -20,
            "company_trust": -25,
            "budget": -5000
          },
          "consequence": "Powering off the machine wiped RAM, destroying the encryption key and malware process tree!",
          "companion_reaction": "MEOWWW! Powering off wipes the volatile RAM! Forensic memory analysis is now impossible!",
          "companion_mood": "alert",
          "remediation": {
            "trigger_reason": "Destruction of volatile forensic evidence (NIST SP 800-86 violation).",
            "situation": "You must reconstruct the attack chain from perimeter firewall logs instead.",
            "remediation_choices": [
              {
                "id": "rem_firewall_reconstruction",
                "title": "Query Zeek/Suricata IDS & Firewall NetFlow Logs",
                "description": "Reconstruct C2 beaconing using perimeter NetFlow telemetry.",
                "effects": {
                  "audit_readiness": 10,
                  "company_trust": 5,
                  "budget": -4000
                },
                "consequence": "The perimeter logs identified the C2 IP. Domain blocked company-wide.",
                "companion_reaction": "Good salvage job! IDS network logs saved the day.",
                "companion_mood": "detective",
                "next_phase_id": "phase_2"
              }
            ]
          }
        }
      ]
    }
  },
  "conclusion": {
    "success_threshold": {
      "audit_readiness": 75,
      "company_trust": 65,
      "budget": 30000
    },
    "takeaway": "Real GRC Lesson: Incident response requires preserving evidence in order of volatility (RFC 3227: Registers/Cache -> RAM -> Disk -> Remote Logs)."
  }
}
```

---

## 🎨 Asset Customization

- Companion SVG sprites are in `static/images/barnaby_*.svg`.
- Pixel scenery background is located at `static/images/pixel_scenery.svg`.
- The pixel art generator script is located at `generate_assets.py`. Run `python3 generate_assets.py` to regenerate or modify color palettes and sprite accessories.

---

## 📜 License
Educational MIT License. Built for security professionals, risk managers, and compliance enthusiasts who believe in calm, humane, blameless GRC culture.
