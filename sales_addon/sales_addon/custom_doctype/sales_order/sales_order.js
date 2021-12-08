// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.ui.form.on('Sales Order', {
	validate:function(frm){
        
	},
	refresh(frm) {
		frm.add_custom_button("Pending Invoice", function(){
		    frappe.call({
                method: 'frappe.client.get_list',
                args: {
                    'doctype': 'Sales Invoice',
                    'filters':[['customer','=',frm.doc.customer],['docstatus','=',1],['outstanding_amount','>',0]],
                    'fields': [
                        'name',
                        'grand_total',
                        'outstanding_amount',
                        'posting_date',
                        'due_date'
                    ]
                },
                callback: function(r) {
                    if (!r.exc) {
                        console.log(r.message)
                        var invoice_table = "<table class ='table' width = '100%'>"+
                                           "<tr>"+
                                           "<th width= '16.66%'>Sr No</th>"+
                                           "<th width= '16.66%'>Sales Invoice ID</th>"+
                                           "<th width= '16.66%'>Sales Invoice Date</th>"+
                                           "<th width='16.66%'>Due Date</th>"+
                                           "<th width= '16.66%'>Oustanding Amount</th>"+
                                           "<th width= '16.66%'>Due Days</th>"+
                                           "</tr>";
                          var i=1;               
                        r.message.forEach(function(element){
                            // console.log(element)
                            var date1 = new Date(element.posting_date);
                            var date2 = new Date();
                            var diffDays = date2.getDate() - date1.getDate(); 
                            // console.log(diffDays)
                                invoice_table+="<tr>"+
                                "<td>"+i+"</td>"+
                               "<td>"+element.name+"</td>"+
                               "<td>"+element.posting_date+"</td>"+
                               "<td>"+element.due_date+"</td>"+
                               "<td>"+element.outstanding_amount+"</td>"+
                               "<td>" + diffDays + "</td>"+
                               "</tr>";
                            i++;
                        })
                        invoice_table+= "</table>";
                        // frappe.msgprint(invoice_table)
                    }
                }
            });
});
	}
})
frappe.ui.form.on("Sales Order", {
    "customer": function(frm) {
        if(frm.doc.customer){
            frappe.call({
                "method":"erpnext.accounts.utils.get_balance_on",
                "args":{
                    date: frappe.datetime.nowdate(),
                    party_type: 'Customer',
                    party: frm.doc.customer
                },
                callback:function(res){
                    console.log(res.message)
					if(res.message){
						frm.doc.outstanding_amount = res.message;
						frm.refresh_field("outstanding_amount");
					}
                }
    
            })
        }
    }
});

frappe.ui.form.on("Sales Order Item", {
    item_code(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
        // frappe.msgprint(row.delivery_date)
		if(row.item_code){
			frappe.call({
				"method":"sales_addon.sales_addon.custom_doctype.sales_order.sales_order.get_item_sold_today",
				"args":{
					"item_code":row.item_code,
                    "company": frm.doc.company
				},
				callback:function(res){
					console.log(res.message[0][0])
					if(res.message){
						row.sold_quantity_today = res.message[0][0];
						frm.refresh_field("items");
					}
				}
	
			})
		}
    },
    // uom(frm, cdt, cdn) {
    //     let row = frappe.get_doc(cdt, cdn);
    //     console.log(row.item_code)
    //     console.log(frm.doc.company)
    //     console.log(row.uom)
    //     frappe.call({
    //         "method":"sales_addon.sales_addon.custom_doctype.sales_order.sales_order.get_uom_for_check",
    //         "args":{
    //             "item_code":row.item_code,
    //             "company": frm.doc.company,
    //             "uom": row.uom
    //         },
    //         callback:function(res){
    //             if(res.message == false){
    //                 frappe.msgprint('Item "' + row.item_code + '" quota is not set for "' + frm.doc.company + '"')
    //                 row.conversion_factor = 1;
    //                 row.stock_qty = 1;
    //                 frm.refresh_field("items");
    //             }
    //         }

    //     })
    // },
});

