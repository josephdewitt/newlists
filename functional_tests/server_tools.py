from fabric.api import run
from fabric.context_managers import settings


def _get_manage_dot_py(host):
    return '~/sites/%s/virtualenv/bin/python ~/sites/%s/source/manage.py' % host


def reset_database(host):
    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string='joseph@' + '%s' % host):
        run( '%s' % manage_dot_py + 'flush --noinput')


def create_session_on_server(host, email):
    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string='joseph@' + '%s' % host):
        session_key = run('%s' % manage_dot_py + 'create_session %s' % email)
        return session_key.strip()