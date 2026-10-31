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

    def test_own_c_adapter_and_header_are_publishable_but_libraries_are_not(self):
        self.assertEqual(policy.inspect_entry('src/carcast/native/adapter.c',b'int result(void){return 0;}'),[])
        self.assertEqual(policy.inspect_entry('src/carcast/native/adapter.h',b'int result(void);'),[])
        self.assertTrue(policy.inspect_entry('src/carcast/native/libvendor.so',b'ELF'))

    def test_only_named_source_submodule_can_be_considered(self):
        commit = b'b8e12bcf0175c8e8f6ede546d92210ff8ce5841f'
        self.assertEqual(policy.inspect_entry('upstream/aerial-tv', commit, '160000'), [])
        self.assertTrue(policy.inspect_entry('upstream/unknown', commit, '160000'))


if __name__ == '__main__':
    unittest.main()
