# Automatos AI Testing Workflow Setup Guide

## Overview
This n8n workflow provides comprehensive automated testing and bug fixing for your Automatos AI platform. It runs tests in parallel, analyzes results with AI, generates and applies fixes, then re-tests until achieving 85% success rate.

## Prerequisites

### 1. n8n Server Setup
- n8n server running on your infrastructure
- SSH access to your testing server (142.93.49.20)
- Anthropic API key configured

### 2. Required Credentials in n8n

#### SSH Credential
- **Name:** `automatos_testing_ssh`
- **Type:** SSH Private Key
- **Host:** 142.93.49.20
- **Username:** root
- **Private Key:** Use your SSH private key (you mentioned ID: ttzZzSoAJhfPWARF)

#### Anthropic API Credential
- **Name:** `anthropic_api_key`
- **Type:** HTTP Header Auth
- **Name:** x-api-key
- **Value:** `Your-Key`

## Workflow Components

### 1. Test Execution Nodes (Parallel)
- **Agent Management Tests:** Runs comprehensive agent lifecycle tests
- **Workflow Management Tests:** Tests workflow orchestration and patterns
- **Document Management Tests:** Validates document processing and analytics
- **Context Engineering Tests:** Tests RAG system and embeddings
- **Performance Analytics Tests:** Monitors system metrics and performance

### 2. AI Analysis Pipeline
- **Bug Analysis Agent:** Uses Claude to analyze test failures and identify root causes
- **Fix Generation Agent:** Creates specific, implementable code fixes
- **Fix Implementation Agent:** Generates shell scripts to apply fixes safely

### 3. Automation Features
- **Parallel Test Execution:** All 5 test suites run simultaneously
- **Intelligent Fix Prioritization:** AI prioritizes fixes by impact
- **Automated Git Operations:** Creates branches, commits, and pushes fixes
- **Success Rate Monitoring:** Continues until 85% success rate achieved
- **Safety Limits:** Max 5 iterations to prevent infinite loops

## Key AI Agent Prompts

### Bug Analysis Agent Prompt
The AI analyzes test results and provides:
- Critical issues identification
- Root cause analysis
- Specific bug reports with severity levels
- Recommended fixes
- Testing strategies

**Requirements:**
- Only analyzes REAL test output (no fake issues)
- Provides specific, actionable recommendations
- Focuses on issues preventing 85% success rate

### Fix Generation Agent Prompt
Creates implementable fixes including:
- Exact file paths and line numbers
- Complete code implementations
- Configuration changes
- Database migrations if needed
- Testing instructions

**Requirements:**
- Follows existing code patterns
- Ensures backwards compatibility
- Includes error handling and logging

### Fix Implementation Agent Prompt
Generates safe shell scripts with:
- Git branch creation
- File backups before changes
- Precise file editing commands
- Individual commits per fix
- Error checking throughout

## Workflow Logic

### 1. Test Execution Flow
```
Scheduler (Every 4 Hours)
    ↓
[Parallel Test Execution]
    ├── Agent Tests
    ├── Workflow Tests  
    ├── Document Tests
    ├── Context Tests
    └── Performance Tests
    ↓
Merge & Analyze Results
    ↓
Success Rate >= 85%?
```

### 2. Fix Implementation Flow
```
Success Rate < 85%
    ↓
AI Bug Analysis
    ↓
Gather Detailed Test Results
    ↓
AI Fix Generation
    ↓
Parse & Structure Fixes
    ↓
AI Fix Implementation Script
    ↓
Execute Fixes via SSH
    ↓
Wait 30s → Re-run All Tests
    ↓
Continue if Success Rate < 85%
(Max 5 iterations)
```

### 3. Completion Flow
```
Success Rate >= 85%
    ↓
Send Success Report

OR

Major Issues Detected / Max Iterations
    ↓
Alert: Manual Intervention Required
```

## File Locations

### On Testing Server (142.93.49.20)
- **Application Code:** `/root/automatos-ai`
- **Testing Code:** `/root/automatos-testing`
- **Test Results:** `/tmp/*_test_results_*.log`
- **Detailed Results:** `/tmp/detailed_test_results_*.json`
- **Test Logs:** `/tmp/detailed_test_logs_*.txt`

