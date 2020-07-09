
from alerta.models.alert import Alert
from alerta.webhooks import WebhookBase
import json

SEVERITY_MAP = {
    '1': 'informational',       # Informational
    '2': 'warning',          # Warning
    '3': 'minor',        # Minor
    '4': 'major',  # Major
    '5': 'critical'           # Critical
}

DEFAULT_SEVERITY_LEVEL = '2'  # 'warning'


class OpenDistroWebhook(WebhookBase):

    def incoming(self, query_string, payload):

        # Default parameters
        environment = 'Production'
        group ='OpenDistro'
        text = ''
        tags = []
        attributes = {}
        origin = ''
        service=['OpenDistro Action']
        value = ''{}

        return Alert(
            resource=payload['resource'],
            event=payload['event'],
            environment=payload.get('environment', environment),
            severity=SEVERITY_MAP[payload.get('severity', DEFAULT_SEVERITY_LEVEL)],
            service=payload.get('service', service),
            group=payload.get('group', group),
            value=payload.get('value', value),
            text=payload.get('text', text),
            tags=payload.get('tags', tags),
            attributes=payload.get('attributes', attributes),
            origin=payload.get('origin', origin),
            raw_data=json.dumps(payload, indent=4)
        )
