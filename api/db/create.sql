SELECT 'CREATE DATABASE lateshop'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'lateshop')\gexec

SELECT 'CREATE DATABASE lateshop_test'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'lateshop_test')\gexec

SELECT 'CREATE DATABASE lateshop_dev'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'lateshop_dev')\gexec

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
