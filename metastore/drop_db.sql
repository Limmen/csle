-- Connect to the csle db --
\connect csle

-- Drop the  CITUS extension --
DROP EXTENSION citus CASCADE ;

-- Try dropping the database --
DROP DATABASE csle

-- Forbid future connections --
REVOKE CONNECT ON DATABASE csle FROM public;

-- Remove active connections --
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = 'csle';
