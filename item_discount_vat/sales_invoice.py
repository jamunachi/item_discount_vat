
import frappe
from frappe.utils import nowdate

def apply_item_discounts(doc, method):
    discount_total = 0
    today = nowdate()

    for item in doc.items:
        discount = 0

        # Look for a matching rule
        rule = frappe.get_all("Item Discount Rule", filters={
            "customer": ["in", ["", doc.customer]],
            "item_code": ["in", ["", item.item_code]],
            "from_date": ["<=", today],
            "to_date": [">=", today]
        }, fields=["discount_percent", "discount_amount"], limit=1)

        if rule:
            rule = rule[0]
            if rule.discount_percent:
                discount = (item.qty * item.rate) * (rule.discount_percent / 100)
                item.custom_item_discount_percent = rule.discount_percent
            elif rule.discount_amount:
                discount = rule.discount_amount
                item.custom_item_discount_amount = rule.discount_amount
        else:
            # Fallback to manual entry
            if item.custom_item_discount_percent:
                discount = (item.qty * item.rate) * (item.custom_item_discount_percent / 100)
            elif item.custom_item_discount_amount:
                discount = item.custom_item_discount_amount

        # Apply discount to net amounts
        discounted_total = (item.qty * item.rate) - discount
        item.net_amount = discounted_total
        item.base_net_amount = discounted_total
        discount_total += discount

    # Optional GL posting
    if discount_total and frappe.db.get_single_value("Item Discount VAT Settings", "discount_account"):
        account = frappe.db.get_single_value("Item Discount VAT Settings", "discount_account")
        doc.append("accounts", {
            "account": account,
            "credit_in_account_currency": discount_total,
            "credit": discount_total,
            "is_advance": "No"
        })
