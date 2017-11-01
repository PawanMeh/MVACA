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
			
		apr_doc = frappe.get_doc('AP Record Request', self.apr_reference)
		if apr_doc.apr_status == "AP Instructed":
			frappe.throw(_("Corresponding AP Accounting instruction is already created for the APR"))

		if self.ap_total_debit != self.ap_total_credit:
			frappe.throw(_("Total debits should be equal to total credits in accounting detail"))

	def on_submit(self):
		self.apai_date = frappe.utils.nowdate()
		ap_record_ref = frappe.get_doc("AP Record Request",self.apr_reference)
		ap_record_ref.apr_status = "AP Instructed"
		ap_record_ref.save()
