import getpass

import boto3
from django.db.backends.postgresql import base

from django_iam_dbauth.utils import resolve_cname


class DatabaseWrapper(base.DatabaseWrapper):
    def get_connection_params(self):
        params = super().get_connection_params()
        enabled = params.pop('use_iam_auth', None)
        if enabled:
            rds_client = boto3.client("rds")

            hostname = params.get('host')
            hostname = resolve_cname(hostname) if hostname else "localhost"

            params["password"] = rds_client.generate_db_auth_token(
                DBHostname=hostname,
                Port=params.get("port", 5432),
                DBUsername=params.get("user") or getpass.getuser(),
            )

        return params
