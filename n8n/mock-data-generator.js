// COMPREHENSIVE MOCK DATA GENERATOR FOR AUTOMATOS AI PLATFORM
// Generates realistic test failures and system logs for workflow testing

class AutomatosMockDataGenerator {
  constructor() {
    this.timestamp = new Date();
    this.sessionId = `test-session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  // Generate comprehensive test failure scenarios
  generateTestResults() {
    const scenarios = [
      this.generateAgentFailures(),
      this.generateWorkflowFailures(), 
      this.generateContextFailures(),
      this.generateKnowledgeFailures(),
      this.generatePlaybookFailures(),
      this.generateSettingsFailures(),
      this.generateAnalyticsFailures()
    ];

    return {
      ok: false,
      totalTests: scenarios.reduce((sum, s) => sum + s.summary.total_tests, 0),
      totalPassed: scenarios.reduce((sum, s) => sum + s.summary.passed, 0),
      successRate: this.calculateSuccessRate(scenarios),
      fails: scenarios.map(s => `${s.module} (${s.summary.success_rate}%)`),
      aggregate: scenarios.reduce((acc, scenario) => {
        acc[scenario.module] = scenario;
        return acc;
      }, {}),
      sessionId: this.sessionId,
      debug: {
        dataSource: "comprehensive_mock",
        scenarioCount: scenarios.length,
        generatedAt: this.timestamp.toISOString()
      }
    };
  }

  // Agent Management API failures
  generateAgentFailures() {
    return {
      module: "agents",
      ok: true,
      summary: {
        total_tests: 35,
        passed: 4,
        failed: 31,
        success_rate: 11.4,
        status: "failed"
      },
      failed_tests: [
        "test_agent_creation_api",
        "test_agent_execution_engine", 
        "test_agent_memory_allocation",
        "test_agent_skill_assignment",
        "test_agent_communication_bus",
        "test_agent_resource_management",
        "test_agent_coordination_protocols",
        "test_agent_health_monitoring",
        "test_agent_performance_metrics",
        "test_agent_error_recovery",
        "test_agent_load_balancing",
        "test_agent_scaling_policies",
        "test_agent_security_validation",
        "test_agent_data_persistence",
        "test_agent_event_streaming",
        "test_agent_workflow_integration",
        "test_agent_knowledge_access",
        "test_agent_context_awareness",
        "test_agent_decision_making",
        "test_agent_learning_adaptation",
        "test_agent_multi_modal_processing",
        "test_agent_real_time_inference",
        "test_agent_batch_processing",
        "test_agent_streaming_analytics",
        "test_agent_model_versioning",
        "test_agent_a_b_testing",
        "test_agent_deployment_strategies",
        "test_agent_rollback_mechanisms",
        "test_agent_monitoring_dashboards",
        "test_agent_alert_systems",
        "test_agent_compliance_checks"
      ],
      error_patterns: [
        "504 Gateway Timeout on /api/v1/agents/create",
        "Database connection pool exhausted",
        "Memory allocation failed for agent instance",
        "Service discovery timeout for agent coordination",
        "Authentication failed for agent API access"
      ]
    };
  }

  // Workflow Engine failures
  generateWorkflowFailures() {
    return {
      module: "workflows", 
      ok: true,
      summary: {
        total_tests: 28,
        passed: 5,
        failed: 23,
        success_rate: 17.9,
        status: "failed"
      },
      failed_tests: [
        "test_workflow_definition_parsing",
        "test_workflow_execution_engine",
        "test_workflow_state_management",
        "test_workflow_error_handling",
        "test_workflow_parallel_execution",
        "test_workflow_conditional_logic",
        "test_workflow_loop_processing",
        "test_workflow_data_transformation",
        "test_workflow_external_integrations",
        "test_workflow_scheduling_system",
        "test_workflow_resource_allocation",
        "test_workflow_performance_optimization",
        "test_workflow_monitoring_metrics",
        "test_workflow_debugging_tools",
        "test_workflow_version_control",
        "test_workflow_rollback_recovery",
        "test_workflow_security_policies",
        "test_workflow_access_controls",
        "test_workflow_audit_logging",
        "test_workflow_compliance_validation",
        "test_workflow_scalability_testing",
        "test_workflow_load_distribution",
        "test_workflow_failover_mechanisms"
      ],
      error_patterns: [
        "Workflow execution timeout after 300 seconds",
        "Redis connection refused for workflow state",
        "Kafka message queue overflow",
        "Workflow definition validation failed",
        "Resource limit exceeded for parallel workflows"
      ]
    };
  }

  // Context Engineering failures  
  generateContextFailures() {
    return {
      module: "context",
      ok: true, 
      summary: {
        total_tests: 22,
        passed: 2,
        failed: 20,
        success_rate: 9.1,
        status: "failed"
      },
      failed_tests: [
        "test_context_vector_embeddings",
        "test_context_semantic_search",
        "test_context_knowledge_retrieval",
        "test_context_document_processing",
        "test_context_entity_extraction",
        "test_context_relationship_mapping",
        "test_context_temporal_awareness",
        "test_context_multi_modal_fusion",
        "test_context_attention_mechanisms",
        "test_context_memory_networks",
        "test_context_inference_chains",
        "test_context_reasoning_graphs",
        "test_context_uncertainty_handling",
        "test_context_bias_detection",
        "test_context_explainability_features",
        "test_context_privacy_preservation",
        "test_context_federated_learning",
        "test_context_transfer_learning",
        "test_context_continual_adaptation",
        "test_context_meta_learning"
      ],
      error_patterns: [
        "Vector database connection timeout",
        "Embedding model loading failed",
        "CUDA out of memory for context processing",
        "Elasticsearch cluster unavailable",
        "Text processing pipeline crashed"
      ]
    };
  }

  // Knowledge System failures
  generateKnowledgeFailures() {
    return {
      module: "knowledge",
      ok: true,
      summary: {
        total_tests: 26,
        passed: 6,
        failed: 20, 
        success_rate: 23.1,
        status: "failed"
      },
      failed_tests: [
        "test_knowledge_graph_construction",
        "test_knowledge_base_querying",
        "test_knowledge_inference_engine",
        "test_knowledge_consistency_checking",
        "test_knowledge_versioning_system",
        "test_knowledge_conflict_resolution",
        "test_knowledge_automated_reasoning",
        "test_knowledge_ontology_management",
        "test_knowledge_schema_evolution",
        "test_knowledge_data_lineage",
        "test_knowledge_quality_assessment",
        "test_knowledge_provenance_tracking",
        "test_knowledge_access_patterns",
        "test_knowledge_caching_strategies",
        "test_knowledge_distributed_storage",
        "test_knowledge_replication_sync",
        "test_knowledge_backup_recovery",
        "test_knowledge_migration_tools",
        "test_knowledge_performance_tuning",
        "test_knowledge_security_controls"
      ],
      error_patterns: [
        "Neo4j graph database connection lost",
        "Knowledge base index corruption detected",
        "Ontology reasoning timeout",
        "Memory exhaustion during graph traversal",
        "Concurrent modification conflict"
      ]
    };
  }

  // Multi-Agent Playbook failures
  generatePlaybookFailures() {
    return {
      module: "playbooks",
      ok: true,
      summary: {
        total_tests: 31,
        passed: 7,
        failed: 24,
        success_rate: 22.6,
        status: "failed"
      },
      failed_tests: [
        "test_playbook_orchestration",
        "test_playbook_agent_coordination",
        "test_playbook_resource_sharing",
        "test_playbook_conflict_resolution", 
        "test_playbook_load_balancing",
        "test_playbook_fault_tolerance",
        "test_playbook_consensus_mechanisms",
        "test_playbook_communication_protocols",
        "test_playbook_state_synchronization",
        "test_playbook_decision_aggregation",
        "test_playbook_performance_monitoring",
        "test_playbook_scalability_testing",
        "test_playbook_security_validation",
        "test_playbook_audit_compliance",
        "test_playbook_version_management",
        "test_playbook_deployment_automation",
        "test_playbook_rollback_procedures",
        "test_playbook_disaster_recovery",
        "test_playbook_capacity_planning",
        "test_playbook_cost_optimization",
        "test_playbook_quality_assurance",
        "test_playbook_integration_testing",
        "test_playbook_user_acceptance",
        "test_playbook_performance_benchmarks"
      ],
      error_patterns: [
        "Agent communication bus overloaded",
        "Playbook execution deadlock detected", 
        "Resource allocation conflict between agents",
        "Consensus algorithm timeout",
        "Distributed lock acquisition failed"
      ]
    };
  }

  // Settings & Configuration failures
  generateSettingsFailures() {
    return {
      module: "settings",
      ok: false,
      error: "Configuration service unavailable",
      summary: {
        total_tests: 18,
        passed: 0,
        failed: 18,
        success_rate: 0.0,
        status: "critical"
      },
      failed_tests: [
        "test_settings_api_endpoints",
        "test_settings_validation_rules",
        "test_settings_persistence_layer",
        "test_settings_caching_mechanism",
        "test_settings_change_notifications",
        "test_settings_audit_logging",
        "test_settings_access_controls",
        "test_settings_encryption_at_rest",
        "test_settings_backup_procedures",
        "test_settings_recovery_mechanisms",
        "test_settings_version_history",
        "test_settings_rollback_capabilities",
        "test_settings_environment_isolation",
        "test_settings_feature_flags",
        "test_settings_a_b_testing",
        "test_settings_performance_tuning",
        "test_settings_monitoring_alerts",
        "test_settings_compliance_checks"
      ],
      error_patterns: [
        "Settings database completely offline",
        "Configuration schema migration failed",
        "Encryption key rotation error",
        "Settings API authentication breakdown",
        "Critical configuration corruption"
      ]
    };
  }

  // Analytics & Monitoring failures
  generateAnalyticsFailures() {
    return {
      module: "analytics", 
      ok: false,
      error: "Analytics pipeline down",
      summary: {
        total_tests: 24,
        passed: 1,
        failed: 23,
        success_rate: 4.2,
        status: "critical"
      },
      failed_tests: [
        "test_analytics_data_collection",
        "test_analytics_real_time_processing",
        "test_analytics_batch_aggregation",
        "test_analytics_streaming_pipeline",
        "test_analytics_data_validation",
        "test_analytics_quality_checks",
        "test_analytics_anomaly_detection",
        "test_analytics_trend_analysis",
        "test_analytics_predictive_modeling",
        "test_analytics_dashboard_rendering",
        "test_analytics_report_generation",
        "test_analytics_alert_system",
        "test_analytics_notification_delivery",
        "test_analytics_data_export",
        "test_analytics_api_integration",
        "test_analytics_security_compliance",
        "test_analytics_performance_optimization",
        "test_analytics_scalability_testing",
        "test_analytics_disaster_recovery",
        "test_analytics_data_retention",
        "test_analytics_archival_procedures",
        "test_analytics_cost_management",
        "test_analytics_resource_monitoring"
      ],
      error_patterns: [
        "ClickHouse cluster completely down",
        "Kafka stream processing failed",
        "Real-time dashboard connection lost",
        "Analytics database corruption",
        "Data pipeline memory overflow"
      ]
    };
  }

  calculateSuccessRate(scenarios) {
    const totalTests = scenarios.reduce((sum, s) => sum + s.summary.total_tests, 0);
    const totalPassed = scenarios.reduce((sum, s) => sum + s.summary.passed, 0);
    return Math.round((totalPassed / totalTests) * 100 * 100) / 100;
  }

  // Generate comprehensive system logs
  generateSystemLogs() {
    const now = new Date();
    const logs = {
      application_errors: this.generateApplicationLogs(now),
      infrastructure_issues: this.generateInfrastructureLogs(now),
      database_problems: this.generateDatabaseLogs(now),
      network_connectivity: this.generateNetworkLogs(now),
      security_events: this.generateSecurityLogs(now),
      performance_metrics: this.generatePerformanceLogs(now)
    };

    return {
      systemLogs: logs,
      logAnalysis: {
        total_error_events: Object.values(logs).flat().length,
        timeframe: "Last 30 minutes",
        critical_events: this.identifyCriticalEvents(logs),
        correlation_score: 0.87,
        system_health: "DEGRADED"
      }
    };
  }

  generateApplicationLogs(baseTime) {
    return [
      `${this.formatLogTime(baseTime, -25)} [FATAL] AgentManager: Agent pool exhausted - cannot create new agent instances`,
      `${this.formatLogTime(baseTime, -22)} [ERROR] WorkflowEngine: Execution timeout for workflow_id=wf_12345 after 300 seconds`,
      `${this.formatLogTime(baseTime, -20)} [ERROR] ContextProcessor: Vector embedding service unreachable (connection refused)`,
      `${this.formatLogTime(baseTime, -18)} [FATAL] KnowledgeGraph: Neo4j connection pool exhausted - failing all queries`,
      `${this.formatLogTime(baseTime, -15)} [ERROR] PlaybookOrchestrator: Agent coordination deadlock detected`,
      `${this.formatLogTime(baseTime, -12)} [CRITICAL] SettingsService: Configuration database offline - using cached values`,
      `${this.formatLogTime(baseTime, -10)} [FATAL] AnalyticsPipeline: ClickHouse cluster unreachable - data loss imminent`,
      `${this.formatLogTime(baseTime, -8)} [ERROR] APIGateway: Rate limit exceeded for /api/v1/agents/* endpoints`,
      `${this.formatLogTime(baseTime, -5)} [WARN] MemoryManager: Heap utilization at 94% - triggering garbage collection`,
      `${this.formatLogTime(baseTime, -2)} [ERROR] LoadBalancer: Backend server 192.168.1.10 marked as unhealthy`
    ];
  }

  generateInfrastructureLogs(baseTime) {
    return [
      `${this.formatLogTime(baseTime, -28)} [ERROR] kubernetes: Pod automatos-backend-7f8b9c-xkj2p CrashLoopBackOff`,
      `${this.formatLogTime(baseTime, -24)} [WARN] docker: Container automatos-agents restarted 5 times in last hour`,
      `${this.formatLogTime(baseTime, -21)} [CRITICAL] systemd: automatos-api.service failed to start (exit code 1)`,
      `${this.formatLogTime(baseTime, -17)} [ERROR] nginx: upstream server timed out (110: Connection timed out)`,
      `${this.formatLogTime(baseTime, -14)} [WARN] disk: /var/lib/docker filesystem 89% full`,
      `${this.formatLogTime(baseTime, -11)} [ERROR] network: packet loss detected on eth0 interface (5.2%)`,
      `${this.formatLogTime(baseTime, -9)} [CRITICAL] memory: OOM killer terminated process automatos-context (PID 15432)`,
      `${this.formatLogTime(baseTime, -6)} [ERROR] cpu: high load average 8.45 exceeding threshold`,
      `${this.formatLogTime(baseTime, -3)} [WARN] ssl: certificate for automatos.ai expires in 7 days`,
      `${this.formatLogTime(baseTime, -1)} [ERROR] firewall: blocked 127 suspicious connection attempts`
    ];
  }

  generateDatabaseLogs(baseTime) {
    return [
      `${this.formatLogTime(baseTime, -26)} [ERROR] postgresql: too many connections for database "automatos_main" (max: 100)`,
      `${this.formatLogTime(baseTime, -23)} [FATAL] redis: memory usage 98% - evicting keys to free space`,
      `${this.formatLogTime(baseTime, -19)} [ERROR] mongodb: replica set connection failed - primary node unreachable`,
      `${this.formatLogTime(baseTime, -16)} [WARN] postgresql: slow query detected (duration: 45.2s) in agents table`,
      `${this.formatLogTime(baseTime, -13)} [ERROR] elasticsearch: cluster health RED - 3 nodes missing`,
      `${this.formatLogTime(baseTime, -7)} [CRITICAL] neo4j: transaction rollback due to deadlock detection`,
      `${this.formatLogTime(baseTime, -4)} [ERROR] clickhouse: disk space insufficient for new data ingestion`
    ];
  }

  generateNetworkLogs(baseTime) {
    return [
      `${this.formatLogTime(baseTime, -27)} [ERROR] api-gateway: 502 Bad Gateway for /api/v1/agents/execute`,
      `${this.formatLogTime(baseTime, -24)} [ERROR] load-balancer: backend connection timeout to 10.0.1.15:8080`,
      `${this.formatLogTime(baseTime, -20)} [WARN] dns: resolution timeout for internal service discovery`,
      `${this.formatLogTime(baseTime, -15)} [ERROR] tcp: connection reset by peer during data transfer`,
      `${this.formatLogTime(baseTime, -10)} [CRITICAL] tls: handshake failure rate 15% above normal`,
      `${this.formatLogTime(baseTime, -5)} [ERROR] websocket: connection dropped for 24 active sessions`
    ];
  }

  generateSecurityLogs(baseTime) {
    return [
      `${this.formatLogTime(baseTime, -25)} [ALERT] auth: 15 failed login attempts from IP 203.0.113.42`,
      `${this.formatLogTime(baseTime, -18)} [CRITICAL] security: JWT token tampering detected`,
      `${this.formatLogTime(baseTime, -12)} [WARN] audit: unauthorized API access attempt blocked`,
      `${this.formatLogTime(baseTime, -8)} [ERROR] encryption: key rotation failed for customer data`,
      `${this.formatLogTime(baseTime, -3)} [ALERT] intrusion: potential SQL injection in workflow parameters`
    ];
  }

  generatePerformanceLogs(baseTime) {
    return [
      `${this.formatLogTime(baseTime, -22)} [WARN] performance: API response time 95th percentile: 2.8s`,
      `${this.formatLogTime(baseTime, -16)} [ERROR] performance: agent creation latency exceeds SLA (>5s)`,
      `${this.formatLogTime(baseTime, -11)} [CRITICAL] performance: memory leak detected in context processing`,
      `${this.formatLogTime(baseTime, -6)} [WARN] performance: garbage collection pause time: 450ms`,
      `${this.formatLogTime(baseTime, -2)} [ERROR] performance: database query timeout threshold exceeded`
    ];
  }

  identifyCriticalEvents(logs) {
    return [
      "Multiple database connections failing simultaneously",
      "Agent management system completely down", 
      "Configuration service offline causing cascading failures",
      "Memory exhaustion across multiple services",
      "Network connectivity issues affecting service mesh"
    ];
  }

  formatLogTime(baseTime, minutesOffset) {
    const logTime = new Date(baseTime.getTime() + (minutesOffset * 60000));
    return logTime.toISOString().replace('T', ' ').split('.')[0];
  }

  // Generate complete dataset
  generateCompleteDataset() {
    const testResults = this.generateTestResults();
    const systemLogs = this.generateSystemLogs();
    
    return {
      ...testResults,
      ...systemLogs,
      metadata: {
        generated_at: this.timestamp.toISOString(),
        generator_version: "1.0.0",
        dataset_type: "comprehensive_failure_simulation",
        total_data_points: testResults.totalTests + systemLogs.logAnalysis.total_error_events,
        simulation_realism: "high"
      }
    };
  }
}

// Export for use in n8n workflows
module.exports = AutomatosMockDataGenerator;

// For direct execution/testing
if (require.main === module) {
  const generator = new AutomatosMockDataGenerator();
  const dataset = generator.generateCompleteDataset();
  console.log(JSON.stringify(dataset, null, 2));
}


