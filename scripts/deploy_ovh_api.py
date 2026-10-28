"""Deploy only contact.php via SFTP with a pinned server identity."""
import hashlib
import io
import os
from pathlib import Path
import ssl
from urllib.error import HTTPError
from urllib.request import urlopen
from uuid import uuid4
import paramiko

HOST = 'ftp.cluster129.hosting.ovh.net'
USER = 'nkzkafh'

def deploy():
    source = Path('contact.php').read_bytes()
    hosts = Path('deploy/ovh_known_hosts')
    if not hosts.is_file():
        raise RuntimeError('Missing reviewed deploy/ovh_known_hosts; no password transmitted')
    password = os.environ.get('OVH_FTP_PASSWORD')
    if not password:
        raise RuntimeError('Missing OVH_FTP_PASSWORD repository secret')
    with paramiko.SSHClient() as client:
        client.load_host_keys(str(hosts))
        client.set_missing_host_key_policy(paramiko.RejectPolicy())
        client.connect(HOST, port=22, username=USER, password=password,
                       look_for_keys=False, allow_agent=False, timeout=30,
                       auth_timeout=30, banner_timeout=30)
        with client.open_sftp() as sftp:
            home = sftp.normalize('.').rstrip('/')
            target = home + '/www'
            remote = target + '/contact.php'
            temporary = target + '/.cln-upload-' + uuid4().hex + '.php'
            old = None
            if 'contact.php' in sftp.listdir(target):
                with sftp.open(remote, 'rb') as stream:
                    old = stream.read()
                folder = home + '/.cln-deploy-backups'
                if '.cln-deploy-backups' not in sftp.listdir(home):
                    sftp.mkdir(folder, mode=0o700)
                sftp.chmod(folder, 0o700)
                backup = folder + '/contact-' + uuid4().hex + '.php'
                with sftp.open(backup, 'wb') as stream:
                    stream.write(old)
                sftp.chmod(backup, 0o600)
                with sftp.open(backup, 'rb') as stream:
                    if stream.read() != old:
                        raise RuntimeError('Backup verification failed')
            with sftp.open(temporary, 'wb') as stream:
                stream.write(source)
            with sftp.open(temporary, 'rb') as stream:
                if hashlib.sha256(stream.read()).digest() != hashlib.sha256(source).digest():
                    sftp.remove(temporary)
                    raise RuntimeError('Upload verification failed')
            sftp.chmod(temporary, 0o644)
            # Require atomic POSIX replacement; fail safely if unsupported.
            sftp.posix_rename(temporary, remote)
            try:
                try:
                    with urlopen('https://api.cln-performance.com/contact.php', timeout=30,
                                 context=ssl.create_default_context()) as response:
                        status, headers = response.status, response.headers
                except HTTPError as response:
                    status, headers = response.code, response.headers
                    response.close()
                if status != 405 or headers.get('Allow') != 'POST':
                    raise RuntimeError('Expected 405 / Allow: POST')
            except Exception:
                if old is None:
                    sftp.remove(remote)
                else:
                    rollback = target + '/.cln-rollback-' + uuid4().hex + '.php'
                    with sftp.open(rollback, 'wb') as stream:
                        stream.write(old)
                    sftp.chmod(rollback, 0o644)
                    sftp.posix_rename(rollback, remote)
                raise
    print('SFTP deployment and GET rejection verified. Mail delivery still requires testing.')

if __name__ == '__main__':
    deploy()
