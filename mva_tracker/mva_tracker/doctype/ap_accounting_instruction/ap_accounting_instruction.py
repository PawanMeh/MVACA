
# -*- coding: utf-8 -*-
# Copyright (c) 2017, hello@openetech.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe import utils

class APAccountingInstruction(Document):
	def validate(self):
		ap_total_debit = 0
		ap_total_credit = 0
		for accounting_detail in self.accounting_detail:
			ap_total_debit = ap_total_debit + accounting_detail.debit
			ap_total_credit = ap_total_credit + accounting_detail.credit
			if accounting_detail.account:
				is_group = 0
				is_group = frappe.db.get_value("Account",{"name":accounting_detail.account},["is_group"])
				if is_group == 1:
					frappe.throw(_("Group Account cannot be selected"))
		diff = round(ap_total_debit,2) - round(ap_total_credit,2)
		if diff  == 0:
			self.ap_total_debit = ap_total_debit
			self.ap_total_credit = ap_total_credit
		else:
			frappe.throw(_("Total debits {0} should be equal to total credits {1} in accounting detail").format(ap_total_debit,ap_total_credit))

		if self.ap_total_debit == 0 or self.ap_total_credit == 0:
			frappe.throw(_("Debit or Credit cannot be zero"))

		if self.apr_reference:
			apai_check = frappe.db.sql("""select name from `tabAP Accounting Instruction` where apr_reference = %s""",self.apr_reference)
			if apai_check:
				name = apai_check[0][0]
				if self.name == name:
					pass
				else:
					frappe.throw(_("AP Accounting Instruction is already created. Ref : {0}").format(name))

		if self.transaction_type:
			db_tran_type = frappe.db.sql("""select transaction_type 
									from `tabAP Accounting Instruction`
									where name = %s""",self.name)
			if self.ap_required_documents and db_tran_type[0][0] == self.transaction_type:
				pass
			else:
				table = "ap_required_documents"
				req_doc_detail = list(frappe.db.sql("""select document_type, document_required
									from `tabRequired Documents Detail`
									where parent = %s""",self.transaction_type,as_dict=1))
				self.set(table, [])
				for d in req_doc_detail:
					self.append(table, d)

	def on_submit(self):
		for ap_req_docs in self.ap_required_documents:
			if ap_req_docs and (ap_req_docs.document_required == "No" or not ap_req_docs.document_required):
				frappe.throw(_("List of verified documents should be set to 'Yes' or 'NA' before submitting"))

		frappe.db.sql("""update `tabAP Accounting Instruction` set apr_status = "Instructed", api_date = %s where name = %s and name not in (select apr_reference from `tabAP Voucher Detail`)""",(frappe.utils.nowdate(),self.name))
		doc_apr = frappe.get_doc("AP Record Request",self.apr_reference)
		doc_apr.apr_status = "Instructed"
		doc_apr.save()
