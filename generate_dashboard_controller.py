#
# This module will generate "dashboard_controller.xlsx" Excel Spreadsheet with two workbooks:
# Dashboards:   Specifies which dashboards to generate
# Tiles:        Specifies the tiles to place in each dashboard (based on matching the "name" column)
#

import ast

from openpyxl import Workbook

from metric_dashboard_name_dictionary import METRIC_DASHBOARD_NAME_DICTIONARY

def main():
    # Use version file to obtain the version details
    with open('version.txt', 'r') as file:
        version = file.read()
    print('version: ' + version)

    infile = open('metrics.txt', 'r')
    outfile_name= 'dashboard_controller.xlsx'

    metric_details_read = 0
    metrics_written = 0
    metrics_skipped = 0

    DASHBOARD_ID_PREFIX = 'aaaaaaaa-bbbb-cccc-dddd-'
    DASHBOARD_OWNER = 'dave.mauney@dynatrace.com'
    DASHBOARD_CLUSTER_VERSION = version
    DASHBOARD_CONFIGURATION_VERSIONS = '3'
    DASHBOARD_SHARED = 'true'
    DASHBOARD_LINK_SHARED = 'true'
    DASHBOARD_PUBLISHED = 'true'
    DASHBOARD_TIMEFRAME = ''
    DASHBOARD_MANAGEMENT_ZONE = 'null'
    DASHBOARD_PROCESS = 'true'
    # 5 tiles = 1520
    # 6 tiles = 1824
    # DASHBOARD_WIDTH=1520
    DASHBOARD_WIDTH = 1824
    DASHBOARD_HEIGHT = 5016
    dashboard_id = 1

    overview_applications_markdown = '[Applications](#dashboard/dashboard;id=aaaaaaaa-bbbb-cccc-dddd-$$ID$$)'
    overview_synthetics_markdown = '[Synthetics](#dashboard;id=aaaaaaaa-bbbb-cccc-dddd-$$ID$$)'
    overview_services_markdown = '[Services](#dashboard;id=aaaaaaaa-bbbb-cccc-dddd-$$ID$$)'
    overview_databases_markdown = '[Databases](#dashboard;id=aaaaaaaa-bbbb-cccc-dddd-$$ID$$)'
    overview_hosts_markdown = '[Hosts](#dashboard;id=aaaaaaaa-bbbb-cccc-dddd-$$ID$$)'
    overview_processes_markdown = '[Processes](#dashboard;id=aaaaaaaa-bbbb-cccc-dddd-$$ID$$)'
    overview_java_markdown = '[Java Monitoring](#dashboard;id=aaaaaaaa-bbbb-cccc-dddd-$$ID$$)'
    overview_net_markdown = '[.Net Monitoring](#dashboard;id=aaaaaaaa-bbbb-cccc-dddd-$$ID$$)'
    overview_tomcat_markdown = '[Tomcat Monitoring](#dashboard;id=aaaaaaaa-bbbb-cccc-dddd-$$ID$$)'

    wb = Workbook()
    dashboards = wb.active
    dashboards.title = 'Dashboards'
    dashboards.append(
        ['name', 'id', 'owner', 'clusterVersion', 'configurationVersions', 'shared', 'linkShared', 'published', 'timeframe',
         'managementZone', 'process', 'width', 'height'])
    tiles = wb.create_sheet(title='Tiles')
    tiles.append(['name', 'tileType', 'metric', 'customName', 'aggregation', 'type', 'entityType', 'filterType',
                  'dimensionDefinition', 'displayName', 'description', 'unit', 'width', 'height'])

    # Save workbook just to be sure to get a lock on it before all the processing...
    wb.save(filename=outfile_name)

    previous_name = ''

    while True:
        line = infile.readline()

        if not line:
            break

        metric_details_dictionary = ast.literal_eval(line)
        metric_details_read += 1
        metric_id = metric_details_dictionary.get('metricId')

        # Use starts with 'builtin:' to process everything...
        # Otherwise, comment it out and pick a specific set of metrics
        if metric_id.startswith('builtin:'):
            # if metricId.startswith('builtin:host') or metricId.startswith('builtin:tech.generic') or metricId.startswith('builtin:synthetic') or metricId.startswith('builtin:service'):
            # if metricId.startswith('builtin:service'):
            # if metricId.startswith('builtin:tech.jvm'):
            # if metricId.startswith('builtin:tech.dotnet'):
            # if metricId.startswith('builtin:tech.cassandra'):
            # if metricId.startswith('builtin:tech.elastic'):
            # if metricId.startswith('builtin:cloud.aws'):
            # if metricId.startswith('builtin:cloud.azure'):
            # if metricId.startswith('builtin:cloud.vmware'):
            # if metricId.startswith('builtin:apps.other'):
            # if metricId.startswith('builtin:containers'):
            # if metricId.startswith('builtin:tech.couchbase'):
            # if metricId.startswith('builtin:tech.rabbitmq'):
            # if metricId.startswith('builtin:tech.Hadoop'):
            # if metricId.startswith('builtin:tech.kafka'):
            # if metricId.startswith('builtin:tech.oracleDb'):
            # if metricId.startswith('builtin:tech.customDevice'):
            # if metricId.startswith('builtin:nam'):
            # if metricId.startswith('builtin:cloud.aws') or metricId.startswith('builtin:tech.customDevice') or metricId.startswith('builtin:nam'):
            # print('passing')
            pass
        else:
            metrics_skipped += 1
            print('Skipping: ' + metric_id + ' because it is blacklisted currently')
            # print('continuing')
            continue

        '''
        Skip Synthetic 'geo' metrics since they require more than one dimension to be useful
        Also, the Synthetic dashboard exceeds the size limit of 5016 x 5016 if they are included
        '''
        if metric_id.startswith('builtin:synthetic') and metric_id.endswith('.geo'):
            metrics_skipped += 1
            print('Skipping: ' + metric_id + ' because it is a synthetic metric with a geo dimension')
            continue

        customName = metric_details_dictionary.get('displayName')

        # Fix non-utf-8 characters in some Solr customName values
        if customName.startswith('Solr '):
            customName = str(bytes(customName, 'ascii', 'replace').decode('utf-8')).replace('?', ' ')

        categories = metric_id.split('.', 2)
        name = 'UNKNOWN'
        key = categories[0] + '.' + categories[1]
        if key in METRIC_DASHBOARD_NAME_DICTIONARY.keys():
            name = METRIC_DASHBOARD_NAME_DICTIONARY.get(key)
        else:
            key = categories[0]
            if key in METRIC_DASHBOARD_NAME_DICTIONARY.keys():
                name = METRIC_DASHBOARD_NAME_DICTIONARY.get(key)

        BAD_METRICS = {'builtin:tech.generic.count',
                       'builtin:tech.cassandra.RangeSlice.Latency.95thPercentile',
                       'builtin:tech.cassandra.Read.Latency.95thPercentile',
                       'builtin:tech.cassandra.Write.Latency.95thPercentile'
                       }

        default_aggregation = metric_details_dictionary.get('defaultAggregation', {'type': 'None'}).get('type', 'None').upper()
        default_aggregation = default_aggregation.replace('VALUE', 'NONE')

        if metric_id in BAD_METRICS or metric_id.startswith('builtin:billing'):
            metrics_skipped += 1
            print('Skipping: ' + metric_id + ' because it is considered a bad metric currently')
            continue

        if '#' in metric_id or '%' in metric_id:
            metrics_skipped += 1
            print('Skipping: ' + metric_id + ' because it contains an invalid character (#, or %)')
            continue

        entity_type = metric_details_dictionary.get('entityType', ['None'])[0]

        BAD_ENTITIES = {
            'SERVICE_METHOD_GROUP'
        }

        if entity_type in BAD_ENTITIES:
            metrics_skipped += 1
            print('Skipping: ' + metric_id + ' because it has a bad entity: ' + entity_type)
            continue

        if entity_type == 'AWS_APPLICATION_LOAD_BALANCER':
            entity_type = 'ALB'
        if entity_type == 'ELASTIC_LOAD_BALANCER':
            entity_type = 'ELB'
        if entity_type == 'AWS_NETWORK_LOAD_BALANCER':
            entity_type = 'NLB'
        if entity_type == 'AUTO_SCALING_GROUP':
            entity_type = 'ASG'
        if entity_type == 'DYNAMO_DB_TABLE':
            entity_type = 'DYNAMO_DB'
        if entity_type == 'EBS_VOLUME':
            entity_type = 'EBS'
        if entity_type == 'EC2_INSTANCE':
            entity_type = 'EC2'
        if entity_type == 'RELATIONAL_DATABASE_SERVICE':
            entity_type = 'RDS'

        if entity_type == 'CUSTOM_DEVICE':
            entity_type = 'IOT'
        if entity_type == 'PROCESS_GROUP':
            entity_type = 'PROCESS_GROUP_INSTANCE'

        dimension_definition = 'dt.entity.' + entity_type.lower()

        if entity_type.startswith('AZURE_'):
            entity_type = entity_type.replace('AZURE_', 'MONITORED_ENTITY\\u02dfAZURE_')

        if entity_type == 'CUSTOM_DEVICE_GROUP':
            entity_type = 'MONITORED_ENTITY\\u02dfCUSTOM_DEVICE_GROUP'

        if entity_type == 'DCRUM_SERVICE':
            entity_type = 'DCRUM_ENTITY'

        if entity_type == 'HYPERVISOR':
            entity_type = 'ESXI'
        if entity_type == 'NETWORK_INTERFACE':
            entity_type = 'MONITORED_ENTITY\\u02dfNETWORK_INTERFACE'
        if entity_type == 'VIRTUALMACHINE':
            entity_type = 'VIRTUAL_MACHINE'

        if entity_type == 'DOCKER_CONTAINER_GROUP_INSTANCE':
            entity_type = 'MONITORED_ENTITY\\u02dfDOCKER_CONTAINER_GROUP_INSTANCE'

        if entity_type == 'SERVICE_METHOD':
            entity_type = 'SERVICE_KEY_REQUEST'
        if entity_type == 'HTTP_CHECK':
            entity_type = 'SYNTHETIC_HTTPCHECK'
        if entity_type == 'HTTP_CHECK_STEP':
            entity_type = 'SYNTHETIC_HTTPCHECK_STEP'

        GLOBAL_BACKGROUND_ACTIVITY = {
            'builtin:tech.generic.cpu.groupSuspensionTime',
            'builtin:tech.generic.cpu.groupTotalTime',
            'builtin:tech.elasticsearch.local.indices.query_cache.cache_count',
            'builtin:tech.elasticsearch.local.indices.query_cache.cache_size',
            'builtin:tech.elasticsearch.local.indices.query_cache.evictions',
            'builtin:tech.elasticsearch.local.indices.segments.count',
            'builtin:tech.elasticsearch.local.number_of_data_nodes',
            'builtin:tech.elasticsearch.local.number_of_nodes',
            'builtin:tech.elasticsearch.local.status-green',
            'builtin:tech.elasticsearch.local.status-red',
            'builtin:tech.elasticsearch.local.status-unknown',
            'builtin:tech.elasticsearch.local.status-yellow',
            'builtin:tech.elasticsearch.local.unassigned_shards',
            'builtin:tech.Hadoop.hdfs.BlocksTotal',
            'builtin:tech.Hadoop.hdfs.CacheCapacity',
            'builtin:tech.Hadoop.hdfs.CacheUsed',
            'builtin:tech.Hadoop.hdfs.CapacityRemaining',
            'builtin:tech.Hadoop.hdfs.CapacityTotal',
            'builtin:tech.Hadoop.hdfs.CapacityUsed',
            'builtin:tech.Hadoop.hdfs.CapacityUsedNonDFS',
            'builtin:tech.Hadoop.hdfs.CorruptBlocks',
            'builtin:tech.Hadoop.hdfs.EstimatedCapacityLostTotal',
            'builtin:tech.Hadoop.hdfs.FilesAppended',
            'builtin:tech.Hadoop.hdfs.FilesCreated',
            'builtin:tech.Hadoop.hdfs.FilesDeleted',
            'builtin:tech.Hadoop.hdfs.FilesRenamed',
            'builtin:tech.Hadoop.hdfs.FilesTotal',
            'builtin:tech.Hadoop.hdfs.NumberOfMissingBlocks',
            'builtin:tech.Hadoop.hdfs.NumDeadDataNodes',
            'builtin:tech.Hadoop.hdfs.NumDecomDeadDataNodes',
            'builtin:tech.Hadoop.hdfs.NumDecomLiveDataNodes',
            'builtin:tech.Hadoop.hdfs.NumDecommissioningDataNodes',
            'builtin:tech.Hadoop.hdfs.NumLiveDataNodes',
            'builtin:tech.Hadoop.hdfs.NumStaleDataNodes',
            'builtin:tech.Hadoop.hdfs.PendingDeletionBlocks',
            'builtin:tech.Hadoop.hdfs.PendingReplicationBlocks',
            'builtin:tech.Hadoop.hdfs.ScheduledReplicationBlocks',
            'builtin:tech.Hadoop.hdfs.TotalLoad',
            'builtin:tech.Hadoop.hdfs.UnderReplicatedBlocks',
            'builtin:tech.Hadoop.hdfs.VolumeFailuresTotal',
            'builtin:tech.Hadoop.yarn.AllocatedContainers',
            'builtin:tech.Hadoop.yarn.AllocatedMB',
            'builtin:tech.Hadoop.yarn.AllocatedVCores',
            'builtin:tech.Hadoop.yarn.AppsCompleted',
            'builtin:tech.Hadoop.yarn.AppsFailed',
            'builtin:tech.Hadoop.yarn.AppsKilled',
            'builtin:tech.Hadoop.yarn.AppsPending',
            'builtin:tech.Hadoop.yarn.AppsRunning',
            'builtin:tech.Hadoop.yarn.AppsSubmitted',
            'builtin:tech.Hadoop.yarn.AvailableMB',
            'builtin:tech.Hadoop.yarn.AvailableVCores',
            'builtin:tech.Hadoop.yarn.NumActiveNMs',
            'builtin:tech.Hadoop.yarn.NumDecommissionedNMs',
            'builtin:tech.Hadoop.yarn.NumLostNMs',
            'builtin:tech.Hadoop.yarn.NumRebootedNMs',
            'builtin:tech.Hadoop.yarn.NumUnhealthyNMs',
            'builtin:tech.Hadoop.yarn.PendingMB',
            'builtin:tech.Hadoop.yarn.PendingVCores',
            'builtin:tech.Hadoop.yarn.ReservedMB',
            'builtin:tech.Hadoop.yarn.ReservedVCores',
            'builtin:tech.kafka.pg.kafka.controller.ControllerStats.LeaderElectionRateAndTimeMs.OneMinuteRate',
            'builtin:tech.kafka.pg.kafka.controller.ControllerStats.UncleanLeaderElectionsPerSec.OneMinuteRate',
            'builtin:tech.kafka.pg.kafka.controller.KafkaController.ActiveControllerCount.Value',
            'builtin:tech.kafka.pg.kafka.controller.KafkaController.OfflinePartitionsCount.Value',
            'builtin:tech.kafka.pg.kafka.server.ReplicaManager.PartitionCount.Value',
            'builtin:tech.kafka.pg.kafka.server.ReplicaManager.UnderReplicatedPartitions.Value'
        }

        if metric_id in GLOBAL_BACKGROUND_ACTIVITY or metric_id.startswith(
                'builtin:tech.jvm.spark') or 'shards' in metric_id or 'indices.count' in metric_id or 'indices.docs' in metric_id or 'indices.fielddata' in metric_id or metric_id.startswith(
                'builtin:tech.couchbase') or metric_id.startswith('builtin:tech.rabbitmq.topN') or metric_id.startswith(
                'builtin:tech.rabbitmq.cluster'):
            entity_type = 'GLOBAL_BACKGROUND_ACTIVITY'
            dimension_definition = 'dt.entity.process_group'
        if metric_id.startswith(
                'builtin:tech.jvm.spark.worker.cores') or metric_id == 'builtin:tech.jvm.spark.worker.executors' or metric_id.startswith(
                'builtin:tech.jvm.spark.worker.mem') or metric_id.startswith('builtin:tech.couchbase.node'):
            entity_type = 'PROCESS_GROUP_INSTANCE'
        if metric_id == 'builtin:synthetic.external.step.responseTime':
            entity_type = 'MONITORED_ENTITY\\u02dfEXTERNAL_SYNTHETIC_TEST_STEP'
            dimension_definition = 'dt.entity.external_synthetic_test_step'
        if metric_id.startswith('builtin:apps.other'):
            if metric_id == 'builtin:apps.other.keyUserActions.apdexValue.os' or metric_id == 'builtin:apps.other.keyUserActions.count.osAndApdex' or metric_id.startswith(
                    'builtin:apps.other.keyUserActions'):
                entity_type = 'MONITORED_ENTITY\\u02dfDEVICE_APPLICATION_METHOD'
                dimension_definition = 'dt.entity.device_application_method'
            else:
                entity_type = 'MONITORED_ENTITY\\u02dfDEVICE_APPLICATION'
                dimension_definition = 'dt.entity.device_application'

        tiles.append([name, 'CUSTOM_CHARTING', metric_id, customName, default_aggregation, 'TIMESERIES', entity_type, 'MIXED',
                      dimension_definition, metric_details_dictionary.get('displayName', ''),
                      metric_details_dictionary.get('description', ''), metric_details_dictionary.get('unit'), '304', '304'])

        if name != previous_name:
            new_id = format(dashboard_id, '012d')
            dashboards.append(
                [name, DASHBOARD_ID_PREFIX + new_id, DASHBOARD_OWNER, DASHBOARD_CLUSTER_VERSION,
                 DASHBOARD_CONFIGURATION_VERSIONS, DASHBOARD_SHARED, DASHBOARD_LINK_SHARED, DASHBOARD_PUBLISHED,
                 DASHBOARD_TIMEFRAME, DASHBOARD_MANAGEMENT_ZONE, DASHBOARD_PROCESS, DASHBOARD_WIDTH, DASHBOARD_HEIGHT])
            previous_name = name

            # Configure the dashboard links used for the Overview markdown tiles
            if name == 'Web Applications':
                overview_applications_markdown = overview_applications_markdown.replace('$$ID$$', new_id)
            if name == 'Synthetics':
                overview_synthetics_markdown = overview_synthetics_markdown.replace('$$ID$$', new_id)
            if name == 'Services':
                overview_services_markdown = overview_services_markdown.replace('$$ID$$', new_id)
            #if name == 'Databases':
            #    overview_databases_markdown = overview_databases_markdown.replace('$$ID$$', new_id)
            if name == 'Hosts':
                overview_hosts_markdown = overview_hosts_markdown.replace('$$ID$$', new_id)
            if name == 'Processes':
                overview_processes_markdown = overview_processes_markdown.replace('$$ID$$', new_id)
            if name == 'Java':
                overview_java_markdown = overview_java_markdown.replace('$$ID$$', new_id)
            if name == '.NET':
                overview_net_markdown = overview_net_markdown.replace('$$ID$$', new_id)
            if name == 'Tomcat':
                overview_tomcat_markdown = overview_tomcat_markdown.replace('$$ID$$', new_id)

            dashboard_id += 1

        metrics_written += 1

    # Generate Overview Rows on both worksheets
    dashboards.append(['Overview', DASHBOARD_ID_PREFIX + format(dashboard_id, '012d'), DASHBOARD_OWNER, DASHBOARD_CLUSTER_VERSION,
         DASHBOARD_CONFIGURATION_VERSIONS, DASHBOARD_SHARED, DASHBOARD_LINK_SHARED, DASHBOARD_PUBLISHED,
         DASHBOARD_TIMEFRAME, DASHBOARD_MANAGEMENT_ZONE, DASHBOARD_PROCESS, DASHBOARD_WIDTH,
         DASHBOARD_HEIGHT])
    dashboard_id += 1
    tiles.append(['Overview', 'MARKDOWN', overview_applications_markdown, '', '', '', '', '', '', '', '', '', '304', '38'])
    tiles.append(['Overview', 'MARKDOWN', overview_synthetics_markdown, '', '', '', '', '', '', '', '', '', '304', '38'])
    tiles.append(['Overview', 'MARKDOWN', overview_services_markdown, '', '', '', '', '', '', '', '', '', '304', '38'])
    tiles.append(['Overview', 'MARKDOWN', overview_databases_markdown, '', '', '', '', '', '', '', '', '', '304', '38'])
    tiles.append(['Overview', 'MARKDOWN', overview_hosts_markdown, '', '', '', '', '', '', '', '', '', '304', '38'])
    tiles.append(['Overview', 'HOSTS', '', '', '', '', '', '', '', '', '', '', '304', '304'])
    tiles.append(['Overview', 'SERVICES', '', '', '', '', '', '', '', '', '', '', '304', '304'])
    tiles.append(['Overview', 'APPLICATIONS', '', '', '', '', '', '', '', '', '', '', '304', '304'])
    tiles.append(['Overview', 'DATABASES_OVERVIEW', '', '', '', '', '', '', '', '', '', '', '304', '304'])
    tiles.append(['Overview', 'SYNTHETIC_TESTS', '', '', '', '', '', '', '', '', '', '', '304', '304'])
    overview_more_details_markdown = 'More Details\\n\\n' + overview_processes_markdown + '\\n\\n' + overview_java_markdown + '\\n\\n' + overview_net_markdown + '\\n\\n' + overview_tomcat_markdown
    print(overview_more_details_markdown)
    tiles.append(['Overview', 'MARKDOWN',overview_more_details_markdown, '', '', '', '', '', '', '', '', '', '304', '304'])

    wb.save(filename=outfile_name)

    print('Metrics Read:    ' + str(metric_details_read))
    print('Metrics Written: ' + str(metrics_written))
    print('Metrics Skipped: ' + str(metrics_skipped))

    print('Output File Name:' + outfile_name)

    infile.close()

if __name__ == '__main__':
    main()