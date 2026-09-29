import unittest
import json
from app import app

class QuietAuditGameTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_get_scenarios(self):
        response = self.app.get('/api/scenarios')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('scenarios', data)
        self.assertEqual(len(data['scenarios']), 5)
        ids = [s['id'] for s in data['scenarios']]
        self.assertIn('midnight-hotfix', ids)
        self.assertIn('vendor-breach', ids)
        self.assertIn('ex-employee-access', ids)
        self.assertIn('boardroom-phish', ids)
        self.assertIn('shadow-ai-leak', ids)


    def test_get_scenario_details(self):
        response = self.app.get('/api/scenario/midnight-hotfix')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], 'midnight-hotfix')
        self.assertIn('phases', data)
        self.assertIn('phase_1', data['phases'])

    def test_good_action_flow(self):
        # Good choice in phase_1
        payload = {
            'scenario_id': 'midnight-hotfix',
            'current_phase_id': 'phase_1',
            'choice_id': 'lock_s3_block_public',
            'is_remediation': False,
            'current_state': {
                'audit_readiness': 65,
                'company_trust': 80,
                'budget': 75000
            }
        }
        response = self.app.post('/api/action', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['next_phase_id'], 'phase_2')
        self.assertFalse(data['triggers_remediation'])
        self.assertEqual(data['new_state']['audit_readiness'], 80) # 65 + 15

    def test_bad_action_triggers_remediation(self):
        # Bad choice in phase_1
        payload = {
            'scenario_id': 'midnight-hotfix',
            'current_phase_id': 'phase_1',
            'choice_id': 'delete_bucket_panicked',
            'is_remediation': False,
            'current_state': {
                'audit_readiness': 65,
                'company_trust': 80,
                'budget': 75000
            }
        }
        response = self.app.post('/api/action', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertTrue(data['triggers_remediation'])
        self.assertIsNotNone(data['remediation'])
        self.assertEqual(len(data['remediation']['remediation_choices']), 2)

        # Now test submitting the remediation choice
        rem_payload = {
            'scenario_id': 'midnight-hotfix',
            'current_phase_id': 'phase_1',
            'parent_choice_id': 'delete_bucket_panicked',
            'choice_id': 'rem_restore_and_log',
            'is_remediation': True,
            'current_state': data['new_state'] # 40, 50, 63000
        }
        rem_response = self.app.post('/api/action', data=json.dumps(rem_payload), content_type='application/json')
        self.assertEqual(rem_response.status_code, 200)
        rem_data = json.loads(rem_response.data)
        self.assertTrue(rem_data['success'])
        self.assertFalse(rem_data['triggers_remediation'])
        self.assertEqual(rem_data['next_phase_id'], 'phase_2')

    def test_conclusion_and_report_card(self):
        # Reaching conclusion
        payload = {
            'scenario_id': 'midnight-hotfix',
            'current_phase_id': 'phase_3',
            'choice_id': 'present_capa_and_guardrails',
            'is_remediation': False,
            'current_state': {
                'audit_readiness': 80,
                'company_trust': 85,
                'budget': 70000
            }
        }
        response = self.app.post('/api/action', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['is_conclusion'])
        self.assertIsNotNone(data['report_card'])
        self.assertIn(data['report_card']['grade'], ['A+', 'A', 'B'])

    def test_companion_hint_endpoint(self):
        res = self.app.get('/api/companion-hint?scenario_id=midnight-hotfix&phase_id=phase_1')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertIn('hint', data)
        self.assertTrue(len(data['hint']) > 10)

    def test_vendor_breach_scenario(self):
        # Test Chapter 2 vendor breach flow
        res = self.app.get('/api/scenario/vendor-breach')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['chapter'], 2)

        # Immediate killswitch action
        payload = {
            'scenario_id': 'vendor-breach',
            'current_phase_id': 'phase_1',
            'choice_id': 'immediate_killswitch',
            'is_remediation': False,
            'current_state': {
                'audit_readiness': 60,
                'company_trust': 75,
                'budget': 85000
            }
        }
        action_res = self.app.post('/api/action', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(action_res.status_code, 200)
        action_data = json.loads(action_res.data)
        self.assertEqual(action_data['next_phase_id'], 'phase_2')
        self.assertFalse(action_data['triggers_remediation'])

    def test_ex_employee_access_scenario(self):
        # Test Chapter 3 ex-employee access flow
        res = self.app.get('/api/scenario/ex-employee-access')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['chapter'], 3)

        payload = {
            'scenario_id': 'ex-employee-access',
            'current_phase_id': 'phase_1',
            'choice_id': 'atomic_deprovisioning',
            'is_remediation': False,
            'current_state': {
                'audit_readiness': 65,
                'company_trust': 80,
                'budget': 90000
            }
        }
        action_res = self.app.post('/api/action', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(action_res.status_code, 200)
        action_data = json.loads(action_res.data)
        self.assertEqual(action_data['next_phase_id'], 'phase_2')

    def test_boardroom_phish_scenario(self):
        res = self.app.get('/api/scenario/boardroom-phish')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['chapter'], 4)

        payload = {
            'scenario_id': 'boardroom-phish',
            'current_phase_id': 'phase_1',
            'choice_id': 'out_of_band_verification',
            'is_remediation': False,
            'current_state': {
                'audit_readiness': 65,
                'company_trust': 75,
                'budget': 85000
            }
        }
        action_res = self.app.post('/api/action', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(action_res.status_code, 200)
        action_data = json.loads(action_res.data)
        self.assertEqual(action_data['next_phase_id'], 'phase_2')

    def test_shadow_ai_leak_scenario(self):
        res = self.app.get('/api/scenario/shadow-ai-leak')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['chapter'], 5)

        payload = {
            'scenario_id': 'shadow-ai-leak',
            'current_phase_id': 'phase_1',
            'choice_id': 'block_egress_and_rotate',
            'is_remediation': False,
            'current_state': {
                'audit_readiness': 60,
                'company_trust': 70,
                'budget': 95000
            }
        }
        action_res = self.app.post('/api/action', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(action_res.status_code, 200)
        action_data = json.loads(action_res.data)
        self.assertEqual(action_data['next_phase_id'], 'phase_2')

    def test_error_handling_unknown_scenario(self):

        res = self.app.get('/api/scenario/unknown-scenario-xyz')
        self.assertEqual(res.status_code, 404)

        payload = {
            'scenario_id': 'non-existent',
            'current_phase_id': 'phase_1',
            'choice_id': 'does_not_matter'
        }
        action_res = self.app.post('/api/action', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(action_res.status_code, 404)

    def test_chat_with_barnaby(self):
        # Test greeting
        res = self.app.post('/api/chat', data=json.dumps({'message': 'hello Barnaby'}), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertIn('reply', data)
        self.assertIn(data['mood'], ['happy', 'alert', 'detective', 'neutral'])

        # Test SOC 2 knowledge
        soc_res = self.app.post('/api/chat', data=json.dumps({'message': 'What is SOC 2 Type II?'}), content_type='application/json')
        self.assertEqual(soc_res.status_code, 200)
        soc_data = json.loads(soc_res.data)
        self.assertTrue(soc_data['success'])
        self.assertIn('SOC 2', soc_data['reply'])

        # Test empty message
        empty_res = self.app.post('/api/chat', data=json.dumps({'message': ''}), content_type='application/json')
        self.assertEqual(empty_res.status_code, 400)

if __name__ == '__main__':
    unittest.main()


