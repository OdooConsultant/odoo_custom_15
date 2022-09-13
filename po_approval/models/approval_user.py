# -*- coding: utf-8 -*-
from odoo import models, fields, _


class ApprovalUser(models.Model):
    _name = 'approval.user'

    user_ids = fields.Many2many('res.users', string='Users')
    from_amount = fields.Float('From Amount')
    to_amount = fields.Float('To Amount')
    approval_id = fields.Many2one('po.approval', 'Approval')
