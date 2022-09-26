# -*- coding: utf-8 -*-
from odoo import models, fields, _, api
from odoo.exceptions import ValidationError


class MultiApprovalUser(models.Model):
    _name = 'approval.user'

    user_ids = fields.Many2many('res.users', string='Users')
    required_second_approval = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Required 2nd Approver', default='no')
    second_approver_user_ids = fields.Many2many('res.users', 'new_approval_user', 'res_user', string='Second Approver Users')
    from_amount = fields.Monetary('From Amount', default=0.0)
    to_amount = fields.Monetary('To Amount')
    approval_id = fields.Many2one('multi.po.approval', 'Approval')
    currency_id = fields.Many2one(string='Currency', related="approval_id.currency_id", store=True)

    @api.constrains('from_amount', 'to_amount')
    def validate_on_to_amount(self):
        for record in self:
            if record.from_amount > record.to_amount:
                raise ValidationError("From amount should be less then To amount !")

    @api.onchange('required_second_approval')
    def onchnage_required_second_approval(self):
        if self.required_second_approval and self.required_second_approval != 'yes':
            self.second_approver_user_ids = [(6, 0, [])]
