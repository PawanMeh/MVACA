# -*- coding: utf-8 -*-
# Copyright (c) 2017, hello@openetech.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe import utils

class CDAccountingInstruction(Document):
	def validate(self):
		self.ap_total_debit = 0
		self.ap_total_credit = 0
		for accounting_detail in self.cd_accounting_detail:
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

		if self.cdr_reference:
			apai_check = frappe.db.sql("""select name from `tabCD Accounting Instruction` where cdr_reference = %s""",self.cdr_reference)
			if apai_check:
				name = apai_check[0][0]
				if self.name == name:
					pass
				else:
					frappe.throw(_("AP Accounting Instruction is already created. Ref : {0}").format(name))


	def on_submit(self):
		frappe.db.sql("""update `tabCD Accounting Instruction` set cdr_status = "Instructed", cdai_date = %s where name = %s and name not in (select cdr_reference from `tabCD Voucher Details`)""",(frappe.utils.nowdate(),self.name))
		doc_cdr = frappe.get_doc("CD Record Request",self.cdr_reference)
		doc_cdr.cdr_date = frappe.utils.nowdate()
		doc_cdr.cdr_status = "Instructed"
		doc_cdr.save()
		#frappe.db.sql("""update `tabAP Record Request` set apr_status = "Instructed" where name = %s""",self.apr_reference)