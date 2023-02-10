-- Connect to the csle db --
\connect csle

-- Setup citus coordinator node --
SELECT citus_set_coordinator_host('172.31.212.92', 5432);

-- Setup citus worker nodes --
SELECT citus_add_node('172.31.212.91', 5432);