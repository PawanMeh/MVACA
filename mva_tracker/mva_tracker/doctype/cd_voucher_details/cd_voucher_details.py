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
		cdai = frappe.db.sql("""select name from `tabCD Accounting Instruction` where cdr_reference = %s""",self.cdr_reference)
		if cdai:
			cdai_name = cdai[0][0]
			doc_cdai = frappe.get_doc("CD Accounting Instruction",cdai_name)
			doc_cdai.cdr_status = "Posted"
			doc_cdai.save()
		doc_cdr = frappe.get_doc("CD Record Request",self.cdr_reference)
		doc_cdr.cdr_status = "Posted"
		doc_cdr.cp_voucher = self.cp_voucher
		doc_cdr.save()

