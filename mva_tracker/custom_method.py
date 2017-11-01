from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt, cstr
from frappe.model.mapper import get_mapped_doc
from frappe.model.document import Document

@frappe.whitelist()
def make_ap_accounting_instruction(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.apr_reference = source_name

	doclist = get_mapped_doc("AP Record Request", source_name, 	{
		"AP Record Request": {
			"doctype": "AP Accounting Instruction",
			"validation": {
				"docstatus": ["=", 1]
			}
		}
	}, target_doc, set_missing_values)

	return doclist

@frappe.whitelist()
def make_ap_voucher_detail(source_name, target_doc=None):
	doclist = get_mapped_doc("AP Accounting Instruction", source_name, 	{
		"AP Accounting Instruction": {
			"doctype": "AP Voucher Detail",
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"AP Accounting Instruction Detail": {
			"doctype": "AP Voucher Detail Accounting"
		}
	}, target_doc)

	return doclist
	
@frappe.whitelist()
def make_wct_detail(source_name, target_doc=None):
	doclist = get_mapped_doc("AP Voucher Detail", source_name, 	{
		"AP Voucher Detail": {
			"doctype": "Wire Check Transfer Details",
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"AP Voucher Detail Accounting": {
			"doctype": "Wire Check Transfer Voucher Detail"
		}
	}, target_doc)

	return doclist

@frappe.whitelist()
def make_cash_dist_instruction(source_name, target_doc=None):
	doclist = get_mapped_doc("Wire Check Transfer Details", source_name, 	{
		"Wire Check Transfer Details": {
			"doctype": "Cash Disbursement Accounting Instruction",
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"Wire Check Transfer Voucher Detail": {
			"doctype": "Cash Distribution Accounting Instruction Detail"
		}
	}, target_doc)

	return doclist

@frappe.whitelist()
def make_cdvd_detail(source_name, target_doc=None):
	doclist = get_mapped_doc("Cash Disbursement Accounting Instruction", source_name, 	{
		"Cash Disbursement Accounting Instruction": {
			"doctype": "Cash Disbursement Voucher Details",
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"Cash Distribution Accounting Instruction Detail": {
			"doctype": "Cash Distribution AP Details"
		},
		"Cash Distribution Accounting": {
			"doctype": "Cash Distribution CD Details"
		},
	}, target_doc)

	return doclist