# -*- coding: utf-8 -*-
# Copyright (c) 2017, hello@openetech.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import utils
from frappe import _

class CDVoucherDetails(Document):
	def validate(self):
		if self.cdr_reference:
			cdvd_check = frappe.db.sql("""select name from `tabCD Voucher Details` where cdr_reference = %s""",self.cdr_reference)
			if cdvd_check:
				name = cdvd_check[0][0]
				if self.name == name:
					pass
				else:
					frappe.throw(_("CD Voucher Detail is already created. Ref : {0}").format(name))
		
	def on_submit(self):
		frappe.db.sql("""update `tabCD Voucher Details` set cdr_status = "Posted", cdvd_date = %s where name = %s""",(frappe.utils.nowdate(),self.name))
		frappe.db.sql("""update `tabCD Accounting Instruction` set cdr_status = "Posted" where name = %s""",self.name)
		doc_cdr = frappe.get_doc("CD Record Request",self.cdr_reference)
		doc_cdr.cdr_date = frappe.utils.nowdate()
		doc_cdr.cdr_status = "Posted"
		doc_cdr.save()
