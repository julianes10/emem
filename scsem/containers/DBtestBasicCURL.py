curl -i -XPOST http://localhost:8086/query --data-urlencode "q=CREATE DATABASE db_ememTest"

curl -i -XPOST 'http://localhost:8086/write?db=db_ememTest' --data-binary 'temperature,sensor=atico value=1.1'

curl -i -XPOST 'http://localhost:8086/write?db=db_ememTest' --data-binary 'temperature,sensor=atico value=1.2'

curl -i -XPOST 'http://localhost:8086/write?db=db_ememTest' --data-binary 'temperature,sensor=atico value=1.3'

curl -G 'http://localhost:8086/query?pretty=true' --data-urlencode "db=db_ememTest" --data-urlencode "q=SELECT \"value\" FROM \"temperature\""

curl -i -XPOST http://localhost:8086/query --data-urlencode "q=DROP DATABASE db_ememTest"
