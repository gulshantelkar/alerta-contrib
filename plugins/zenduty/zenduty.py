import logging

# import os
# import re

import requests
from alerta.plugins import PluginBase

LOG = logging.getLogger("alerta.plugins.zenduty")

ZENDUTY_EVENTS_URL = "https://d344-103-174-71-214.ngrok-free.app/api/account/outgoing/alerta/webhook/2dbf673c-26ac-41b6-a344-13f8ea8ce918/"


class TriggerEvent(PluginBase):
    def pre_receive(self, alert):
        return alert

    def post_receive(self, alert):
        if alert.repeat:
            return

        message = "{}: {} alert for {} - {} is {}".format(
            alert.environment, alert.severity.capitalize(), ",".join(alert.service), alert.resource, alert.event
        )

        payload = {
            "incident_key": alert.id,
            "description": message,
            "client": "alerta",
            "status": alert.status,
            "details": alert.get_body(history=False),
        }

        LOG.debug("Zenduty payload: %s", payload)

        try:
            r = requests.post(ZENDUTY_EVENTS_URL, json=payload, timeout=2)
        except Exception as e:
            raise RuntimeError("Zenduty connection error: %s" % e)

        LOG.debug("Zenduty response: %s - %s", r.status_code, r.text)

    def status_change(self, alert, status, text):
        LOG.debug("status_change")
        if status not in ["ack", "assign", "closed", "expired"]:
            return

        payload = {
            "incident_key": alert.id,
            "description": text,
            "status": status,
            "details": alert.get_body(history=False),
        }

        LOG.debug("Zenduty payload: %s", payload)

        try:
            r = requests.post(ZENDUTY_EVENTS_URL, json=payload, timeout=2)
        except Exception as e:
            raise RuntimeError("Zenduty connection error: %s" % e)

        LOG.debug("Zenduty response: %s - %s", r.status_code, r.text)
    
    def post_action(self, alert, action, text, **kwargs):
        LOG.debug("status_change")
        if action not in ["ack", "assign", "closed", "expired"]:
            return

        payload = {
            "incident_key": alert.id,
            "description": text,
            "status": action,
            "details": alert.get_body(history=False),
        }

        LOG.debug("Zenduty payload: %s", payload)

        try:
            r = requests.post(ZENDUTY_EVENTS_URL, json=payload, timeout=2)
        except Exception as e:
            raise RuntimeError("Zenduty connection error: %s" % e)

        LOG.debug("Zenduty response: %s - %s", r.status_code, r.text)
