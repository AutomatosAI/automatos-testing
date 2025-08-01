import json
import subprocess
import sys

def run_round7_analysis():
    print('🚀 ROUND 7 - API ANALYSIS RESULTS')
    print('=' * 50)
    
    # Get OpenAPI data
    try:
        result = subprocess.run(['curl', '-s', 'http://localhost:8000/openapi.json'], 
                              capture_output=True, text=True)
        openapi_data = json.loads(result.stdout)
        
        endpoints = []
        for path, methods in openapi_data.get('paths', {}).items():
            for method in methods.keys():
                endpoints.append(f'{method.upper()} {path}')
        
        print(f'📊 ENDPOINT DISCOVERY:')
        print(f'Total Endpoints: {len(endpoints)}')
        print(f'Growth from Round 6: +{len(endpoints) - 46} endpoints ({((len(endpoints) - 46) / 46 * 100):.1f}% increase)')
        
        # Categorize endpoints
        categories = {}
        for ep in endpoints:
            if '/api/' in ep:
                category = ep.split('/api/')[1].split('/')[0]
                categories[category] = categories.get(category, 0) + 1
        
        print(f'\n📋 Endpoint Categories:')
        for cat, count in sorted(categories.items()):
            print(f'  {cat}: {count} endpoints')
        
        # Find new skills/AI endpoints
        skills_endpoints = [ep for ep in endpoints if any(keyword in ep.lower() 
                           for keyword in ['skill', 'pattern', 'template', 'agent'])]
        print(f'\n🤖 Skills/AI Related Endpoints: {len(skills_endpoints)}')
        
        # Show some examples of new endpoints
        new_endpoint_examples = []
        for ep in endpoints:
            if any(keyword in ep for keyword in ['skills', 'patterns', 'templates', 'performance', 'statistics']):
                new_endpoint_examples.append(ep)
        
        if new_endpoint_examples:
            print(f'\n🆕 Example New Endpoints:')
            for i, ep in enumerate(new_endpoint_examples[:8]):
                print(f'  {i+1}. {ep}')
        
        # Quick functionality test
        print(f'\n🧪 QUICK FUNCTIONALITY TEST:')
        test_endpoints = [
            '/health',
            '/api/system/health', 
            '/api/agents/',
            '/api/agents/skills',
            '/api/workflows/active',
            '/api/context/stats'
        ]
        
        successful = 0
        for endpoint in test_endpoints:
            try:
                result = subprocess.run(['curl', '-s', '-w', '%{http_code}', 
                                       f'http://localhost:8000{endpoint}'], 
                                      capture_output=True, text=True, timeout=5)
                
                # Extract status code (last line)
                lines = result.stdout.strip().split('\n')
                status_code = lines[-1] if lines else '000'
                
                if status_code.isdigit() and int(status_code) < 400:
                    successful += 1
                    status = '✅'
                else:
                    status = '❌'
                
                print(f'{status} {endpoint} - HTTP {status_code}')
                
            except Exception as e:
                print(f'❌ {endpoint} - Error: {str(e)[:30]}')
        
        success_rate = (successful / len(test_endpoints)) * 100
        
        print(f'\n📊 ROUND 7 - SUMMARY:')
        print(f'Total Endpoints: {len(endpoints)} (+{len(endpoints) - 46} new)')
        print(f'Quick Test Success Rate: {success_rate:.1f}% ({successful}/{len(test_endpoints)})')
        print(f'API Status: {🟢 OPERATIONAL if successful > 3 else 🔴 ISSUES DETECTED}')
        
        return {
            'total_endpoints': len(endpoints),
            'new_endpoints': len(endpoints) - 46,
            'categories': categories,
            'skills_endpoints': len(skills_endpoints),
            'success_rate': success_rate
        }
        
    except Exception as e:
        print(f'❌ Error analyzing API: {e}')
        return None

if __name__ == '__main__':
    run_round7_analysis()
