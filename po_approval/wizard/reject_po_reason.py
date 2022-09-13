# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class RejectReasonPo(models.TransientModel):
    _name = 'reason.po'
    _description="Reject Reason Po"

    reason = fields.Char('Reason')

    def confirm(self):
        active_id = self.env.context.get('active_id')
        purchase_id = self.env['purchase.order'].search([('id', '=', active_id)])
        if purchase_id:
            purchase_id.approval_user_id = False
            purchase_id.button_draft()
            template = self.env.ref('po_approval.mail_template_purchase_reject', raise_if_not_found=False)
            ctx = self._context.copy()
            ctx.update({
                'reason': self.reason,
            })
            template.with_context(ctx).send_mail(purchase_id.id,)
