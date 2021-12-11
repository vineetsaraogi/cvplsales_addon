# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
import json
import frappe.utils
from frappe.utils import cstr, flt, getdate, cint, nowdate, add_days, get_link_to_form, strip_html
from frappe import _
from six import string_types
from frappe.model.utils import get_fetch_values
from frappe.model.mapper import get_mapped_doc
from erpnext.stock.stock_balance import update_bin_qty, get_reserved_qty
from frappe.desk.notifications import clear_doctype_notifications
from frappe.contacts.doctype.address.address import get_company_address
from erpnext.controllers.selling_controller import SellingController
from erpnext.selling.doctype.customer.customer import check_credit_limit
from erpnext.stock.doctype.item.item import get_item_defaults
from erpnext.setup.doctype.item_group.item_group import get_item_group_defaults
from erpnext.manufacturing.doctype.production_plan.production_plan import get_items_for_material_requests
from erpnext.accounts.doctype.sales_invoice.sales_invoice import validate_inter_company_party, update_linked_doc,\
	unlink_inter_company_doc

def validate(self,method):
	item_code = []
	for item in self.items:
		item_code.append(item.item_code)

	customer = self.customer
	customer_group = frappe.db.get_value("Customer", customer, "customer_group")
	values = {'item_code': item_code, 'customer_group': customer_group, 'company': self.company}

	diff = frappe.db.sql("""
		select
		    `tabItem`.name as item_code,
		    ifnull((`tabItem Master`.quota_in_stock_uom - (select SUM(`tabSales Order Item`.stock_qty) from `tabSales Order Item` where CAST(`tabSales Order Item`.creation AS DATE) = CAST(CURRENT_TIMESTAMP AS DATE) and `tabSales Order Item`.item_code = `tabItem`.name and `tabSales Order Item`.docstatus = 1 AND `tabSales Order Item`.parent in (Select `tabSales Order`.name from `tabSales Order` where `tabSales Order`.company = %(company)s and `tabSales Order`.customer in (select `tabCustomer`.name from `tabCustomer` where `tabCustomer`.customer_group = %(customer_group)s)))), `tabItem Master`.quota_in_stock_uom) as diff,
			ifnull((`tabItem Master`.quota - (select SUM(`tabSales Order Item`.qty) from `tabSales Order Item` where CAST(`tabSales Order Item`.creation AS DATE) = CAST(CURRENT_TIMESTAMP AS DATE) and `tabSales Order Item`.item_code = `tabItem`.name and `tabSales Order Item`.docstatus = 1 AND `tabSales Order Item`.parent in (Select `tabSales Order`.name from `tabSales Order` where `tabSales Order`.company = %(company)s and `tabSales Order`.customer in (select `tabCustomer`.name from `tabCustomer` where `tabCustomer`.customer_group = %(customer_group)s)))), `tabItem Master`.quota) as diff_qty,
			`tabItem`.stock_uom as uom,`tabItem Master`.quota_in_stock_uom,`tabItem Master`.quota,`tabItem Master`.uom as second_uom
		from
		    `tabItem`
			left join `tabItem Master` on `tabItem`.name = `tabItem Master`.parent			
	    where
	        `tabItem`.name in  %(item_code)s
			and `tabItem Master`.company = %(company)s
	        group by `tabItem`.name
		""", values=values, as_dict=True)

	if diff != []:
		for item in self.items:
			for i in diff:
				if i.item_code == item.item_code:
					diff_in_qty = i.diff - item.stock_qty
					diff_in_quota = i.diff_qty - item.qty
					if diff_in_qty < 0:
						string = "Daily Quota for Item <b>{item}</b> is <b>{quota_in_stock_uom}({default_stock_uom})/{quota_in_second_uom}({second_uom})</b> for customer group <b>{customer_group}</b>.Out of which <b>{remaining_quota_in_stock_uom}({default_stock_uom})/{left_in_second_uom}({second_uom})</b> is left. Inserted Quantity is <b>{ordered_qty}({ordered_uom})</b>".format(item=str(item.item_code),quota_in_stock_uom=i.quota_in_stock_uom,default_stock_uom=i.uom,quota_in_second_uom=i.quota,second_uom=i.second_uom,customer_group=customer_group,remaining_quota_in_stock_uom=i.diff,ordered_qty=item.qty,ordered_uom=item.uom,left_in_second_uom=i.diff_qty)
						frappe.throw(string)
						# frappe.throw('Daily Quota for Item <b>"'+ str(item.item_code) + '"</b> is <b>' + str(i.diff) + '(' + i.uom + ')</b>/<b>"' + str(i.diff_qty) + '(' + item.uom + ')"</b> for customer group <b>"'+ customer_group +'"</b><br>" and the inserted Quantity is <b>' + str(item.qty) + '</b>')
		
	# quota check for company
	# for item in self.items:
	# 	data = frappe.db.count('Item Master', {'company': self.company, 'parent': item.item_code, 'uom': item.uom})
	# 	if data == 0:
	# 		frappe.throw('UOM of item "' + item.item_code + '" for "' + item.uom + '" is not set for the company "' + self.company + '". Kindly insert the UOM in Item first')
	

@frappe.whitelist()
def get_item_sold_today(item_code, company):
	values = {'item_code': item_code, "company": company}
	total_quantity = frappe.db.sql("""
		select
		    SUM(`tabSales Order Item`.qty)
		from
		    `tabSales Order Item`
			LEFT JOIN `tabSales Order` on `tabSales Order`.name = `tabSales Order Item`.parent
	    where
	        CAST(`tabSales Order Item`.creation AS DATE) = CAST(CURRENT_TIMESTAMP AS DATE)
	        AND
	        `tabSales Order Item`.item_code = %(item_code)s
			and
	        `tabSales Order Item`.docstatus = 1
			and
			`tabSales Order`.company = %(company)s
		""", values=values, as_dict=False)
	
	return total_quantity


@frappe.whitelist()
def get_uom_for_check(item_code, company, uom):
	values = {'item_code': item_code, 'company': company, 'uom': uom}
	data = frappe.db.sql("""
    	select company, uom, quota from `tabItem Master` where parent = %(item_code)s and company = %(company)s and quota_in_stock_uom = %(uom)s
	""", values=values, as_dict = 1)

	if data == []:
		return False
	else:
		return True