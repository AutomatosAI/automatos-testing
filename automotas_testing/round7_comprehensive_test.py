import httpx
import asyncio
import json
import time
from datetime import datetime

class Round7Tester:
    def __init__(self):
        self.base_url = 'http://localhost:8000'
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'round': 7,
            'total_endpoints': 0,
            'successful_tests': 0,
            'failed_tests': 0,
            'endpoints_tested': [],
            'performance_metrics': {},
            'new_endpoints_found': [],
            'comparison_with_round6': {}
        }
    
    async def discover_endpoints(self):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f'{self.base_url}/openapi.json')
                if response.status_code == 200:
                    openapi_data = response.json()
                    endpoints = []
                    for path, methods in openapi_data.get('paths', {}).items():
                        for method in methods.keys():
                            endpoints.append({
                                'method': method.upper(), 
                                'path': path,
                                'full_endpoint': f'{method.upper()} {path}'
                            })
                    return endpoints
                return []
            except Exception as e:
                print(f'Discovery error: {e}')
                return []
    
    async def test_endpoint(self, endpoint):
        async with httpx.AsyncClient() as client:
            method = endpoint['method']
            path = endpoint['path']
            url = f'{self.base_url}{path}'
            
            start_time = time.time()
            try:
                # Basic test data for POST/PUT requests
                test_data = {}
                if 'agent' in path.lower():
                    test_data = {'name': 'Test Agent', 'type': 'test', 'capabilities': ['testing']}
                elif 'workflow' in path.lower():
                    test_data = {'name': 'Test Workflow', 'description': 'Testing'}
                elif 'skill' in path.lower():
                    test_data = {'name': 'Test Skill', 'category': 'testing', 'level': 'beginner'}
                
                # Replace path parameters with test values
                test_url = url.replace('{agent_id}', 'test_agent_123')
                test_url = test_url.replace('{workflow_id}', 'test_workflow_123') 
                test_url = test_url.replace('{skill_id}', 'test_skill_123')
                test_url = test_url.replace('{config_id}', 'test_config_123')
                test_url = test_url.replace('{config_key}', 'test_key')
                
                if method == 'GET':
                    response = await client.get(test_url)
                elif method == 'POST':
                    response = await client.post(test_url, json=test_data)
                elif method == 'PUT':
                    response = await client.put(test_url, json=test_data)
                elif method == 'DELETE':
                    response = await client.delete(test_url)
                else:
                    return None
                
                duration = time.time() - start_time
                
                result = {
                    'endpoint': endpoint['full_endpoint'],
                    'method': method,
                    'path': path,
                    'status_code': response.status_code,
                    'success': response.status_code < 400,
                    'response_time_ms': round(duration * 1000, 2),
                    'response_size': len(response.content) if response.content else 0
                }
                
                if response.status_code < 400:
                    self.results['successful_tests'] += 1
                else:
                    self.results['failed_tests'] += 1
                    
                return result
                
            except Exception as e:
                duration = time.time() - start_time
                return {
                    'endpoint': endpoint['full_endpoint'],
                    'method': method,
                    'path': path,
                    'status_code': 0,
                    'success': False,
                    'response_time_ms': round(duration * 1000, 2),
                    'error': str(e)
                }
    
    async def run_comprehensive_test(self):
        print('🚀 ROUND 7 - COMPREHENSIVE API TESTING')
        print('=' * 50)
        
        endpoints = await self.discover_endpoints()
        self.results['total_endpoints'] = len(endpoints)
        
        print(f'✅ Discovered {len(endpoints)} endpoints')
        
        # Test all endpoints
        for i, endpoint in enumerate(endpoints):
            result = await self.test_endpoint(endpoint)
            if result:
                self.results['endpoints_tested'].append(result)
                status = '✅' if result['success'] else '❌'
                print(f'{status} {i+1:2d}/{len(endpoints)} {result[endpoint]} (HTTP {result[status_code]}) - {result[response_time_ms]}ms')
        
        # Performance analysis
        successful_times = [r['response_time_ms'] for r in self.results['endpoints_tested'] if r['success']]
        if successful_times:
            self.results['performance_metrics'] = {
                'avg_response_time': round(sum(successful_times) / len(successful_times), 2),
                'min_response_time': min(successful_times),
                'max_response_time': max(successful_times),
                'total_successful': len(successful_times)
            }
        
        # Compare with Round 6 (46 endpoints)
        round6_endpoints = 46
        new_endpoints = len(endpoints) - round6_endpoints
        
        self.results['comparison_with_round6'] = {
            'round6_endpoints': round6_endpoints,
            'round7_endpoints': len(endpoints),
            'new_endpoints_added': new_endpoints,
            'growth_percentage': round((new_endpoints / round6_endpoints) * 100, 1) if round6_endpoints > 0 else 0
        }
        
        # Success rate
        success_rate = (self.results['successful_tests'] / len(endpoints)) * 100 if endpoints else 0
        
        print('\n' + '=' * 50)
        print('📊 ROUND 7 - FINAL RESULTS')
        print('=' * 50)
        print(f'Total Endpoints: {len(endpoints)} (+{new_endpoints} from Round 6)')
        print(f'Successful Tests: {self.results[successful_tests]}')
        print(f'Failed Tests: {self.results[failed_tests]}')
        print(f'Success Rate: {success_rate:.1f}%')
        
        if successful_times:
            print(f'Avg Response Time: {self.results[performance_metrics][avg_response_time]}ms')
            print(f'Fastest Response: {self.results[performance_metrics][min_response_time]}ms')
            print(f'Slowest Response: {self.results[performance_metrics][max_response_time]}ms')
        
        return self.results

async def main():
    tester = Round7Tester()
    results = await tester.run_comprehensive_test()
    
    # Save results
    with open('logs/round7_comprehensive_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    return results

if __name__ == '__main__':
    asyncio.run(main())
