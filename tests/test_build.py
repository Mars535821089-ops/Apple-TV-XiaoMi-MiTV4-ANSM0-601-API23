import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest
import contextlib
import io
from unittest.mock import patch
from zipfile import ZipFile

SPEC = importlib.util.spec_from_file_location('source_build', Path(__file__).parents[1] / 'tools/build.py')
build = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(build)


class BuildBoundaryTests(unittest.TestCase):
    def test_probe_cannot_overwrite_the_baseline_label(self):
        with patch('sys.argv', ['build.py', '--input-probe', 'consumer-menu']), contextlib.redirect_stderr(io.StringIO()):
            with patch.object(build, 'artifact') as artifact:
                with self.assertRaises(SystemExit) as error:
                    build.main()
                self.assertEqual(error.exception.code, 2)
                artifact.assert_not_called()

    def test_memory_probe_rejects_default_before_accessing_dependencies(self):
        stderr=io.StringIO()
        with patch('sys.argv',['build.py','--memory-probe','ashmem']),contextlib.redirect_stderr(stderr):
            with patch.object(build,'artifact') as artifact:
                with self.assertRaises(SystemExit) as error:build.main()
                self.assertEqual(error.exception.code,2)
                artifact.assert_not_called()
        self.assertIn('Probes need a separate --label',stderr.getvalue())

    def test_poisoned_cache_is_not_silently_trusted(self):
        with tempfile.TemporaryDirectory() as folder:
            cache = Path(folder)
            (cache / 'upstream.apk').write_bytes(b'changed')
            spec = {'filename': 'upstream.apk', 'sha256': hashlib.sha256(b'original').hexdigest()}
            with self.assertRaisesRegex(ValueError, 'SHA256 mismatch'):
                build.artifact(spec, cache, None, True)

    def test_offline_missing_dependency_does_not_access_network(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(build.urllib.request, 'urlopen') as request:
            with self.assertRaises(FileNotFoundError):
                build.artifact({'filename': 'missing.jar'}, Path(folder), None, True)
            request.assert_not_called()

    def test_case_distinct_vendor_resources_must_both_survive(self):
        with tempfile.TemporaryDirectory() as folder:
            original, good, bad = [Path(folder) / name for name in ['original.apk', 'good.apk', 'bad.apk']]
            for path in [original, good]:
                with ZipFile(path, 'w') as archive:
                    archive.writestr('res/Dt.png', b'upper')
                    archive.writestr('res/dt.png', b'lower')
            with ZipFile(bad, 'w') as archive:
                archive.writestr('res/dt.png', b'lower')
            self.assertEqual(build.verify_resources(original, good), 2)
            with self.assertRaises((KeyError, ValueError)):
                build.verify_resources(original, bad)


if __name__ == '__main__':
    unittest.main()