### Test Output Structure
Each test generates:
- **Log Files:** Console output with exit codes
- **Result Files:** JSON reports in `phase*/results/`
- **Response Files:** API responses in `phase*/responses/`
- **Master Reports:** `MASTER_TEST_REPORT_*.json` and `MASTER_SUMMARY_*.md`

## Safety Features

### 1. Iteration Limits
- Maximum 5 fix iterations per workflow run
- Prevents infinite loops if issues persist

### 2. Major Issue Detection
Pauses testing and alerts for manual intervention if:
- Service connectivity issues (Connection refused, Service unavailable)
- Authentication/authorization failures
- Critical system failures (success rate < 30%)

### 3. Git Safety
- Creates feature branches for all fixes
- Backs up files before modification
- Individual commits per fix
- Never modifies main branch directly

### 4. Error Handling
- Comprehensive error checking in all scripts
- Graceful failure handling
- Detailed logging and reporting

## Monitoring & Alerting

### Success Webhooks
- **Success Report:** Sent when 85% success rate achieved
- **Completion Report:** Final status with metrics
- **Manual Intervention Alert:** When major issues detected

### Webhook Payloads
```json
{
  "status": "COMPLETED|REQUIRES_MANUAL_INTERVENTION",
  "timestamp": "2025-01-23T12:00:00.000Z",
  "finalSuccessRate": 87.5,
  "totalIterations": 3,
  "testResults": [...],
  "majorIssues": [...]
}
```

## Usage Instructions

### 1. Import Workflow
1. Copy the `automatos-testing-workflow.json` content
2. Import into your n8n instance
3. Configure the required credentials

### 2. Configure Schedule
- Default: Every 4 hours (`0 */4 * * *`)
- Modify the cron expression in the Scheduler node as needed

### 3. Test Manually
1. Execute the workflow manually first
2. Monitor the execution logs
3. Verify SSH connections work
4. Check AI agent responses

### 4. Monitor Results
- Set up webhook endpoints to receive alerts
- Monitor test success rates over time
- Review fix implementation logs

## Customization Options

### Adjust Success Threshold
Change the target success rate from 85% in:
- `check_success_rate` node condition
- `analyze_retest` function
- AI prompts mentioning the threshold

### Modify Test Schedule
Update the cron expression in the Scheduler node:
- Every 2 hours: `0 */2 * * *`
- Daily at 2 AM: `0 2 * * *`
- Every 30 minutes: `*/30 * * * *`

### Customize AI Prompts
Modify the prompt parameters in AI nodes to:
- Change analysis focus areas
- Adjust fix generation strategies
- Modify implementation approaches

## Troubleshooting

### Common Issues

1. **SSH Connection Failures**
   - Verify SSH key is correctly configured
   - Check server accessibility from n8n
   - Ensure root user has proper permissions

2. **AI API Errors**
   - Verify Anthropic API key is valid
   - Check API rate limits
   - Monitor token usage

3. **Test Execution Failures**
   - Check Python dependencies on testing server
   - Verify test configurations
   - Review server logs

4. **Git Operation Failures**
   - Ensure Git is configured on the server
   - Check repository permissions
   - Verify branch naming conventions

### Debug Mode
Enable verbose logging by adding `set -x` to SSH commands for detailed execution traces.

## Performance Considerations

### Resource Usage
- **Test Execution:** ~15-30 minutes for all suites
- **AI Analysis:** ~2-5 minutes per iteration
- **Fix Implementation:** ~1-3 minutes per fix set
- **Total Cycle Time:** 30-60 minutes per iteration

### Optimization Tips
- Run during low-traffic periods
- Monitor server resources during execution
- Adjust parallel execution if server is overloaded
- Consider splitting large test suites

## Security Considerations

### SSH Access
- Use dedicated SSH keys for automation
- Limit SSH user permissions to necessary directories
- Regularly rotate SSH keys

### API Keys
- Store securely in n8n credentials
- Monitor API usage and costs
- Set up alerts for unusual activity

### Code Safety
- All fixes create new branches
- Manual review recommended before merging
- Automated fixes are incremental, not wholesale changes

---

## Next Steps

1. **Initial Setup:** Configure credentials and import workflow
2. **Test Run:** Execute manually and verify all components work
3. **Schedule:** Enable automated scheduling
4. **Monitor:** Set up webhook endpoints and monitoring
5. **Optimize:** Adjust settings based on initial results

This workflow provides a comprehensive, automated testing and fixing pipeline that will continuously improve your Automatos AI platform's reliability and test coverage.