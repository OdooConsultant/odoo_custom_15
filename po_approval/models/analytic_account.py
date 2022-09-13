# -*- coding: utf-8 -*-
from odoo import models, fields, _


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    approval_id = fields.Many2one('po.approval', 'Approval Table')
