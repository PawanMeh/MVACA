# -*- coding: utf-8 -*-
# Copyright (c) 2017, hello@openetech.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe import utils

class CashDisbursementAccountingInstruction(Document):
	def validate(self):
		self.cd_total_debit = 0
		self.cd_total_credit = 0
		
		apr_doc = frappe.get_doc('AP Record Request', self.apr_reference)
		if apr_doc.apr_status == "CD Instructed":
			frappe.throw(_("Corresponding CD Accounting Instruction is already created for the APR"))
		
		for accounting_detail in self.cash_distribution:
			self.cd_total_debit = self.cd_total_debit + accounting_detail.debit
			self.cd_total_credit = self.cd_total_credit + accounting_detail.credit

		if self.cd_total_debit != self.cd_total_credit:
			frappe.throw(_("Total debits should be equal to total credits in accounting detail"))

	def on_submit(self):
		self.cdai_date = frappe.utils.nowdate()
		ap_record_ref = frappe.get_doc("AP Record Request",self.apr_reference)
		ap_record_ref.apr_status = "CD Instructed"
		ap_record_ref.save()