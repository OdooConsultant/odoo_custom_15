# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class PoApproval(models.Model):
    _name = 'multi.po.approval'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'image.mixin']
    _description = "Multi Po Approval"

    name = fields.Char('Name', tracking=True)
    company_id = fields.Many2one('res.company', 'Company', tracking=True)
    currency_id = fields.Many2one(string='Currency', related="company_id.currency_id", store=True)
    approval_user_ids = fields.One2many('approval.user', 'approval_id', 'Approval Users')

    _sql_constraints = [
        ('name', 'unique (name)',
         "Name must be unique"),
    ]

    def write(self, vals):
        result = super(PoApproval, self).write(vals)
        for rec in self:
            count = 0
            last_amount = 0
            for app_user_id in rec.approval_user_ids:
                count += 1
                if count == 1:
                    app_user_id.from_amount = 0.0
                    last_amount = app_user_id.to_amount
                if count > 1:
                    app_user_id.from_amount = last_amount + 1
                    last_amount = app_user_id.to_amount
        return result

    @api.model
    def create(self, vals):
        result = super(PoApproval, self).create(vals)
        count = 0
        last_amount = 0
        for app_user_id in result.approval_user_ids:
            count += 1
            if count == 1:
                app_user_id.from_amount = 0.0
                last_amount = app_user_id.to_amount
            if count > 1:
                app_user_id.from_amount = last_amount + 1
                last_amount = app_user_id.to_amount
        return result
