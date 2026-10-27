"""Deploy only contact.php over certificate-verified explicit FTPS."""
import hashlib
import io
import os
from pathlib import Path
import ssl
from ftplib import FTP_TLS, error_perm
from urllib.error import HTTPError
from urllib.request import urlopen
from uuid import uuid4


def deploy():
    source = Path('contact.php').read_bytes()
    password = os.environ.get('OVH_FTP_PASSWORD')
    if not password:
        raise RuntimeError('Missing OVH_FTP_PASSWORD repository secret')
    remote = 'contact.php'
    temporary = '.cln-upload-' + uuid4().hex + '.php'
    backup = None
    old = None
    with FTP_TLS(context=ssl.create_default_context(), timeout=30) as ftp:
        ftp.connect('ftp.cluster129.hosting.ovh.net', 21)
        ftp.login('nkzkafh', password)
        ftp.prot_p()
        home = ftp.pwd().rstrip('/')
        target = home + '/www'
        ftp.cwd(target)
        names = {name.rsplit('/', 1)[-1] for name in ftp.nlst()}
        if remote in names:
            buffer = io.BytesIO()
            ftp.retrbinary('RETR ' + remote, buffer.write)
            old = buffer.getvalue()
            ftp.cwd(home or '/')
            folder = '.cln-deploy-backups'
            try:
                ftp.mkd(folder)
            except error_perm:
                # Verify that the directory exists; do not ignore other errors.
                ftp.cwd(folder)
                ftp.cwd(home or '/')
            ftp.sendcmd('SITE CHMOD 700 ' + folder)
            backup = folder + '/contact-' + uuid4().hex + '.php'
            ftp.storbinary('STOR ' + backup, io.BytesIO(old))
            ftp.sendcmd('SITE CHMOD 600 ' + backup)
            check = io.BytesIO()
            ftp.retrbinary('RETR ' + backup, check.write)
            if check.getvalue() != old:
                raise RuntimeError('Backup verification failed; deployment stopped')
            ftp.cwd(target)
        ftp.storbinary('STOR ' + temporary, io.BytesIO(source))
        check = io.BytesIO()
        ftp.retrbinary('RETR ' + temporary, check.write)
        if hashlib.sha256(check.getvalue()).digest() != hashlib.sha256(source).digest():
            ftp.delete(temporary)
            raise RuntimeError('Upload verification failed')
        ftp.sendcmd('SITE CHMOD 644 ' + temporary)
        ftp.rename(temporary, remote)
        try:
            try:
                with urlopen('https://api.cln-performance.com/contact.php', timeout=30) as response:
                    status, headers = response.status, response.headers
            except HTTPError as response:
                status, headers = response.code, response.headers
                response.close()
            if status != 405 or headers.get('Allow') != 'POST':
                raise RuntimeError('PHP endpoint did not return the expected 405 / Allow: POST')
        except Exception:
            if old is None:
                ftp.delete(remote)
            else:
                rollback = '.cln-rollback-' + uuid4().hex + '.php'
                ftp.storbinary('STOR ' + rollback, io.BytesIO(old))
                ftp.sendcmd('SITE CHMOD 644 ' + rollback)
                ftp.rename(rollback, remote)
            raise
    print('PHP deployed and GET rejection verified. Mailbox delivery still requires testing.')
    if backup:
        print('Previous script backed up outside www in .cln-deploy-backups.')


if __name__ == '__main__':
    deploy()
