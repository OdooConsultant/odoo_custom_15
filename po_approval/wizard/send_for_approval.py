# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class SendForApproval(models.TransientModel):
    _name = 'approval.send'
    _description = "Send For Approval"

    user_id = fields.Many2one('res.users', 'Users')
    
    @api.onchange('user_id')
    def _onchange_user_id(self):
        active_id = self.env.context.get('active_id')
        purchase_id = self.env['purchase.order'].search([('id', '=', active_id)])
        if purchase_id:
            if not purchase_id.analytic_account_id and purchase_id.partner_id.approval_id:
                users = purchase_id.partner_id.approval_id.approval_user_ids.mapped('user_ids')
                domain = [("id", "in", users.ids)] if users else [("id", "=", False)]
            elif purchase_id.analytic_account_id and purchase_id.analytic_account_id.approval_id:
                users = purchase_id.analytic_account_id.approval_id.approval_user_ids.mapped('user_ids')
                domain = [("id", "in", users.ids)] if users else [("id", "=", False)]
            elif purchase_id.company_id.approval_id:
                users = purchase_id.company_id.approval_id.approval_user_ids.mapped('user_ids')
                domain = [("id", "in", users.ids)] if users else [("id", "=", False)]
            else:
                domain = [("id", "=", False)]
        else:
            domain = [("id", "=", False)]
        return{'domain':{'user_id':domain}}

    def confirm(self):
        active_id = self.env.context.get('active_id')
        purchase_id = self.env['purchase.order'].search([('id', '=', active_id)])
        if purchase_id:
            template = self.env.ref('po_approval.mail_template_purchase_approval', raise_if_not_found=False)
            purchase_id.state = 'po awaiting'
            purchase_id.approval_user_id = self.user_id.id
            template.send_mail(purchase_id.id,)

