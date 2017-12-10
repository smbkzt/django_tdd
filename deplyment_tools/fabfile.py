from fabric.contrib.files import append, exists, sed
from fabric.api import cd, env, local, run
import random

REPO_URL = 'https://github.com/smbkzt/smbkzt.tk.git'


def deploy():
    site_folder = '/home/smbkzt/sites/104.131.115.175'
    run('mkdir -p 104.131.115.175')
    with cd(site_folder):
        _get_latest_source()
        _update_settings(env.host)
        _update_virtualenv()
        _update_static_files()
        _update_database()


def _get_latest_source():
    if exists('.git'):
        run('git fetch')
    else:
        run('git clone https://github.com/smbkzt/smbkzt.tk.git')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run('git reset --hard {current_commit}')


def _update_settings(site_name):
    settings_path = 'first_tdd/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        'ALLOWED_HOSTS = ["{site_name}"]'
        )


def _update_virtualenv():
    if not exists('virtualenv/bin/pip'):
        run('python3 -m venv virtualenv')
    run('./virtualenv/bin/pip install -r requirements.txt')


def _update_static_files():
    run('./virtualenv/bin/python manage.py collectstatic --noinput')


def _update_database():
    run('./virtualenv/bin/python manage.py migrate --noinput')
