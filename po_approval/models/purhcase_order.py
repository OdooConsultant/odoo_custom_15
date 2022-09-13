# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import werkzeug.urls


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account')
    state = fields.Selection(selection_add=[('po awaiting', 'Po Awaiting'), ('to approve',)])
    approval_user_id = fields.Many2one('res.users', string='Approval User')
    approved_button_bool = fields.Boolean(string='approved bool', compute="_compute_approved_button_bool")
    approval_url = fields.Char(string='approved bool', compute="_compute_approval_url")

    def _compute_approval_url(self):
        result = self.sudo()._get_approval_url_for_action()
        for app in self:
            app.approval_url = result.get(app.id, False)

    def _get_approval_url_for_action(self, action=None, view_type=None, menu_id=None, res_id=None, model=None):
        res = dict.fromkeys(self.ids, False)
        for app in self:
            base_url = self.env.user.get_base_url()
            menu_id = self.env.ref('purchase.menu_purchase_root', False).id
            action_id = self.env.ref('purchase.purchase_rfq', False).id
            approval_url = "web#id=%s&cids=1&menu_id=%s&action=%s&model=purchase.order&view_type=form" % (self.id, menu_id, action_id,)
            approval_url = werkzeug.urls.url_join(base_url, approval_url)
            res[app.id] = approval_url
        return res

    def _compute_approved_button_bool(self):
        for rec in self:
            if rec.approval_user_id and self.env.user.id == rec.approval_user_id.id and self.state == 'po awaiting':
                rec.approved_button_bool = True
            else:
                rec.approved_button_bool = False

    def approve_po(self):
        template = self.env.ref('po_approval.mail_template_purchase_approved', raise_if_not_found=False)
        self.button_confirm()
        template.send_mail(self.id)

    def button_cancel(self):
        result = super(PurchaseOrder, self).button_cancel()
        self.approval_user_id = False
        return result

    def button_confirm(self):
        for order in self:
            # add state po awaiting
            if order.state not in ['draft', 'sent', 'po awaiting']:
                continue
            order._add_supplier_to_product()
            # Deal with double validation process
            if order._approval_allowed():
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
            if order.partner_id not in order.message_partner_ids:
                order.message_subscribe([order.partner_id.id])
        return True
