"""Read-only public TLS certificate checks; no mailbox credentials."""
import datetime
import json
import socket
import ssl
import urllib.request
for host in ['cln-performance.com', 'api.cln-performance.com']:
    with socket.create_connection((host, 443), timeout=20) as connection:
        with ssl.create_default_context().wrap_socket(connection, server_hostname=host) as secure:
            cert = secure.getpeercert()
    remaining = (ssl.cert_time_to_seconds(cert['notAfter']) - datetime.datetime.now(datetime.timezone.utc).timestamp()) / 86400
    print(json.dumps({'host':host,'notBefore':cert['notBefore'],'notAfter':cert['notAfter'],'daysRemaining':round(remaining,1),'issuer':cert['issuer'],'verified':True}), flush=True)
    if remaining <= 14:
        raise RuntimeError('Certificate close to expiration: ' + host)
