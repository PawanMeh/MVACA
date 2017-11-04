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
		self.apvd_date = frappe.utils.nowdate()
		frappe.db.sql("""update `tabAP Voucher Detail` set apr_status = "Posted" where name = %s""",self.name)
		frappe.db.sql("""update `tabAP Record Request` set apr_status = "Posted" where name = %s""",self.apr_reference)