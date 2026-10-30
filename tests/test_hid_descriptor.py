import importlib.util
from pathlib import Path
import unittest

SPEC = importlib.util.spec_from_file_location('hid_inspector', Path(__file__).parents[1] / 'experiments/hid_descriptor.py')
hid = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(hid)


class DescriptorInspectionTests(unittest.TestCase):
    def test_three_button_mouse_padding_and_signed_axes(self):
        descriptor = bytes.fromhex('05010902a1010901a100050919012903150025017501950381029501750581010501093009311581257f750895028106c0c0')
        bits, fields = hid.input_fields(descriptor)
        self.assertEqual(bits, 24)
        self.assertEqual(fields[:3], [(n, 1, (9, n + 1), 2, 0, 1) for n in range(3)])
        self.assertEqual(fields[3], (3, 5, None, 1, 0, 1))
        self.assertEqual(fields[4:], [(8, 8, (1, 48), 6, -127, 127),
                                     (16, 8, (1, 49), 6, -127, 127)])

    def test_global_push_pop_restores_page_and_report_dimensions(self):
        bits, fields = hid.input_fields(bytes.fromhex('050175089501a4050c75109502b409308102'))
        self.assertEqual(bits, 8)
        self.assertEqual(fields[0][:3], (0, 8, (1, 48)))

    def test_unsupported_or_truncated_descriptor_is_rejected(self):
        for descriptor in (b'\x75', bytes.fromhex('8501'), bytes.fromhex('fe00')):
            with self.subTest(descriptor=descriptor), self.assertRaises(ValueError):
                hid.input_fields(descriptor)


if __name__ == '__main__':
    unittest.main()
