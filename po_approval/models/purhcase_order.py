# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import werkzeug.urls

READONLY_STATES = {
    'purchase': [('readonly', True)],
    'done': [('readonly', True)],
    'cancel': [('readonly', True)],
    'po awaiting': [('readonly', True)],
}


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account')
    state = fields.Selection(selection_add=[('po awaiting', 'Awaiting Approval'), ('to approve',)])
    approval_user_id = fields.Many2one('res.users', string='Approval User')
    approved_button_bool = fields.Boolean(string='approved bool', compute="_compute_approved_button_bool")
    approval_url = fields.Char(string='approved bool', compute="_compute_approval_url")
    partner_id = fields.Many2one('res.partner', string='Vendor', required=True, states=READONLY_STATES, change_default=True, tracking=True, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", help="You can find a vendor by its Name, TIN, Email or Internal Reference.")
    date_order = fields.Datetime('Order Deadline', required=True, states=READONLY_STATES, index=True, copy=False,
                                 default=fields.Datetime.now,
                                 help="Depicts the date within which the Quotation should be confirmed and converted into a purchase order.")
    currency_id = fields.Many2one('res.currency', 'Currency', required=True, states=READONLY_STATES,
                                  default=lambda self: self.env.company.currency_id.id)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, states=READONLY_STATES, default=lambda self: self.env.company.id)
    dest_address_id = fields.Many2one('res.partner', domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", string='Dropship Address', states=READONLY_STATES,
        help="Put an address if you want to deliver directly from the vendor to the customer. "
             "Otherwise, keep empty to deliver to your own company.")
    partner_ref = fields.Char('Vendor Reference', copy=False,
                              help="Reference of the sales order or bid sent by the vendor. "
                                   "It's used to do the matching when you receive the "
                                   "products as this reference is usually written on the "
                                   "delivery order sent by your vendor.", states=READONLY_STATES)
    user_id = fields.Many2one(
        'res.users', string='Purchase Representative', index=True, tracking=True,
        default=lambda self: self.env.user, check_company=True, states=READONLY_STATES)
    origin = fields.Char('Source Document', copy=False,
        help="Reference of the document that generated this purchase order "
             "request (e.g. a sales order)", states=READONLY_STATES)
    reminder_date_before_receipt = fields.Integer('Days Before Receipt', related='partner_id.reminder_date_before_receipt', readonly=False, states=READONLY_STATES)

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

    def recall_po(self):
        self.button_draft()
        return True
    #
    # def write(self, vals):
    #     res = super(PurchaseOrder, self).write(vals)
    #     if res and vals:
    #         for rec in self:
    #             state = vals.get('state',False) or rec.state
    #             if state == 'po awaiting':
    #                 raise ValidationError("user cannot be able to edit the PO in awaiting")
    #     return res

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

    def button_draft(self):
        result = super(PurchaseOrder, self).button_draft()
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
