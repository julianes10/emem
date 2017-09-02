curl -G 'http://localhost:8086/query?pretty=true' --data-urlencode "db=db_emem" --data-urlencode "q=SELECT * FROM \"temperature\""

echo "NUMBER OF RECORDS:"
curl -G 'http://localhost:8086/query?pretty=true' --data-urlencode "db=db_emem" --data-urlencode "q=SELECT COUNT(*) FROM \"temperature\""

