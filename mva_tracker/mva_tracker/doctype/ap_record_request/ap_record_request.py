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
			supp_invoice_check = frappe.db.sql("""select name from `tabAP Record Request` where supplier = %s and supplier_invoice_no = %s and docstatus <> 2""",(self.supplier, self.supplier_invoice_no))
			if supp_invoice_check:
				name = supp_invoice_check[0][0]
				if self.name == name:
					pass
				else:
					frappe.throw(_("Duplicate Vendor Inovice No already exists on : {0}").format(name))

		if self.transaction_type:
			db_tran_type = frappe.db.sql("""select transaction_type
							from `tabAP Record Request`
							where name = %s""",self.name)
			if self.get("__islocal") == 1:
				table = "ap_required_documents"
                                req_doc_detail = list(frappe.db.sql("""select document_type, document_required
                                                                        from `tabRequired Documents Detail`
                                                                        where parent = %s""",self.transaction_type,as_dict=1))
                                self.set(table, [])
                                for d in req_doc_detail:
                                        self.append(table, d)
			else:	
				if self.ap_required_documents and db_tran_type[0][0] == self.transaction_type:
					pass
				else:
					table = "ap_required_documents"
					req_doc_detail = list(frappe.db.sql("""select document_type, document_required
									from `tabRequired Documents Detail`
									where parent = %s""",self.transaction_type,as_dict=1))
					self.set(table, [])
					for d in req_doc_detail:
						self.append(table, d)

		self.amt_net_of_tax = self.amount - self.tax_amt

		name_check = frappe.db.sql("""select name from `tabAP Record Request` where name = %s""",(self.name))
		if name_check:
			pass
		else:
			self.apr_status = "Initiated"

	def on_submit(self):
		#Check for not exists condition
		#frappe.db.sql("""update `tabAP Record Request` set apr_date = %s, apr_status = "Requested" where name = %s and name not in (select apr_reference from `tabAP Accounting Instruction`)""",(frappe.utils.nowdate(),self.name))
		for ap_req_docs in self.ap_required_documents:
                	if ap_req_docs and (ap_req_docs.document_required == "No" or not ap_req_docs.document_required):
				frappe.throw(_("List of verified documents should be set to 'Yes' or 'NA' before submitting"))
		doc = frappe.get_doc("AP Record Request",self.name)
		doc.apr_date = frappe.utils.nowdate()
		doc.apr_status = "Requested"
		doc.save()
