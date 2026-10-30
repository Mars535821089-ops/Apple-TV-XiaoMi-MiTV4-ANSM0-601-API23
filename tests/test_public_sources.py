import importlib.util
from pathlib import Path
import unittest

SPEC = importlib.util.spec_from_file_location('source_policy', Path(__file__).parents[1] / 'tools/check_public_sources.py')
policy = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(policy)


class PublicSourceBoundaryTests(unittest.TestCase):
    def test_runtime_and_binary_payloads_cannot_be_published(self):
        self.assertTrue(policy.inspect_entry('local/runtime/upstream.apk', b'PK\0binary'))

    def test_actual_token_shape_is_rejected_without_echoing_value(self):
        data = ('sk-' + 'a' * 32).encode()
        issues = policy.inspect_entry('config.json', data)
        self.assertTrue(issues)
        self.assertNotIn(data.decode(), str(issues))

    def test_normal_helper_source_is_accepted(self):
        self.assertEqual(policy.inspect_entry('tools/example.py', b'print("ready")\n'), [])


if __name__ == '__main__':
    unittest.main()
