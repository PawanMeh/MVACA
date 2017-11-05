// Copyright (c) 2017, hello@openetech.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('CD Accounting Instruction', {
	refresh:function(frm) {
		if(frm.doc.docstatus === 1) {
			frm.add_custom_button(__('CD Voucher Detail'), function() {
				frm.events.ap_accounting_instruction(frm)
			}, __("Make"));
		}
	},
	ap_accounting_instruction: function(frm){
		frappe.model.open_mapped_doc({
			method: "mva_tracker.custom_method.make_cdvd_detail",
			frm: frm
		})
	}
});
