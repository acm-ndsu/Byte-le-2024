-- Database: byteserver

DROP DATABASE IF EXISTS byteserver;

DROP USER IF EXISTS byteuser;

CREATE USER byteuser WITH PASSWORD 'bytepassword';

CREATE DATABASE byteserver
    WITH
    OWNER = byteuser
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
--     LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

GRANT ALL ON DATABASE byteserver TO byteuser;