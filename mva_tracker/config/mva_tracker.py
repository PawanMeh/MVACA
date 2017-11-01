from frappe import _

def get_data():
	return [
		{	"module_name": "mva_tracker",
			"label": _("AP Process"),
			"icon": "icon-star",
			"items": [
				{	"type": "doctype",
					"name": "AP Record Request",
					"label": "AP Record Request"
				},
				{	"type": "doctype",
					"name": "AP Accounting Instruction",
					"label": "AP Accounting Instruction"
				},
				{	"type": "doctype",
					"name": "AP Voucher Detail",
					"label": "AP Voucher Detail"
				}
			]
		},
		{	"module_name": "mva_tracker",
			"label": _("Payment Process"),
			"icon": "icon-star",
			"items": [
				{	"type": "doctype",
					"name": "Wire Check Transfer Details",
					"label": "Wire Check Transfer Details",
				},
				{	"type": "doctype",
					"name": "Cash Disbursement Accounting Instruction",
					"label": "Cash Disbursement Accounting Instruction",
				},
				{	"type": "doctype",
					"name": "Cash Disbursement Voucher Details",
					"label": "Cash Disbursement Voucher Details",
				}
			]
		}
]