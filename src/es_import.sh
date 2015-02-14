curl -s -XPOST localhost:9200/_bulk --data-binary @probes/logs/cpu-log-proc.es
curl -s -XPOST localhost:9200/_bulk --data-binary @probes/logs/cpu-log-sys.es
curl -s -XPOST localhost:9200/_bulk --data-binary @probes/logs/io-log-sys.es
curl -s -XPOST localhost:9200/_bulk --data-binary @probes/logs/mem-log-proc.es
curl -s -XPOST localhost:9200/_bulk --data-binary @probes/logs/mem-log-sys.es
curl -s -XPOST localhost:9200/_bulk --data-binary @probes/logs/proc-log-errors.es
curl -s -XPOST localhost:9200/_bulk --data-binary @probes/logs/proc-log-info.es

