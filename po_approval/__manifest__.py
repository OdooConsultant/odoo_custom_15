# -*- coding: utf-8 -*-
{
    'name': "PO Approval",

    'summary': """
        PO Approval""",

    'description': """
        PO Approval
    """,
    'depends': ['web', 'base', 'purchase', 'analytic', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'data/mail_template_data.xml',
        'wizard/send_for_approval_wizard.xml',
        'wizard/reject_po_reason_wizard.xml',
        'views/po_approval_view.xml',
        'views/res_partner_view.xml',
        'views/purchase_view.xml',
        'views/analytic_account_view.xml',
        'views/res_company_view.xml',
    ],
}