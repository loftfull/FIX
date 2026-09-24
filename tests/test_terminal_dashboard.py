import http.client
import json
import tempfile
import threading
import unittest
from pathlib import Path
from project_history_agent import empty_state
from project_history_journal import bootstrap_journal_from_state
from terminal_control import submit_contract
from terminal_dashboard import build_view, render_page, make_server


class TerminalDashboardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        state = empty_state('p', 'Проект', 'Наблюдение')
        bootstrap_journal_from_state(state, self.root/'PROJECT_HISTORY.events.jsonl')

    def tearDown(self):
        self.tmp.cleanup()

    def test_view_real_contract_and_empty_visuals(self):
        submit_contract(self.root, 'p', {'task_id':'t1','title':'Задача','purpose':'Проверка',
            'deliverables':['Отчёт'],'acceptance':['Unicode'],'constraints':[], 'stop_conditions':['Нет данных']})
        data = build_view(self.root, 'p')
        self.assertTrue(data['integrity']['ok'])
        self.assertEqual(data['tasks'][0]['purpose'], 'Проверка')
        self.assertEqual(data['tasks'][0]['status'], 'queued')
        self.assertEqual(data['visuals'], [])
        self.assertEqual(data['mode'], 'live')

    def test_snapshot_cannot_escape_script(self):
        data = build_view(self.root, 'p', mode='snapshot')
        data['project']['name'] = '</script><script>alert(1)</script>'
        html = render_page(data)
        self.assertNotIn('</script><script>alert', html)
        self.assertIn('\\u003c/script', html)
        self.assertIn('"mode": "snapshot"', html)

    def test_identity_and_tamper_fail_closed(self):
        with self.assertRaises(ValueError):
            build_view(self.root, 'other')
        path = self.root/'PROJECT_HISTORY.events.jsonl'
        path.write_text(path.read_text(encoding='utf-8').replace('Наблюдение','Подмена'), encoding='utf-8')
        with self.assertRaises(ValueError):
            build_view(self.root, 'p')

    def test_http_read_only_and_rebinding_guards(self):
        server = make_server(self.root,'p',port=0)
        thread = threading.Thread(target=server.serve_forever,daemon=True)
        thread.start()
        def req(path, method='GET', headers=None):
            conn = http.client.HTTPConnection('127.0.0.1',server.server_port,timeout=5)
            conn.request(method,path,headers=headers or {})
            r=conn.getresponse(); body=r.read(); result=(r.status,body,dict(r.getheaders())); conn.close(); return result
        try:
            status,body,headers=req('/api/state')
            self.assertEqual(status,200)
            self.assertEqual(json.loads(body)['project']['name'],'Проект')
            self.assertEqual(headers['Cache-Control'],'no-store')
            self.assertNotIn('Access-Control-Allow-Origin',headers)
            self.assertEqual(req('/')[0],200)
            self.assertEqual(req('/PROJECT_MEMORY.json')[0],404)
            self.assertEqual(req('/../../etc/passwd')[0],404)
            self.assertEqual(req('/api/state?root=elsewhere')[0],404)
            self.assertEqual(req('/api/state','POST')[0],405)
            self.assertEqual(req('/api/state',headers={'Host':'attacker.test'})[0],403)
            self.assertEqual(req('/api/state',headers={'Origin':'https://attacker.test'})[0],403)
            self.assertEqual(req('/api/state',headers={'Sec-Fetch-Site':'cross-site'})[0],403)
            p=self.root/'PROJECT_HISTORY.events.jsonl';p.write_text('broken',encoding='utf-8')
            self.assertEqual(req('/api/state')[0],503)
        finally:
            server.shutdown();server.server_close();thread.join(timeout=3)


if __name__ == '__main__':
    unittest.main()
