#!/usr/bin/env sh
python -m admin_database.tool.init_database
if [ $? -ne 0 ]; then 
    exit 1
fi
alembic check > /tmp/alembic_check.log 2>&1
if [ $? -eq 0 ]; then 
    cat /tmp/alembic_check.log
    echo "🎉  Your database is up to date."
elif cat /tmp/alembic_check.log | grep "Target database is not up to date."; then
    cat /tmp/alembic_check.log
    echo "🚨  Your database is not up to date. Upgrading..."
    alembic upgrade head
else
    cat /tmp/alembic_check.log
    echo "❌  An error occurred while checking the database. The connection is very likely to be broken or impossible. Please check the above logs. As it can be a temporary issue, Docker will restart now to try again."
    exit 1
fi
echo "🍺  All logs are in /var/log/api"
echo "🚀  Starting gunicorn"
gunicorn --bind 0.0.0.0:8080 main:app --error-logfile /var/log/api/gunicorn_error.log --access-logfile /var/log/api/gunicorn_access.log --capture-output --enable-stdio-inheritance -k uvicorn.workers.UvicornWorker
echo "❌  If you see this, gunicorn has crashed. Check the logs (/var/log/api/gunicorn*.log)"