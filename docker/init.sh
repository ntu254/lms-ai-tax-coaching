#!/bin/bash

# Configure MariaDB client to disable SSL requirement
printf "[client]\nskip-ssl\n[mariadb-client]\nskip-ssl\n" > ~/.my.cnf

if [ -d "/home/frappe/frappe-bench/apps/frappe" ] && [ -d "/home/frappe/frappe-bench/sites/lms.localhost" ]; then
    echo "Bench and site already exist, skipping init"
    cd frappe-bench
    bench start
    exit 0
fi

echo "Creating new bench..."

export PATH="${NVM_DIR}/versions/node/v${NODE_VERSION_DEVELOP}/bin/:${PATH}"

if [ ! -d "/home/frappe/frappe-bench" ]; then
    bench init --skip-redis-config-generation frappe-bench
fi

cd frappe-bench

# Use containers instead of localhost
bench set-mariadb-host mariadb
bench set-redis-cache-host redis://redis:6379
bench set-redis-queue-host redis://redis:6379
bench set-redis-socketio-host redis://redis:6379

# Remove redis, watch from Procfile
sed -i '/redis/d' ./Procfile
sed -i '/watch/d' ./Procfile
sed -i 's/bench serve/bench serve --host 0.0.0.0/' ./Procfile

if [ ! -d "apps/payments" ]; then
    bench get-app payments
fi

if [ ! -d "apps/lms" ]; then
    bench get-app lms
fi

bench new-site lms.localhost \
--force \
--mariadb-root-password 123 \
--admin-password admin \
--mariadb-user-host-login-scope='%'

bench --site lms.localhost install-app payments
bench --site lms.localhost install-app lms
bench --site lms.localhost set-config developer_mode 1

# Configure Vietnam localization & Vietnamese translations
if [ -f "/workspace/vietnam_setup.py" ]; then
    /home/frappe/frappe-bench/env/bin/python /workspace/vietnam_setup.py
fi
if [ -f "/workspace/apply_vietnamese.py" ]; then
    /home/frappe/frappe-bench/env/bin/python /workspace/apply_vietnamese.py
fi
if [ -f "/workspace/expand_translations.py" ]; then
    /home/frappe/frappe-bench/env/bin/python /workspace/expand_translations.py
fi
if [ -f "/workspace/update_comprehensive_vietnamese.py" ]; then
    /home/frappe/frappe-bench/env/bin/python /workspace/update_comprehensive_vietnamese.py
fi
if [ -f "/workspace/translate_forms_and_sections.py" ]; then
    /home/frappe/frappe-bench/env/bin/python /workspace/translate_forms_and_sections.py
fi
if [ -f "/workspace/translate_course_pricing_related.py" ]; then
    /home/frappe/frappe-bench/env/bin/python /workspace/translate_course_pricing_related.py
fi
if [ -f "/workspace/translate_statistics.py" ]; then
    /home/frappe/frappe-bench/env/bin/python /workspace/translate_statistics.py
fi
if [ -f "/workspace/translate_jobs_and_empty_states.py" ]; then
    /home/frappe/frappe-bench/env/bin/python /workspace/translate_jobs_and_empty_states.py
fi
if [ -f "/workspace/translate_payment_settings.py" ]; then
    /home/frappe/frappe-bench/env/bin/python /workspace/translate_payment_settings.py
fi
if [ -f "/workspace/init_users.py" ]; then
    /home/frappe/frappe-bench/env/bin/python /workspace/init_users.py
fi

bench --site lms.localhost clear-cache
bench use lms.localhost

bench start
