// Copyright (c) 2017, hello@openetech.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('AP Record Request', {
	supplier: function(frm) {
		if (frm.doc.supplier && frm.doc.docstatus !== 1)
		{
			frappe.call({
				method:'frappe.client.get_value',
				args: {
							'doctype': 'Supplier',
							'filters': {'name': frm.doc.supplier},
							'fieldname': ['default_currency']
						},
							async:false,
							callback: function(r) {
								if (!r.exc) {
								frm.doc.currency = r.message.default_currency;
								frm.doc.advance_currency = r.message.default_currency;
							}
						}
			})
			frm.refresh_field("currency");
			frm.refresh_field("advance_currency");
		}
	},
	refresh:function(frm) {
		if(frm.doc.docstatus === 1) {
			frm.add_custom_button(__('AP Accounting Instruction'), function() {
				frm.events.ap_accounting_instruction(frm)
			}, __("Make"));
		}
	},
	ap_accounting_instruction: function(frm){
		frappe.model.open_mapped_doc({
			method: "mva_tracker.custom_method.make_ap_accounting_instruction",
			frm: frm
		})
	}
});