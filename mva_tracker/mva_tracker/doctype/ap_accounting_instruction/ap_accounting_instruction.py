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
		self.ap_total_debit = 0
		self.ap_total_credit = 0
		for accounting_detail in self.accounting_detail:
			self.ap_total_debit = self.ap_total_debit + accounting_detail.debit
			self.ap_total_credit = self.ap_total_credit + accounting_detail.credit
			if accounting_detail.account:
				is_group = 0
				is_group = frappe.db.get_value("Account",{"name":accounting_detail.account},["is_group"])
				if is_group == 1:
					frappe.throw(_("Group Account cannot be selected"))

		if self.ap_total_debit != self.ap_total_credit:
			frappe.throw(_("Total debits should be equal to total credits in accounting detail"))
		
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


	def on_submit(self):
		frappe.db.sql("""update `tabAP Accounting Instruction` set apr_status = "Instructed", api_date = %s where name = %s and name not in (select apr_reference from `tabAP Voucher Detail`)""",(frappe.utils.nowdate(),self.name))
		doc_apr = frappe.get_doc("AP Record Request",self.apr_reference)
		doc_apr.apr_date = frappe.utils.nowdate()
		doc_apr.apr_status = "Instructed"
		doc_apr.save()
		#frappe.db.sql("""update `tabAP Record Request` set apr_status = "Instructed" where name = %s""",self.apr_reference)