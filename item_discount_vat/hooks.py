app_name = "item_discount_vat"
app_title = "Item Discount VAT"
app_publisher = "Jamunachi"
app_description = "Apply item-wise discounts with VAT recalculation in ERPNext"
app_email = "jamunachi007@gmail.com"
app_license = "MIT"
doc_events = {
    "Sales Invoice": {
        "before_submit": "item_discount_vat.sales_invoice.apply_item_discounts"
    }
}

