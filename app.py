import os
import json
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'quiet-audit-cozy-grc-secret-2026')

DATA_FILE = os.path.join(os.path.dirname(__file__), 'scenarios.json')

def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_scenario_by_id(scenario_id):
    data = load_data()
    for s in data.get('scenarios', []):
        if s['id'] == scenario_id:
            return s
    return None

def compute_grade(audit_readiness, company_trust, budget, threshold):
    """
    Computes letter grade and auditor verdict based on metrics and threshold.
    """
    min_audit = threshold.get('audit_readiness', 70)
    min_trust = threshold.get('company_trust', 60)
    min_budget = threshold.get('budget', 20000)

    score = (audit_readiness * 0.5) + (company_trust * 0.3) + (min(100, (budget / 75000) * 100) * 0.2)

    passed_all = (audit_readiness >= min_audit) and (company_trust >= min_trust) and (budget >= min_budget)

    if score >= 88 and passed_all:
        grade = "A+"
        verdict = "Clean Unqualified Opinion (Gold Standard)"
        badge_earned = "Clean SOC 2 Gold Stamp"
        feedback = "Exceptional GRC leadership! You contained risks promptly, preserved all forensic audit trails, maintained team psychological safety, and established automated preventive controls."
    elif score >= 78 and passed_all:
        grade = "A"
        verdict = "Unqualified Opinion (Satisfactory Compliance)"
        badge_earned = "Pragmatic Risk Defender"
        feedback = "Solid compliance performance! You navigated the crisis with clear operational judgment, contained technical fallout, and satisfied all Trust Services Criteria."
    elif score >= 65:
        grade = "B"
        verdict = "Qualified Opinion with Minor Observations"
        badge_earned = "Resilient Responder"
        feedback = "You survived the crisis and contained the worst damage, though some friction or remediation loops were triggered along the way. Management recommendations have been noted."
    elif score >= 50:
        grade = "C"
        verdict = "Adverse Finding with Significant Deficiencies"
        badge_earned = "Remediation Apprentice"
        feedback = "Multiple control breakdowns and remediation delays occurred. Significant findings noted for internal controls, though basic operational survival was achieved."
    else:
        grade = "F"
        verdict = "Disclaimer of Opinion (Critical Control Breakdown)"
        badge_earned = "Audit Emergency Responder"
        feedback = "Severe material weaknesses, destroyed logs, or catastrophic trust erosion. The audit committee has ordered an immediate external restructuring."

    return {
        "grade": grade,
        "score": round(score, 1),
        "verdict": verdict,
        "passed": passed_all,
        "badge_earned": badge_earned,
        "feedback": feedback
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/scenarios', methods=['GET'])
def get_scenarios():
    data = load_data()
    summary_list = []
    for s in data.get('scenarios', []):
        summary_list.append({
            'id': s['id'],
            'chapter': s.get('chapter', 1),
            'title': s['title'],
            'subtitle': s.get('subtitle', ''),
            'category': s.get('category', ''),
            'compliance_framework': s.get('compliance_framework', ''),
            'badge': s.get('badge', 'badge_soc2'),
            'difficulty': s.get('difficulty', 'Moderate'),
            'summary': s.get('summary', ''),
            'initial_state': s['briefing'].get('initial_state', {})
        })
    return jsonify({
        'metadata': data.get('metadata', {}),
        'scenarios': summary_list
    })

@app.route('/api/scenario/<scenario_id>', methods=['GET'])
def get_scenario(scenario_id):
    scenario = get_scenario_by_id(scenario_id)
    if not scenario:
        return jsonify({'error': 'Scenario not found'}), 404
    return jsonify(scenario)

@app.route('/api/action', methods=['POST'])
def handle_action():
    req = request.get_json(silent=True) or {}
    scenario_id = req.get('scenario_id')
    current_phase_id = req.get('current_phase_id')
    choice_id = req.get('choice_id')
    is_remediation = req.get('is_remediation', False)
    parent_choice_id = req.get('parent_choice_id')
    
    current_state = req.get('current_state', {
        'audit_readiness': 70,
        'company_trust': 70,
        'budget': 50000
      })

    scenario = get_scenario_by_id(scenario_id)
    if not scenario:
        return jsonify({'error': 'Scenario not found'}), 404

    phase = scenario.get('phases', {}).get(current_phase_id)
    if not phase:
        return jsonify({'error': f'Phase {current_phase_id} not found in scenario {scenario_id}'}), 400

    choice_obj = None
    triggers_remediation = False
    remediation_payload = None

    if is_remediation:
        # Match remediation choice from parent choice's remediation block
        parent_choice = None
        for c in phase.get('choices', []):
            if c['id'] == parent_choice_id:
                parent_choice = c
                break
        
        if not parent_choice or 'remediation' not in parent_choice:
            return jsonify({'error': 'Parent choice or remediation not found'}), 400

        for r_choice in parent_choice['remediation'].get('remediation_choices', []):
            if r_choice['id'] == choice_id:
                choice_obj = r_choice
                break

        if not choice_obj:
            return jsonify({'error': f'Remediation choice {choice_id} not found'}), 400

    else:
        # Match standard choice in phase
        for c in phase.get('choices', []):
            if c['id'] == choice_id:
                choice_obj = c
                break

        if not choice_obj:
            return jsonify({'error': f'Choice {choice_id} not found'}), 400

        # Check if choice triggers a Backlash / Remediation loop
        if choice_obj.get('type') == 'bad' and 'remediation' in choice_obj:
            triggers_remediation = True
            remediation_payload = {
                'parent_choice_id': choice_obj['id'],
                'trigger_reason': choice_obj['remediation'].get('trigger_reason', 'Compliance control failure.'),
                'situation': choice_obj['remediation'].get('situation', 'Urgent mitigation required.'),
                'remediation_choices': choice_obj['remediation'].get('remediation_choices', [])
            }

    # Apply metric effects
    effects = choice_obj.get('effects', {})
    new_audit = max(0, min(100, current_state.get('audit_readiness', 70) + effects.get('audit_readiness', 0)))
    new_trust = max(0, min(100, current_state.get('company_trust', 70) + effects.get('company_trust', 0)))
    new_budget = max(0, current_state.get('budget', 50000) + effects.get('budget', 0))

    new_state = {
        'audit_readiness': new_audit,
        'company_trust': new_trust,
        'budget': new_budget
    }

    deltas = {
        'audit_readiness': effects.get('audit_readiness', 0),
        'company_trust': effects.get('company_trust', 0),
        'budget': effects.get('budget', 0)
    }

    next_phase_id = choice_obj.get('next_phase_id')
    is_conclusion = (next_phase_id == 'conclusion')

    report_card = None
    if is_conclusion:
        threshold = scenario.get('conclusion', {}).get('success_threshold', {})
        report_card = compute_grade(new_audit, new_trust, new_budget, threshold)
        report_card['takeaway'] = scenario.get('conclusion', {}).get('takeaway', '')

    next_phase_data = None
    if not is_conclusion and not triggers_remediation and next_phase_id:
        next_phase_data = scenario.get('phases', {}).get(next_phase_id)

    return jsonify({
        'success': True,
        'choice_id': choice_id,
        'choice_title': choice_obj.get('title', ''),
        'consequence': choice_obj.get('consequence', ''),
        'companion_reaction': choice_obj.get('companion_reaction', ''),
        'companion_mood': choice_obj.get('companion_mood', 'neutral'),
        'new_state': new_state,
        'deltas': deltas,
        'triggers_remediation': triggers_remediation,
        'remediation': remediation_payload,
        'next_phase_id': next_phase_id,
        'next_phase_data': next_phase_data,
        'is_conclusion': is_conclusion,
        'report_card': report_card
    })

@app.route('/api/companion-hint', methods=['GET'])
def get_companion_hint():
    scenario_id = request.args.get('scenario_id')
    phase_id = request.args.get('phase_id')
    
    scenario = get_scenario_by_id(scenario_id)
    if not scenario:
        return jsonify({'hint': "Take a deep breath and review your risk framework! Barnaby is here."})

    phase = scenario.get('phases', {}).get(phase_id)
    if phase and 'companion_tip' in phase:
        return jsonify({
            'hint': phase['companion_tip'],
            'mood': phase.get('companion_mood', 'detective')
        })

    return jsonify({
        'hint': "When in doubt, apply Least Privilege, preserve audit logs, and maintain honest stakeholder communication!",
        'mood': 'happy'
    })

from barnaby_brain import generate_barnaby_reply

@app.route('/api/chat', methods=['POST'])
def chat_with_barnaby():
    req = request.get_json(silent=True) or {}
    message = req.get('message', '').strip()
    history = req.get('history', [])

    if not message:
        return jsonify({'error': 'Message cannot be empty'}), 400

    response = generate_barnaby_reply(message, history)
    return jsonify({
        'success': True,
        'reply': response['reply'],
        'mood': response['mood'],
        'suggested_followups': response.get('suggested_followups', [])
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5050))
    app.run(host='0.0.0.0', port=port, debug=True)


