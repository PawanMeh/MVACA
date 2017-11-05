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
			"label": _("Disbursement Process"),
			"icon": "icon-star",
			"items": [
				{	"type": "doctype",
					"name": "CD Record Request",
					"label": "CD Record Request",
				},
				{	"type": "doctype",
					"name": "CD Accounting Instruction",
					"label": "CD Accounting Instruction",
				},
				{	"type": "doctype",
					"name": "CD Voucher Details",
					"label": "CD Voucher Details",
				}
			]
		}
]