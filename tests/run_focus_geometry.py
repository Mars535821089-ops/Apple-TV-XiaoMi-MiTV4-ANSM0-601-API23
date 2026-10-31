"""Run actual pure Java geometry and probe-state tests; no Android input."""
import argparse
from pathlib import Path
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from build import artifact


def run(java):
    lock=json.loads((ROOT/'dependencies.lock.json').read_text())
    ecj=artifact(lock['ecj'],ROOT/'build/deps',None,True)
    classes=ROOT/'build/focus-host-tests';classes.mkdir(parents=True,exist_ok=True)
    sources=[*sorted((ROOT/'src/carcast/java').rglob('*.java')),
             ROOT/'tests/fakes/ai/rplay/carcast/CnProbeHost.java',
             ROOT/'tests/java/FocusGeometryTest.java',ROOT/'tests/java/FocusProbeTest.java',
             ROOT/'tests/java/SpatialPathTest.java',ROOT/'tests/java/SpatialNavigatorTest.java']
    subprocess.run([java,'-jar',str(ecj),'-1.8','-proc:none','-g:none','-d',str(classes),*map(str,sources)],check=True)
    for name in ('FocusGeometryTest','FocusProbeTest','SpatialPathTest','SpatialNavigatorTest'):
        subprocess.run([java,'-cp',str(classes),name],check=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--java',required=True)
    run(p.parse_args().java)
