"""The frame-age observer must not terminate a still-connected phone session.

A quiet UI or a lost TextureView callback is insufficient transport evidence.
This boundary check examines the complete production observer, including helpers,
so moving the disconnect into another method in that class cannot hide it.
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class FrameObserverSafetyTests(unittest.TestCase):
    def test_missing_texture_updates_alone_cannot_disconnect_the_phone(self):
        observer = (ROOT / 'src/carcast/smali/ai/rplay/carcast/CnRender.smali').read_text()
        calls = re.findall(r'invoke-\S+\s+\{[^}]*\},\s+(L[^;]+;)->(\w+)\(', observer)
        disconnects = [(owner, method) for owner, method in calls
                       if method == 'teardownSession' or owner.endswith('/CnReconnect;')]
        self.assertEqual(disconnects, [],
                         'Frame silence is an observation, not proof of a dead CarPlay transport')


if __name__ == '__main__':
    unittest.main()
