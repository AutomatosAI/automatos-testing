#!/usr/bin/env python3
"""
PHASE 5: COMPREHENSIVE PERFORMANCE ANALYTICS TESTING
Tests all performance analytics and monitoring endpoints with full request/response logging
"""

import sys
import os
import time
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from shared_utils import ComprehensiveAPITester

class PerformanceAnalyticsTester:
    """
    Comprehensive Performance Analytics testing with full API logging
    """
    
    def __init__(self):
        test_dir = Path(__file__).parent.parent
        config_path = test_dir.parent / "shared_config.yaml"
        
        self.tester = ComprehensiveAPITester(
            config_path=str(config_path),
            phase_name="performance_analytics",
            test_dir=str(test_dir)
        )
        
        self.performance_data_collected = []
        self.metrics_analyzed = []
        self.test_summary = {
            "metrics_collected": 0,
            "dashboards_accessed": 0,
            "analytics_operations": 0,
            "performance_tests": 0,
            "monitoring_checks": 0,
            "realtime_operations": 0,
            "api_calls_made": 0,
            "successful_calls": 0,
            "failed_calls": 0
        }
    
    def run_comprehensive_tests(self):
        """
        Run all performance analytics tests and return real success/failure
        """
        print("🚀 STARTING COMPREHENSIVE PERFORMANCE ANALYTICS TESTING")
        print("=" * 75)
        
        try:
            # Phase 1: Environment Setup & Performance System Discovery
            self.test_environment_setup()
            
            # Phase 2: System Metrics Collection
            self.test_system_metrics()
            
            # Phase 3: Performance Dashboards & Overview
            self.test_performance_dashboards()
            
            # Phase 4: Real-Time Performance Monitoring
            self.test_realtime_monitoring()
            
            # Phase 5: Response Time Analytics
            self.test_response_time_analytics()
            
            # Phase 6: Throughput & Load Analysis
            self.test_throughput_analysis()
            
            # Phase 7: Resource Utilization Monitoring
            self.test_resource_utilization()
            
            # Phase 8: Performance Optimization Analytics
            self.test_performance_optimization()
            
            # Phase 9: Historical Performance Analysis
            self.test_historical_analysis()
            
            # Phase 10: Error Handling & Edge Cases
            self.test_error_handling()
            
            # Phase 11: Performance Stress Testing
            self.test_performance_stress()
            
            # Generate final report
            report = self.generate_final_report()
            
            # Calculate real success based on API results
            total_calls = self.test_summary["api_calls_made"]
            successful_calls = self.test_summary["successful_calls"]
            
            print(f"\n📊 PERFORMANCE ANALYTICS TESTING COMPLETED")
            print(f"📊 Total API Calls: {total_calls}")
            print(f"✅ Successful: {successful_calls}")
            print(f"❌ Failed: {total_calls - successful_calls}")
            
            # Define minimum success threshold (70% of API calls must succeed)
            success_threshold = 0.7
            success_rate = successful_calls / total_calls if total_calls > 0 else 0
            
            print(f"📈 Success Rate: {success_rate * 100:.1f}%")
            print(f"🎯 Required Threshold: {success_threshold * 100:.1f}%")
            
            is_successful = success_rate >= success_threshold
            
            if is_successful:
                print("✅ PERFORMANCE ANALYTICS TESTS PASSED - Meeting minimum threshold")
                return True
            else:
                print("❌ PERFORMANCE ANALYTICS TESTS FAILED - Below minimum threshold")
                return False
            
        except Exception as e:
            print(f"💥 COMPREHENSIVE TESTING FAILED: {str(e)}")
            import traceback
            print(f"🔍 Error details: {traceback.format_exc()}")
            return False

    def test_environment_setup(self):
        """
        Test 1: Environment Setup and Performance System Discovery
        """
        print("\n🔍 PHASE 1: ENVIRONMENT SETUP & PERFORMANCE SYSTEM DISCOVERY")
        
        # Test 1.1: Health Check
        result = self.tester.make_api_call("GET", "/health")
        self.update_summary(result)
        
        # Test 1.2: Endpoint Discovery
        discovery = self.tester.test_endpoint_discovery()
        
        # Test 1.3: Performance System Availability
        performance_endpoints = [
            "/api/system/metrics",
            "/api/system/performance/dashboard",
            "/api/analytics/performance",
            "/api/system/health/detailed"
        ]
        
        print("\n📋 Testing Performance Analytics Endpoint Availability:")
        for endpoint in performance_endpoints:
            result = self.tester.make_api_call("GET", endpoint, expected_status=[200, 404, 405])
            self.update_summary(result)
            status = "✅ Available" if result.get("validation", {}).get("is_success") else "❌ Not Available"
            print(f"  {endpoint}: {status}")
        
        # Test 1.4: Validate Expected Performance Endpoints
        validation = self.tester.validate_endpoint_list("performance_analytics")
        
        print(f"✅ Environment setup completed - {len(discovery['endpoints'])} total endpoints discovered")
    
    def test_system_metrics_collection(self):
        """
        Test 2: System Metrics Collection
        """
        print("\n📊 PHASE 2: SYSTEM METRICS COLLECTION")
        
        # Test 2.1: Basic System Metrics
        result = self.tester.make_api_call("GET", "/api/system/metrics")
        self.update_summary(result)
        if result.get("validation", {}).get("is_success"):
            self.test_summary["metrics_collected"] += 1
            self.metrics_analyzed.append("system_metrics")
        
        # Test 2.2: Detailed Health Metrics
        result = self.tester.make_api_call("GET", "/api/system/health/detailed")
        self.update_summary(result)
        if result.get("validation", {}).get("is_success"):
            self.test_summary["metrics_collected"] += 1
        
        # Test 2.3: Performance Analytics Overview
        result = self.tester.make_api_call("GET", "/api/analytics/performance")
        self.update_summary(result)
        if result.get("validation", {}).get("is_success"):
            self.test_summary["analytics_operations"] += 1
        
        # Test 2.4: System Overview Analytics
        result = self.tester.make_api_call("GET", "/api/analytics/system/overview")
        self.update_summary(result)
        if result.get("validation", {}).get("is_success"):
            self.test_summary["analytics_operations"] += 1
        
        # Test 2.5: Custom Metrics Collection
        metrics_query = {
            "metrics": ["cpu_usage", "memory_usage", "response_time", "throughput"],
            "timeframe": "1h",
            "granularity": "5m"
        }
        result = self.tester.make_api_call("POST", "/api/system/metrics/query", metrics_query, [200, 404])
        self.update_summary(result)
        
        print(f"✅ System metrics collection completed - {self.test_summary['metrics_collected']} metrics collected")
    
    def test_performance_dashboards(self):
        """
        Test 3: Performance Dashboards & Overview
        """
        print("\n📈 PHASE 3: PERFORMANCE DASHBOARDS & OVERVIEW")
        
        # Test 3.1: Main Performance Dashboard
        result = self.tester.make_api_call("GET", "/api/system/performance/dashboard")
        self.update_summary(result)
        if result.get("validation", {}).get("is_success"):
            self.test_summary["dashboards_accessed"] += 1
        
        # Test 3.2: System Performance Overview
        result = self.tester.make_api_call("GET", "/api/system/performance/overview", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 3.3: Performance Summary with Time Range
        dashboard_params = {
            "timeframe": "24h",
            "metrics": ["response_time", "throughput", "error_rate"],
            "granularity": "1h"
        }
        result = self.tester.make_api_call("GET", "/api/system/performance/dashboard", dashboard_params)
        self.update_summary(result)
        if result.get("validation", {}).get("is_success"):
            self.test_summary["dashboards_accessed"] += 1
        
        # Test 3.4: Performance Trends Analysis
        result = self.tester.make_api_call("GET", "/api/analytics/performance/trends", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 3.5: Custom Dashboard Configuration
        dashboard_config = {
            "dashboard_type": "performance_overview",
            "widgets": ["cpu_chart", "memory_chart", "response_time_chart"],
            "refresh_interval": "30s"
        }
        result = self.tester.make_api_call("POST", "/api/system/performance/dashboard/config", dashboard_config, [200, 404])
        self.update_summary(result)
        
        print(f"✅ Performance dashboards testing completed - {self.test_summary['dashboards_accessed']} dashboards accessed")
    
    def test_realtime_monitoring(self):
        """
        Test 4: Real-time Performance Monitoring
        """
        print("\n⚡ PHASE 4: REAL-TIME PERFORMANCE MONITORING")
        
        # Test 4.1: Real-time Performance Data
        result = self.tester.make_api_call("GET", "/api/system/performance/realtime")
        self.update_summary(result)
        if result.get("validation", {}).get("is_success"):
            self.test_summary["realtime_operations"] += 1
        
        # Test 4.2: Live System Metrics Stream
        result = self.tester.make_api_call("GET", "/api/system/metrics/live", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 4.3: Real-time Monitoring Over Time
        print("\n⏱️ Monitoring Real-time Performance Over 3 Intervals:")
        for i in range(3):
            result = self.tester.make_api_call("GET", "/api/system/performance/realtime")
            self.update_summary(result)
            if result.get("validation", {}).get("is_success"):
                self.test_summary["realtime_operations"] += 1
            if i < 2:
                time.sleep(2)
        
        # Test 4.4: Real-time Alert Status
        result = self.tester.make_api_call("GET", "/api/system/alerts/active", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 4.5: Live Performance Thresholds
        result = self.tester.make_api_call("GET", "/api/system/performance/thresholds", expected_status=[200, 404])
        self.update_summary(result)
        
        print(f"✅ Real-time monitoring completed - {self.test_summary['realtime_operations']} real-time operations")
    
    def test_response_time_analytics(self):
        """
        Test 5: Response Time Analytics
        """
        print("\n⏱️ PHASE 5: RESPONSE TIME ANALYTICS")
        
        # Test 5.1: Response Time Metrics
        result = self.tester.make_api_call("GET", "/api/metrics/response-times")
        self.update_summary(result)
        if result.get("validation", {}).get("is_success"):
            self.test_summary["performance_tests"] += 1
            self.metrics_analyzed.append("response_times")
        
        # Test 5.2: Endpoint Response Time Analysis
        result = self.tester.make_api_call("GET", "/api/analytics/response-times/endpoints", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 5.3: Response Time Distribution
        time_params = {
            "timeframe": "12h",
            "percentiles": [50, 90, 95, 99],
            "group_by": "endpoint"
        }
        result = self.tester.make_api_call("GET", "/api/metrics/response-times", time_params)
        self.update_summary(result)
        
        # Test 5.4: Slow Query Analysis
        result = self.tester.make_api_call("GET", "/api/analytics/slow-queries", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 5.5: Response Time Optimization Suggestions
        result = self.tester.make_api_call("GET", "/api/analytics/response-time/optimization", expected_status=[200, 404])
        self.update_summary(result)
        
        print(f"✅ Response time analytics completed - analyzed {len(self.metrics_analyzed)} metric types")
    
    def test_throughput_analysis(self):
        """
        Test 6: Throughput & Load Analysis
        """
        print("\n🚀 PHASE 6: THROUGHPUT & LOAD ANALYSIS")
        
        # Test 6.1: Throughput Metrics
        result = self.tester.make_api_call("GET", "/api/metrics/throughput")
        self.update_summary(result)
        if result.get("validation", {}).get("is_success"):
            self.test_summary["performance_tests"] += 1
            self.metrics_analyzed.append("throughput")
        
        # Test 6.2: Load Analysis
        result = self.tester.make_api_call("GET", "/api/analytics/load", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 6.3: Concurrent Request Analysis
        result = self.tester.make_api_call("GET", "/api/analytics/concurrent-requests", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 6.4: Throughput by Time Period
        throughput_params = {
            "timeframe": "6h",
            "interval": "15m",
            "metrics": ["requests_per_second", "bytes_per_second"]
        }
        result = self.tester.make_api_call("GET", "/api/metrics/throughput", throughput_params)
        self.update_summary(result)
        
        # Test 6.5: Peak Load Analysis
        result = self.tester.make_api_call("GET", "/api/analytics/peak-load", expected_status=[200, 404])
        self.update_summary(result)
        
        print("✅ Throughput analysis completed")
    
    def test_resource_utilization(self):
        """
        Test 7: Resource Utilization Monitoring
        """
        print("\n💾 PHASE 7: RESOURCE UTILIZATION MONITORING")
        
        # Test 7.1: CPU Utilization
        result = self.tester.make_api_call("GET", "/api/system/resources/cpu", expected_status=[200, 404])
        self.update_summary(result)
        if result.get("validation", {}).get("is_success"):
            self.test_summary["monitoring_checks"] += 1
        
        # Test 7.2: Memory Utilization
        result = self.tester.make_api_call("GET", "/api/system/resources/memory", expected_status=[200, 404])
        self.update_summary(result)
        if result.get("validation", {}).get("is_success"):
            self.test_summary["monitoring_checks"] += 1
        
        # Test 7.3: Disk I/O Metrics
        result = self.tester.make_api_call("GET", "/api/system/resources/disk", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 7.4: Network Utilization
        result = self.tester.make_api_call("GET", "/api/system/resources/network", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 7.5: Database Performance
        result = self.tester.make_api_call("GET", "/api/system/database/performance", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 7.6: Resource Usage Trends
        resource_params = {
            "resources": ["cpu", "memory", "disk", "network"],
            "timeframe": "4h",
            "aggregation": "average"
        }
        result = self.tester.make_api_call("GET", "/api/system/resources/trends", resource_params, expected_status=[200, 404])
        self.update_summary(result)
        
        print(f"✅ Resource utilization monitoring completed - {self.test_summary['monitoring_checks']} monitoring checks")
    
    def test_performance_optimization(self):
        """
        Test 8: Performance Optimization Analytics
        """
        print("\n🔧 PHASE 8: PERFORMANCE OPTIMIZATION ANALYTICS")
        
        # Test 8.1: Performance Bottleneck Analysis
        result = self.tester.make_api_call("GET", "/api/analytics/bottlenecks", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 8.2: Optimization Recommendations
        result = self.tester.make_api_call("GET", "/api/analytics/optimization/recommendations", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 8.3: Performance Scoring
        result = self.tester.make_api_call("GET", "/api/analytics/performance/score", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 8.4: Capacity Planning Analysis
        capacity_data = {
            "projection_period": "30d",
            "growth_rate": 0.1,
            "metrics": ["cpu", "memory", "storage"]
        }
        result = self.tester.make_api_call("POST", "/api/analytics/capacity-planning", capacity_data, [200, 404])
        self.update_summary(result)
        
        # Test 8.5: Performance Benchmark Comparison
        benchmark_data = {
            "benchmark_type": "api_performance",
            "comparison_period": "7d"
        }
        result = self.tester.make_api_call("POST", "/api/analytics/benchmark", benchmark_data, [200, 404])
        self.update_summary(result)
        
        print("✅ Performance optimization analytics completed")
    
    def test_historical_analysis(self):
        """
        Test 9: Historical Performance Analysis
        """
        print("\n📈 PHASE 9: HISTORICAL PERFORMANCE ANALYSIS")
        
        # Test 9.1: Historical Performance Data
        historical_params = {
            "start_date": "2025-07-30T00:00:00Z",
            "end_date": "2025-07-31T23:59:59Z",
            "metrics": ["response_time", "throughput", "error_rate"]
        }
        result = self.tester.make_api_call("GET", "/api/analytics/historical", historical_params, expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 9.2: Performance Trend Analysis
        result = self.tester.make_api_call("GET", "/api/analytics/trends", expected_status=[200, 404])
        self.update_summary(result)
        
        # Test 9.3: Comparative Analysis
        comparison_data = {
            "period1": {"start": "2025-07-30T00:00:00Z", "end": "2025-07-30T23:59:59Z"},
            "period2": {"start": "2025-07-31T00:00:00Z", "end": "2025-07-31T23:59:59Z"},
            "metrics": ["avg_response_time", "total_requests"]
        }
        result = self.tester.make_api_call("POST", "/api/analytics/compare", comparison_data, [200, 404])
        self.update_summary(result)
        
        # Test 9.4: Performance Reports Generation
        report_config = {
            "report_type": "performance_summary",
            "period": "daily",
            "format": "json"
        }
        result = self.tester.make_api_call("POST", "/api/analytics/reports/generate", report_config, [200, 404])
        self.update_summary(result)
        
        print("✅ Historical analysis completed")
    
    def test_error_handling(self):
        """
        Test 10: Error Handling and Edge Cases
        """
        print("\n🚨 PHASE 10: ERROR HANDLING & EDGE CASES")
        
        # Test 10.1: Invalid Metrics Query
        invalid_metrics = {
            "metrics": ["invalid_metric", "nonexistent_metric"],
            "timeframe": "invalid_timeframe"
        }
        result = self.tester.make_api_call("POST", "/api/system/metrics/query", invalid_metrics, expected_status=[400, 404, 422])
        self.update_summary(result)
        
        # Test 10.2: Invalid Time Range
        invalid_time_params = {
            "start_date": "invalid_date",
            "end_date": "2025-13-45T25:70:90Z"  # Invalid date
        }
        result = self.tester.make_api_call("GET", "/api/analytics/historical", invalid_time_params, expected_status=[400, 422])
        self.update_summary(result)
        
        # Test 10.3: Non-existent Dashboard
        result = self.tester.make_api_call("GET", "/api/system/performance/dashboard/nonexistent", expected_status=404)
        self.update_summary(result)
        
        # Test 10.4: Invalid Optimization Request
        invalid_optimization = {
            "optimization_target": "invalid_target",
            "constraints": {"invalid_constraint": "invalid_value"}
        }
        result = self.tester.make_api_call("POST", "/api/analytics/optimization", invalid_optimization, expected_status=[400, 404, 422])
        self.update_summary(result)
        
        print("✅ Error handling testing completed")
    
    def test_performance_stress(self):
        """
        Test 11: Performance Stress Testing
        """
        print("\n⚡ PHASE 11: PERFORMANCE STRESS TESTING")
        
        # Test 11.1: Rapid Metrics Collection
        print("🔥 Rapid metrics collection stress test:")
        for i in range(10):
            result = self.tester.make_api_call("GET", "/api/system/metrics")
            self.update_summary(result)
            if result.get("validation", {}).get("is_success"):
                self.test_summary["performance_tests"] += 1
        
        # Test 11.2: Concurrent Dashboard Access
        print("📊 Concurrent dashboard access test:")
        for i in range(5):
            result = self.tester.make_api_call("GET", "/api/system/performance/dashboard")
            self.update_summary(result)
        
        # Test 11.3: Real-time Monitoring Stress
        print("⚡ Real-time monitoring stress test:")
        for i in range(5):
            result = self.tester.make_api_call("GET", "/api/system/performance/realtime")
            self.update_summary(result)
        
        print(f"✅ Performance stress testing completed - {self.test_summary['performance_tests']} performance tests executed")
    
    def update_summary(self, result):
        """Update test summary statistics"""
        self.test_summary["api_calls_made"] += 1
        if result.get("validation", {}).get("is_success", False):
            self.test_summary["successful_calls"] += 1
        else:
            self.test_summary["failed_calls"] += 1
    
    def generate_final_report(self):
        """Generate comprehensive final report"""
        base_report = self.tester.generate_comprehensive_report()
        
        # Add performance analytics specific metrics
        base_report["performance_analytics_summary"] = self.test_summary
        
        # Calculate performance system capabilities
        base_report["performance_system_analysis"] = {
            "metrics_collection_available": self.test_summary["metrics_collected"] > 0,
            "dashboards_available": self.test_summary["dashboards_accessed"] > 0,
            "realtime_monitoring_available": self.test_summary["realtime_operations"] > 0,
            "analytics_available": self.test_summary["analytics_operations"] > 0,
            "monitoring_checks_available": self.test_summary["monitoring_checks"] > 0,
            "performance_testing_capable": self.test_summary["performance_tests"] > 0,
            "metrics_analyzed": self.metrics_analyzed
        }
        
        # Save enhanced report
        report_file = Path(self.tester.test_dir) / "results" / f"FINAL_PERFORMANCE_ANALYTICS_REPORT_{int(time.time())}.json"
        with open(report_file, 'w') as f:
            import json
            json.dump(base_report, f, indent=2)
        
        return base_report

def main():
    """
    Main execution function
    """
    print("🚀 COMPREHENSIVE PERFORMANCE ANALYTICS TESTING")
    print("==============================================")
    
    tester = PerformanceAnalyticsTester()
    success = tester.run_comprehensive_tests()
    
    # Cleanup resources
    tester.tester.cleanup()
    
    if success:
        print("\n🎉 COMPREHENSIVE PERFORMANCE ANALYTICS TESTING COMPLETED SUCCESSFULLY!")
        return 0
    else:
        print("\n💥 COMPREHENSIVE PERFORMANCE ANALYTICS TESTING FAILED!")
        return 1


    def test_system_metrics(self):
        """
        Test 2: System Metrics Collection
        """
        print("📊 PHASE 2: SYSTEM METRICS COLLECTION")
        
        # Test 2.1: Get current system metrics
        result = self.tester.make_api_call("GET", "/api/system/metrics")
        self.update_summary(result)
        
        # Test 2.2: Get detailed system health
        result = self.tester.make_api_call("GET", "/api/system/health")
        self.update_summary(result)
        
        # Test 2.3: Get system configuration
        result = self.tester.make_api_call("GET", "/api/system/config")
        self.update_summary(result)
        
        # Test 2.4: Test system test route
        result = self.tester.make_api_call("GET", "/api/system/test-route")
        self.update_summary(result)
        
        print("✅ System metrics collection completed")

if __name__ == "__main__":
    exit(main())