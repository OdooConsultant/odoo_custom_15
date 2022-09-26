# -*- coding: utf-8 -*-
from odoo import models, fields, _


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    approval_id = fields.Many2one('multi.po.approval', 'Approval Table')
