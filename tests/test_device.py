import importlib.util
from pathlib import Path
import tempfile
import json
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('tv_device', Path(__file__).parents[1] / 'tools/device.py')
device = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(device)


class TargetAndInstallTests(unittest.TestCase):
    def test_other_device_is_rejected_before_mutation(self):
        tv = device.TV('test-target')
        with patch.object(tv, 'run', side_effect=['device', 'SomeOtherTV', '23', 'armeabi-v7a']):
            with self.assertRaisesRegex(RuntimeError, 'not the validated'):
                tv.identity()

    def test_target_with_wrong_sdk_is_rejected(self):
        tv = device.TV('test-target')
        with patch.object(tv, 'run', side_effect=['device', 'MiTV4-ANSM0', '24', 'armeabi-v7a']):
            with self.assertRaises(RuntimeError):
                tv.identity()

    def test_modified_apk_is_rejected_before_installation(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            apk, receipt = root / 'candidate.apk', root / 'candidate.json'
            apk.write_bytes(b'changed')
            receipt.write_text(json.dumps({'apk': apk.name, 'sha256': '0' * 64}))
            with self.assertRaisesRegex(ValueError, 'does not match'):
                device.validate_install(apk, receipt)


if __name__ == '__main__':
    unittest.main()
