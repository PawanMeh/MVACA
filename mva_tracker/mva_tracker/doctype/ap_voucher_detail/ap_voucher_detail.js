// Copyright (c) 2017, hello@openetech.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('AP Voucher Detail', {
		refresh:function(frm) {
			if(frm.doc.docstatus == 1) {
				frm.add_custom_button(__('Wire/Check Transfer Detail'), function() {
					frm.events.wct_detail(frm)
				}, __("Make"));
			}
		},
		wct_detail: function(frm){
			frappe.model.open_mapped_doc({
				method: "mva_tracker.custom_method.make_wct_detail",
				frm: frm
			})
		}
});
