"""Deploy contact.php and private SMTP dependencies over pinned-key SFTP."""
import hashlib
import secrets
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
            smtp_password = os.environ.get('CLN_SMTP_PASSWORD')
            vendor = Path('deploy/mail/vendor')
            if not smtp_password:
                raise RuntimeError('Missing CLN_SMTP_PASSWORD; no file transferred')
            if not (vendor / 'autoload.php').is_file():
                raise RuntimeError('Missing built PHPMailer dependency')
            # Provision dependencies and credentials outside every public web root.
            def private_dir(path):
                import stat
                try:
                    entry = sftp.lstat(path)
                except FileNotFoundError:
                    sftp.mkdir(path, mode=0o700)
                    entry = sftp.lstat(path)
                if not stat.S_ISDIR(entry.st_mode):
                    raise RuntimeError('Private directory is not a real directory')
                sftp.chmod(path, 0o700)
            mail_root = home + '/.cln-mailer'
            private_dir(mail_root)
            release = mail_root + '/7.1.1'
            private_dir(release)
            for local in sorted(vendor.rglob('*')):
                relative = local.relative_to(vendor).as_posix()
                destination = release + '/' + relative
                if local.is_symlink():
                    raise RuntimeError('Unexpected dependency symlink')
                if local.is_dir():
                    private_dir(destination)
                elif local.is_file():
                    staged = destination + '.upload-' + uuid4().hex
                    data = local.read_bytes()
                    with sftp.open(staged, 'wb') as stream:
                        stream.write(data)
                    sftp.chmod(staged, 0o600)
                    with sftp.open(staged, 'rb') as stream:
                        if stream.read() != data:
                            raise RuntimeError('Dependency verification failed')
                    sftp.posix_rename(staged, destination)
            import json
            secret_root = home + '/.cln-secrets'
            private_dir(secret_root)
            staged_config = secret_root + '/.mail-' + uuid4().hex + '.json'
            config = {}
            if 'mail.json' in sftp.listdir(secret_root):
                with sftp.open(secret_root + '/mail.json', 'rb') as stream:
                    previous_config = stream.read()
                config = json.loads(previous_config)
                # Configuration backup remains private; never print its content.
                config_backup = secret_root + '/.mail-backup-' + uuid4().hex + '.json'
                with sftp.open(config_backup, 'wb') as stream:
                    stream.write(previous_config)
                sftp.chmod(config_backup, 0o600)
            config['password'] = smtp_password
            if not isinstance(config.get('security_key'), str) or len(config['security_key']) < 32:
                config['security_key'] = secrets.token_hex(32)
            helper = Path('contact_security.php').read_bytes()
            helper_tmp = secret_root + '/.security-' + uuid4().hex + '.php'
            with sftp.open(helper_tmp, 'wb') as stream:
                stream.write(helper)
            sftp.chmod(helper_tmp, 0o600)
            with sftp.open(helper_tmp, 'rb') as stream:
                if stream.read() != helper:
                    raise RuntimeError('Security helper verification failed')
            sftp.posix_rename(helper_tmp, secret_root + '/contact_security.php')
            config_data = json.dumps(config).encode('utf-8')
            with sftp.open(staged_config, 'wb') as stream:
                stream.write(config_data)
            sftp.chmod(staged_config, 0o600)
            with sftp.open(staged_config, 'rb') as stream:
                if stream.read() != config_data:
                    raise RuntimeError('Private configuration verification failed')
            sftp.posix_rename(staged_config, secret_root + '/mail.json')
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

