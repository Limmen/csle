--  Create csle db if not exists --
SELECT 'CREATE DATABASE csle'
    WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'csle')\gexec

-- Connect to the csle db --
    \connect csle

-- Create CITUS extension --
CREATE EXTENSION citus;