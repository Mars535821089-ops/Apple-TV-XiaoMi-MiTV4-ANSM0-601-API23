import importlib.util
from pathlib import Path
import unittest

SPEC = importlib.util.spec_from_file_location('tv_monitor', Path(__file__).parents[1] / 'tools/monitor.py')
monitor = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(monitor)


class MonitorPrivacyTests(unittest.TestCase):
    def test_audio_parameter_is_kept_but_peer_addresses_are_removed(self):
        line = 'CarCast audioLatencyMs: 1000 peer=192.0.2.10 device=AA:BB:CC:DD:EE:FF'
        result = monitor.redact(line)
        self.assertIn('audioLatencyMs: 1000', result)
        self.assertNotIn('192.0.2.10', result)
        self.assertNotIn('AA:BB:CC:DD:EE:FF', result)

    def test_surface_detach_evidence_is_preserved_without_peer_identity(self):
        self.assertEqual(monitor.redact('CarCast slot 0: surface gone peer=192.0.2.10'),
                         'CarCast slot 0: surface gone peer=<address>')

    def test_secret_line_is_dropped_even_when_audio_keyword_matches(self):
        self.assertIsNone(monitor.redact('CarCast audioType: media passphrase=example-private-value'))

    def test_unrelated_protocol_payload_is_not_recorded(self):
        self.assertIsNone(monitor.redact('HTTP request body: arbitrary payload'))


if __name__ == '__main__':
    unittest.main()
