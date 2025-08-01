import httpx
import asyncio
import json

async def main():
    print('🔍 Round 7: Discovering API endpoints...')
    
    async with httpx.AsyncClient() as client:
        try:
            # Test basic connectivity
            health_response = await client.get('http://localhost:8000/health')
            print(f'✅ Health Check: HTTP {health_response.status_code}')
            
            # Discover endpoints
            openapi_response = await client.get('http://localhost:8000/openapi.json')
            if openapi_response.status_code == 200:
                openapi_data = openapi_response.json()
                endpoints = []
                for path, methods in openapi_data.get('paths', {}).items():
                    for method in methods.keys():
                        endpoints.append(f'{method.upper()} {path}')
                
                print(f'✅ Discovered {len(endpoints)} total endpoints')
                print('📋 First 15 endpoints:')
                for i, ep in enumerate(endpoints[:15]):
                    print(f'  {i+1:2d}. {ep}')
                
                if len(endpoints) > 15:
                    print(f'  ... and {len(endpoints) - 15} more endpoints')
                    
                # Look for new endpoint patterns
                new_patterns = []
                for ep in endpoints:
                    if 'skill' in ep.lower() or 'chat' in ep.lower() or 'ai' in ep.lower():
                        new_patterns.append(ep)
                
                if new_patterns:
                    print(f'🆕 Found {len(new_patterns)} potential new skill/AI endpoints:')
                    for pattern in new_patterns[:10]:
                        print(f'  ⭐ {pattern}')
                        
            else:
                print(f'❌ OpenAPI Discovery failed: HTTP {openapi_response.status_code}')
                
        except Exception as e:
            print(f'❌ Error: {e}')

if __name__ == '__main__':
    asyncio.run(main())
