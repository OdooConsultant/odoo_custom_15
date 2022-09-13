# -*- coding: utf-8 -*-
from odoo import models, fields, _


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    approval_id = fields.Many2one('po.approval', 'Approval Table')
