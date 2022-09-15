# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class PoApproval(models.Model):
    _name = 'po.approval'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'image.mixin']
    _description = "Po Approval"

    name = fields.Char('Name', tracking=True)
    company_id = fields.Many2one('res.company', 'Company', tracking=True)
    currency_id = fields.Many2one(string='Currency', related="company_id.currency_id", store=True)
    approval_user_ids = fields.One2many('approval.user', 'approval_id', 'Approval Users')

    _sql_constraints = [
        ('name', 'unique (name)',
         "Name must be unique"),
    ]
