import requests
import json

url = 'http://localhost:8000/api/marketmind/research'
query = 'Research the e-commerce retention marketing software market. Compare Klaviyo and Omnisend on pricing plans, free plan limits, SMS automation features, and target audience.'

print('[🚀] Executing Research Engine for Prompt...')
res = requests.post(url, json={'query': query})
data = res.json()

print('\n========================================')
print('RUN ID:', data.get('run_id'))
print('STATUS:', data.get('status'))
print('REPORT TITLE:', data.get('report', {}).get('title'))
print('========================================\n')

print('--- EXECUTIVE SUMMARY ---')
print(data.get('report', {}).get('executive_summary'))
print('\n--- MARKET OVERVIEW ---')
print(data.get('report', {}).get('market_overview'))

print('\n--- COMPETITOR COMPARISON MATRIX ---')
for comp in data.get('report', {}).get('competitor_analysis', []):
    print(f"* Company: {comp.get('company_name')}")
    print(f"  - Starting Price: {comp.get('starting_price')}")
    print(f"  - Free Plan Limits: {comp.get('free_plan')}")
    print(f"  - Target Audience: {comp.get('target_audience')}")
    print(f"  - Key / SMS Features: {comp.get('key_features')}")
    print(f"  - Limitations: {comp.get('limitations')}")
    print(f"  - Verified Source URLs: {comp.get('source_urls')}")
    print()

print('--- QUALITY AUDIT BREAKDOWN ---')
audit = data.get('quality_audit', {}) or data.get('report', {}).get('quality_audit', {})
print('Overall Score:', audit.get('overall_score'), '%')
print('Status:', audit.get('status'))
print('Passed:', audit.get('passed'))
print('Category Scores:', json.dumps(audit.get('category_scores'), indent=2))
print('Failed Checks:', audit.get('failed_checks'))
