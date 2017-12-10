from fabric.contrib.files import append, exists, sed
from fabric.api import cd, env, local, run
import random

REPO_URL = 'https://github.com/smbkzt/smbkzt.tk.git'


def deploy():

    site_folder = '/home/smbkzt/sites/{0}'.format(env.host)
    run('mkdir -p {0}'.format(site_folder))
    with cd(site_folder):
        _get_latest_source()
        _update_settings(env.host)
        _update_static_files()
        _update_database()


def _get_latest_source():
    if exists('.git'):
        run('git fetch')
    else:
        run('git clone {0} .'.format(REPO_URL))
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run('git reset --hard {0}'.format(current_commit))


def _update_settings(site_name):
    settings_path = 'first_tdd/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        'ALLOWED_HOSTS = ["{0}"]'.format(site_name)
        )

    secret_key_file = 'first_tdd/secret_key.py'
    if not exists(secret_key_file):
        key = ''.join([random.SystemRandom().choice(
            'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
            ) for i in range(50)])
        append(secret_key_file, 'SECRET_KEY = "{0}"'.format(key))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv():
    if not exists('tddenv/bin/pip'):
        run('python3 -m venv tddenv')
    run('./tddenv/bin/pip install -r requirements.txt')


def _update_static_files():
    run('./tddenv/bin/python3 manage.py collectstatic --noinput')


def _update_database():
    run('./tddenv/bin/python3 manage.py migrate --noinput')
