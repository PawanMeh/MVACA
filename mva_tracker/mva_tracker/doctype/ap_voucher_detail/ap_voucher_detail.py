# -*- coding: utf-8 -*-
# Copyright (c) 2017, hello@openetech.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import utils
from frappe import _

class APVoucherDetail(Document):
	def validate(self):
		apr_doc = frappe.get_doc('AP Record Request', self.apr_reference)
		if apr_doc.apr_status == "AP Recorded":
			frappe.throw(_("Corresponding AP Voucher Detail is already created for the APR"))
		
	def on_submit(self):
		self.apvd_date = frappe.utils.nowdate()
		ap_record_ref = frappe.get_doc("AP Record Request",self.apr_reference)
		ap_record_ref.apr_status = "AP Recorded"
		ap_record_ref.save()