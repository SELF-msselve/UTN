INSERT INTO http_events
SELECT  TO_TIMESTAMP(envoy_fields['timestamp'], 'yyyy-MM-dd''T''HH:mm:ss''Z''') AS event_ts,
        envoy_fields['method']                                                  AS http_method,
        CAST(envoy_fields['http_status'] AS INT)                                AS http_status
FROM (SELECT grok(`message`,'\[%{TIMESTAMP_ISO8601:timestamp}\] "%{DATA:method}" %{INT:http_status}') AS envoy_fields
        FROM envoy_raw)



INSERT INTO datos_agregados
SELECT window_start, window_end, http_method, COUNT(*) AS `count`
FROM TABLE(
    TUMBLE(TABLE http_events, descriptor(`event_ts`), INTERVAL '30' SECONDS))
GROUP BY window_start, window_end, http_method