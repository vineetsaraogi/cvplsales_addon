// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.ui.form.on('Item Master', {
    quota(frm, cdt, cdn) {
		let row = frappe.get_doc(cdt, cdn);
		var uom = 0;
		var conversion_factor = 0;
		var total = 0
        for(var i in frm.doc.uoms){
            console.log(frm.doc.uoms[i].uom + " - " + frm.doc.uoms[i].conversion_factor)
			if(row.uom == frm.doc.uoms[i].uom){
				total = quota_uom(row.quota, frm.doc.uoms[i].conversion_factor)
				break;
			}
        }
		row.quota_in_stock_uom = total;
		refresh_field("table_of_item")
    },
	uom(frm, cdt, cdn) {
		let row = frappe.get_doc(cdt, cdn);
		var uom = 0;
		var conversion_factor = 0;
		var total = 0
        for(var i in frm.doc.uoms){
            console.log(frm.doc.uoms[i].uom + " - " + frm.doc.uoms[i].conversion_factor)
			if(row.uom == frm.doc.uoms[i].uom){
				total = quota_uom(row.quota, frm.doc.uoms[i].conversion_factor)
				break;
			}
        }
		row.quota_in_stock_uom = total;
		refresh_field("table_of_item")
    }
})

function quota_uom(quota, conversion_factor){
	var total = quota * conversion_factor;
	return total
}