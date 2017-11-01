# -*- coding: utf-8 -*-
# Copyright (c) 2017, hello@openetech.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import utils

class APRecordRequest(Document):
	def on_submit(self):
		self.apr_date = frappe.utils.nowdate()
		self.apr_status = "Initiated"