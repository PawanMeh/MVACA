# -*- coding: utf-8 -*-
# Copyright (c) 2017, hello@openetech.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe import utils

class WireCheckTransferDetails(Document):
	def validate(self):
		apr_doc = frappe.get_doc('AP Record Request', self.apr_reference)
		if apr_doc.apr_status == "Paid":
			frappe.throw(_("Corresponding Wire Check Transfer Detail is already created for the APR"))
		
		if self.wct_amount <= 0:
			frappe.throw(_("WCT Amount cannot be zero or negative")) 

	def on_submit(self):
		self.wctd_date = frappe.utils.nowdate()
		ap_record_ref = frappe.get_doc("AP Record Request",self.apr_reference)
		ap_record_ref.apr_status = "Paid"
		ap_record_ref.save()
