-- Try Dropping the database --
DROP DATABASE csle WITH (FORCE) ;

-- Drop the  CITUS extension --
DROP EXTENSION citus CASCADE ;

-- Forbid future connections --
REVOKE CONNECT ON DATABASE csle FROM public;

-- Remove active connections --
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = 'csle';

-- Drop the database --
DROP DATABASE csle WITH (FORCE);
