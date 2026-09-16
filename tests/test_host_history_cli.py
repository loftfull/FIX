import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class HostHistoryCliTests(unittest.TestCase):
    def test_discover_history_cli_reports_bounded_sources(self):
        with tempfile.TemporaryDirectory() as td:
            home = Path(td); (home / '.codex' / 'sessions').mkdir(parents=True)
            proc = subprocess.run([sys.executable, str(ROOT / 'host_history_cli.py'), 'discover', '--home', str(home)], cwd=ROOT, text=True, capture_output=True)
            self.assertEqual(0, proc.returncode, proc.stderr)
            payload = json.loads(proc.stdout)
            self.assertTrue(payload['bounded']); self.assertEqual('candidate-discovery-only', payload['authority'])
            self.assertEqual('available', next(x for x in payload['sources'] if x['provider'] == 'codex')['status'])

    def test_history_search_cli_uses_discovered_adapter(self):
        with tempfile.TemporaryDirectory() as td:
            home = Path(td); session_dir = home / '.claude' / 'projects' / 'demo'; session_dir.mkdir(parents=True)
            (session_dir / 'session.jsonl').write_text(json.dumps({'sessionId':'claude-cli-1','cwd':'/repo/demo','message':{'role':'user','content':'repair payment flow'}}) + '\n', encoding='utf-8')
            proc = subprocess.run([sys.executable, str(ROOT / 'host_history_cli.py'), 'search', 'payment', '--home', str(home), '--scope', 'conversations'], cwd=ROOT, text=True, capture_output=True)
            self.assertEqual(0, proc.returncode, proc.stderr)
            payload = json.loads(proc.stdout)
            self.assertEqual(1, payload['count']); self.assertEqual('claude-cli-1', payload['results'][0]['session_id']); self.assertEqual('candidate-discovery-only', payload['authority'])

    def test_history_search_cli_fails_cleanly_when_no_source_available(self):
        with tempfile.TemporaryDirectory() as td:
            proc = subprocess.run([sys.executable, str(ROOT / 'host_history_cli.py'), 'search', 'anything', '--home', td], cwd=ROOT, text=True, capture_output=True)
            self.assertEqual(2, proc.returncode)
            self.assertEqual('NO_HISTORY_SOURCE', json.loads(proc.stdout)['error'])


if __name__ == '__main__':
    unittest.main()
