# Technical Architecture Notes

Author: Jane Smith
Date: December 3, 2025

## Current MarkLogic Architecture

### Cluster Configuration
- 3 E-nodes (evaluator nodes)
- Load balancer: AWS ELB
- Region: us-east-1
- Instance type: r5.2xlarge (64GB RAM each)

### Database Structure
- Content database: "documents-db"
- Modules database: "modules-db"
- Security database: default
- Schemas database: default

### Performance Characteristics
- Query throughput: 5000 queries/second average
- Peak load: 12000 queries/second
- Memory usage: 75-85% during peak hours
- Disk I/O: Write-heavy during ingestion windows

## Upgrade Considerations

### Compatibility Issues Found
1. Legacy XQuery syntax in 3 modules needs updating
2. Custom REST extension uses deprecated API
3. Index configuration format changed in v11

### Performance Improvements Expected
- 30% faster document ingestion with new indexing engine
- Improved memory management should reduce peak usage
- Better query optimization for complex searches

### Migration Steps
1. Backup all databases
2. Export configuration
3. Upgrade software on test cluster first
4. Validate custom code compatibility
5. Performance testing with production load
6. Schedule production upgrade

## Security Configuration

- TLS 1.2 minimum
- Certificate-based authentication for app servers
- Role-based access control (RBAC) configured
- Audit logging enabled for compliance
