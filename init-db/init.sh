#!/bin/bash
set -e
psql --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" /docker-entrypoint-initdb.d/db_admin_dump4.sql
