# -*- coding: utf-8 -*-
# Copyright (c) 2017, hello@openetech.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import utils,_,msgprint

class APRecordRequest(Document):
	def validate(self):
		if self.supplier_invoice_no:
			supp_invoice_check = frappe.db.sql("""select name from `tabAP Record Request` where supplier = %s and supplier_invoice_no = %s""",(self.supplier, self.supplier_invoice_no))
			if supp_invoice_check:
				name = supp_invoice_check[0][0]
				if self.name == name:
					pass
				else:
					frappe.throw(_("Duplicate Vendor Inovice No already exists on : {0}").format(name))
		name_check = frappe.db.sql("""select name from `tabAP Record Request` where name = %s""",(self.name))
		if name_check:
			pass
		else:
			self.apr_status = "Initiated"

	def on_submit(self):
		#Check for not exists condition
		#frappe.db.sql("""update `tabAP Record Request` set apr_date = %s, apr_status = "Requested" where name = %s and name not in (select apr_reference from `tabAP Accounting Instruction`)""",(frappe.utils.nowdate(),self.name))
		doc = frappe.get_doc("AP Record Request",self.name)
		doc.apr_date = frappe.utils.nowdate()
		doc.apr_status = "Requested"
		doc.save()