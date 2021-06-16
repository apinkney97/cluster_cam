#1/bin/bash
set -x

for host in p1 p2 p3 p4
do
	ssh $host sudo halt || :
done

sleep 30

clusterctrl off

# sleep 5
# sudo halt

