from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

from datetime import datetime, timedelta, date
from collections import namedtuple, OrderedDict, defaultdict


class ProductTemplate(models.Model):
    _inherit = "product.template"
    professor_ids = fields.Many2many(
                    'professor.professor','product_professor_rel', string="Professors")

