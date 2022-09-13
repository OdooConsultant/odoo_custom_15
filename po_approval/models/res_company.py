# -*- coding: utf-8 -*-
from odoo import models, fields, _


class ResCompany(models.Model):
    _inherit = 'res.company'

    approval_id = fields.Many2one('po.approval', 'Approval Table')

