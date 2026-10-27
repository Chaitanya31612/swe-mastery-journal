"""Score saved synthetic decisions. No model calls and no semantic truth claims."""
import argparse,json
from pathlib import Path

def records(path):
    rows=[json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]
    if any(not isinstance(r,dict) or not isinstance(r.get('case_id'),str) for r in rows):
        raise ValueError('Every row needs a case_id')
    if len({r['case_id'] for r in rows})!=len(rows):
        raise ValueError('Duplicate case ID')
    return {r['case_id']:r for r in rows}

def score(cases,predictions):
    if not cases:
        raise ValueError('At least one evaluation case is required')
    if set(cases)!=set(predictions):
        raise ValueError('Prediction IDs must match all evaluation cases exactly')
    wrong=[key for key,row in cases.items() if predictions[key].get('state')!=row['expected_state']]
    critical=[key for key in wrong if cases[key]['critical']]
    return {'correct':len(cases)-len(wrong),'total':len(cases),'wrong_cases':wrong,
            'critical_decision_failures':critical,
            'decision_gate':'hold' if critical or wrong else 'contract_check_passed'}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('predictions');parser.add_argument('--cases',default=str(Path(__file__).with_name('cases.jsonl')))
    args=parser.parse_args()
    print(json.dumps(score(records(args.cases),records(args.predictions)),indent=2))
