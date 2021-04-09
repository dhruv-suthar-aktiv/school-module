from odoo import fields, models, api, _, modules

from datetime import datetime, timedelta
import base64


class ResPartner(models.Model):
    _inherit = "res.partner"


