# -*- coding: utf-8 -*-
from odoo import models, fields, _, api
from odoo.exceptions import ValidationError


class ApprovalUser(models.Model):
    _name = 'approval.user'

    user_ids = fields.Many2many('res.users', string='Users')
    from_amount = fields.Monetary('From Amount')
    to_amount = fields.Monetary('To Amount')
    approval_id = fields.Many2one('po.approval', 'Approval')
    currency_id = fields.Many2one(string='Currency', related="approval_id.currency_id", store=True)

    @api.constrains('from_amount', 'to_amount')
    def validate_on_to_amount(self):
        for record in self:
            if record.from_amount > record.to_amount:
                raise ValidationError("From amount should be less then To amount !")
