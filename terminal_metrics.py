"""Evidence-derived counters, not a readiness estimator or live chat subscription."""
from collections import Counter
from terminal_control import tasks_from_state


def metrics(state):
    tasks = list(tasks_from_state(state).values())
    total = sum(len(t['acceptance']) for t in tasks)
    results = Counter(r['result'] for t in tasks for r in t['acceptance_results'])
    imports = {e.get('session_id') for e in state.get('events', [])
               if e.get('event_type') == 'message_record' and e.get('session_id')}
    catalog = {}
    for e in state.get('events', []):
        if e.get('event_type') == 'integration_observation':
            p = e.get('integration', {})
            if p.get('id') and p.get('kind') in ('repository', 'dependency', 'plugin', 'skill'):
                catalog[p['id']] = dict(p, event_id=e['event_id'],
                    evidence_status=e.get('evidence_status','unknown'),
                    source_ids=e.get('source_ids',[]), observed_at=e.get('observed_at'))
    return {'project_percent': None,
        'criteria': {'total':total, 'reported_pass':results['pass'],
                     'reported_fail':results['fail'],
                     'not_run':total-results['pass']-results['fail'], 'accepted':0},
        'plans': dict(Counter(p.get('status','unknown') for p in state.get('plans',[]))),
        'integrations':list(catalog.values()),
        'chat': {'status':'not_connected', 'transport':'none',
                 'imported_sessions':len(imports),
                 'message_observations':sum(e.get('event_type')=='message_record' for e in state.get('events',[])),
                 'detail':'Импорт и MCP не являются подпиской на текущий ChatGPT-чат. Полнота неизвестна.'}}
