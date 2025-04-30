#!/bin/bash

LOG_FILE=/var/www/html/repologs/rhel9.5/repo_sync_$(date +%Y.%m.%d).log

# Remove old logs
find /var/www/html/repologs/rhel9.5/repo_sync* -mtime +5 -delete; >> $LOG_FILE 2>&1
rm -rf /var/cache/dnf
# Sync repositories
/usr/bin/reposync -p /var/www/html/baseOS --download-metadata --repo=rhel-9-for-x86_64-baseos-rpms --newest-only >> $LOG_FILE 2>&1
sleep 2

/usr/bin/reposync -p /var/www/html/AppStream --download-metadata --repo=rhel-9-for-x86_64-appstream-rpms --newest-only   >> $LOG_FILE 2>&1

# cat /var/lib/containers/storage/overlay/4717c33822906e13a5ff7245fd1c535e32a58b7d4f2775ba301fbd443860434b/merged/opt/rhel9.5sync
