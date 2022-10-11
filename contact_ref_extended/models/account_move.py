# -*- coding: utf-8 -*-
from odoo import models, fields, _


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    customer_ref = fields.Char('Customer Reference',related="partner_id.ref")
