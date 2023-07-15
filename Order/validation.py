import re
from Product.models import Product


class GetProduct:

    @staticmethod
    def by_name(name):
        requested_product_object = Product.objects.filter(name=name, is_deleted=False)
        if requested_product_object.count() != 0:
            return {'status': True, 'object': requested_product_object[0]}
        return {'status': False, 'error_code': 'P-NF-101', 'error_msg': f'There is no Product Like {name}'}

    @staticmethod
    def by_uuid(uuid):
        requested_product_object = Product.objects.filter(uuid=uuid, is_deleted=False)
        if requested_product_object.count() != 0:
            return {'status': True, 'object': requested_product_object[0]}
        return {'status': False, 'error_code': 'P-NF-102', 'error_msg': f'There is no product which have uuid = {uuid}'}

    @staticmethod
    def by_product(product):
        if product.is_deleted:
            return {'status': False, 'error_code': 'P-NF-103', 'error_msg': f'Product Object Not Found'}
        return {'status': True, 'object': product}

    @staticmethod
    def by_id(pk):
        requested_product_object = Product.objects.filter(id=pk, is_deleted=False)
        if requested_product_object.count() != 0:
            return {'status': True, 'object': requested_product_object[0]}
        return {'status': False, 'error_code': 'P-NF-104', 'error_msg': f'There is no product which have id = {pk}'}


def is_requested_qty_of_product_available(requested_product_object, requested_qty):
    product_existence_status = GetProduct.by_product(requested_product_object)
    if product_existence_status['status']:
        available_product_qty = requested_product_object.qty
        if available_product_qty >= requested_qty:
            return {'status': True}
        elif available_product_qty == 0:
            return {'status': False, 'error_code': 'P102',
                    'error_msg': f'Inventory not Available for Product : {requested_product_object.name}.'}
        else:
            return {'status': False, 'error_code': 'P103',
                    'error_msg': f'Only {available_product_qty} QTY left form Product {requested_product_object.name}.'}
    else:
        return product_existence_status


def validate_customer(fname, lname, phone, email, address):
    fname = fname.strip()
    lname = lname.strip()
    phone = phone.strip()
    email = email.strip()

    phone_pattern = r"^\d{10}$"
    phone_match = re.match(phone_pattern, phone)

    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    email_match = re.match(email_pattern, email)

    if fname == "" or lname == "":
        return {'status': False, 'error_code': 'VAN_101', 'error_msg': 'First & Last name is Mandatory'}

    elif phone != "":
        if not phone_match:
            return {'status': False, 'error_code': 'VAN_102', 'error_msg': 'Please enter a valid phone number'}

    elif email != "":
        if not email_match:
            return {'status': False, 'error_code': 'VAN_103', 'error_msg': 'Please enter a valid Email number'}

    return {'status': True}