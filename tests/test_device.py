import importlib.util
from pathlib import Path
import tempfile
import json
import hashlib
import io
import contextlib
import subprocess
from zipfile import ZipFile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('tv_device', Path(__file__).parents[1] / 'tools/device.py')
device = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(device)


class TargetAndInstallTests(unittest.TestCase):
    def test_install_timeout_still_checks_device_before_reporting_failure(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            apk, receipt = root / 'candidate.apk', root / 'candidate.json'
            with ZipFile(apk, 'w') as archive:
                archive.writestr('lib/armeabi-v7a/libcarcast.so', b'test-library')
            receipt.write_text(json.dumps({'apk': apk.name, 'sha256': hashlib.sha256(apk.read_bytes()).hexdigest()}))
            arguments = ['device.py', '--serial', 'test-target', 'install', '--apk', str(apk), '--receipt', str(receipt)]
            with patch.object(device, 'TV') as factory, patch('sys.argv', arguments), contextlib.redirect_stdout(io.StringIO()):
                tv = factory.return_value
                tv.run.side_effect = [subprocess.TimeoutExpired(['adb'], 1),
                                      'package:/data/app/ai.rplay.carcast-1/base.apk',
                                      hashlib.md5(apk.read_bytes()).hexdigest() + '  installed.apk']
                timed_out = None
                try:
                    device.main()
                except subprocess.TimeoutExpired as error:
                    timed_out = error
                self.assertIsNone(timed_out, 'A client timeout must not hide a completed TV installation')
                self.assertEqual(sum(call.args[0] == 'install' for call in tv.run.call_args_list), 1)

    def test_other_device_is_rejected_before_mutation(self):
        tv = device.TV('test-target')
        with patch.object(tv, 'run', side_effect=['device', 'SomeOtherTV', '23', 'armeabi-v7a']):
            with self.assertRaisesRegex(RuntimeError, 'not the validated'):
                tv.identity()

    def test_verify_install_never_requests_an_install(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            apk, receipt = root / 'candidate.apk', root / 'candidate.json'
            with ZipFile(apk, 'w') as archive:
                archive.writestr('lib/armeabi-v7a/libcarcast.so', b'test-library')
            receipt.write_text(json.dumps({'apk': apk.name, 'sha256': hashlib.sha256(apk.read_bytes()).hexdigest()}))
            arguments = ['device.py', '--serial', 'test-target', 'verify-install', '--apk', str(apk), '--receipt', str(receipt)]
            with patch.object(device, 'TV') as factory, patch('sys.argv', arguments), contextlib.redirect_stdout(io.StringIO()) as output:
                tv = factory.return_value
                tv.run.side_effect = ['package:/data/app/ai.rplay.carcast-1/base.apk',
                                      hashlib.md5(apk.read_bytes()).hexdigest() + '  installed.apk']
                device.main()
                self.assertFalse(json.loads(output.getvalue())['install_requested'])
                self.assertTrue(all(call.args[0] == 'shell' for call in tv.run.call_args_list))

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
