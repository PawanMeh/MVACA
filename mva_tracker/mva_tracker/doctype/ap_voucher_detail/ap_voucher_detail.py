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
		if self.apr_reference:
			apvd_check = frappe.db.sql("""select name from `tabAP Voucher Detail` where apr_reference = %s""",self.apr_reference)
			if apvd_check:
				name = apvd_check[0][0]
				if self.name == name:
					pass
				else:
					frappe.throw(_("AP Voucher Detail is already created. Ref : {0}").format(name))
		
	def on_submit(self):
		frappe.db.sql("""update `tabAP Voucher Detail` set apr_status = "Posted", apvd_date = %s where name = %s""",(frappe.utils.nowdate(),self.name))
		apai = frappe.db.sql("""select name from `tabAP Accounting Instruction` where apr_reference = %s""",self.apr_reference)
		if apai:
			apai_name = apai[0][0]
			doc_apai = frappe.get_doc("AP Accounting Instruction",apai_name)
			doc_apai.apr_status = "Posted"
			doc_apai.save()
			
		doc_apr = frappe.get_doc("AP Record Request",self.apr_reference)
		doc_apr.apr_status = "Posted"
		doc_apr.save()