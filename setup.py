from setuptools import setup, find_packages

setup(
    name='item_discount_vat',
    version='0.0.1',
    description='Apply item-wise discounts with VAT recalculation in ERPNext',
    author='jamunachi',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['frappe'],
)
