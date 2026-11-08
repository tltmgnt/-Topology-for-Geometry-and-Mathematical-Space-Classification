"""Exercise the installed console entry point outside the source tree."""
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as folder:
    output = Path(folder)/'bundle'
    for command in (["geometry-topology", "analyze", str(ROOT/'examples/sphere.json'), "--requirements", str(ROOT/'examples/requirements.json'), "--output", str(output)],
                    ["geometry-topology", "verify", str(output)],
                    ["geometry-topology", "compare", str(output), str(output)]):
        result = subprocess.run(command,cwd=folder,text=True,capture_output=True,check=True)
        assert json.loads(result.stdout)['execution_authorized'] is False
print('Installed CLI analyze/verify/compare passed outside source tree')
