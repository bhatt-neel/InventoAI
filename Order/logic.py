from .validation import *
from Customer.models import *

class InvoiceSession:

    @staticmethod
    def get_product_qty_by_uuid(request, product_uuid):

        invoice = request.session.get('invoice')

        if invoice:
            existing_qty = invoice.get(product_uuid)

            if existing_qty:
                qty = invoice[product_uuid]
                return qty

        return 0

    @staticmethod
    def GetTotal(request):
        Total = 0
        invoice = request.session.get('invoice')
        if invoice:
            for product_uuid in invoice:
                productResponse = GetProduct.by_uuid(product_uuid)
                existing_qty = invoice.get(product_uuid)
                if productResponse['status']:
                    product = productResponse['object']
                    product_total = product.sellingPrice * existing_qty
                    Total += product_total
                else:
                    return productResponse

            return {'status': True, 'Total': Total}

        else:
            return 0

    @staticmethod
    def get_all_products(request):

        invoice = request.session.get('invoice')

        if invoice:
            uuidLst = list(invoice.keys())
        else:
            uuidLst = []

        products = Product.objects.filter(uuid__in=uuidLst)

        return products

    @staticmethod
    def add_qty(request, product_uuid, qty_to_add):
        existing_qty_in_session = InvoiceSession.get_product_qty_by_uuid(request, product_uuid)
        requested_qty_to_add = abs(qty_to_add)
        total_requested_qty = requested_qty_to_add + existing_qty_in_session

        productResponse = GetProduct.by_uuid(product_uuid)

        if productResponse['status']:

            product_object = productResponse['object']

            availability_status = is_requested_qty_of_product_available(product_object, total_requested_qty)

            if availability_status['status']:
                invoice = request.session.get('invoice')

                if invoice:
                    existing_qty = invoice.get(product_uuid)
                    if existing_qty:
                        invoice[product_uuid] += requested_qty_to_add
                    else:
                        invoice[product_uuid] = requested_qty_to_add
                else:
                    invoice = {product_uuid: requested_qty_to_add}

                request.session['invoice'] = invoice

                return {'status': True}

            else:
                return availability_status
        else:
            return productResponse

    @staticmethod
    def decrease_qty(request, product_uuid, qty_to_decrease):
        requested_qty_to_add = abs(qty_to_decrease)

        product = GetProduct.by_uuid(product_uuid)

        if product['status']:

            invoice = request.session.get('invoice')

            if invoice:

                existing_qty = invoice.get(product_uuid)

                if existing_qty:

                    if existing_qty == 1:
                        invoice.pop(product_uuid)
                    else:
                        invoice[product_uuid] -= requested_qty_to_add

                    request.session['invoice'] = invoice

                    return {'status': True}

            else:
                return {'status': False, 'error_code': 'YTD', 'error_msg': 'Product Not Found in Cart !'}

    @staticmethod
    def delete_product(request, product_uuid):

        invoice = request.session.get('invoice')

        if invoice:
            existing_qty = invoice.get(product_uuid)
            if existing_qty:
                invoice.pop(product_uuid)

        request.session['invoice'] = invoice

        return {'status': True}

    @staticmethod
    def delete_all(request):

        invoice = request.session.get('invoice')

        if invoice:
            del request.session['invoice']

        return {'status': True}


def InvoicePostRequestHandler(request):

    request_data = request.POST
    request_type = request_data.get('request_type')

    if request_type == 'add_product':
        requested_product_response = GetProduct.by_name(request_data['product_name'])
        requested_qty = int(request_data['qty'])
        if requested_product_response['status']:
            requested_product_uuid = str(requested_product_response['object'].uuid)
            response = InvoiceSession.add_qty(request, requested_product_uuid, requested_qty)
            return response
        else:
            return requested_product_response

    elif request_type == 'increase_product_qty':
        requested_product_response = GetProduct.by_uuid(request_data['requested_product'])
        if requested_product_response['status']:
            requested_product_uuid = str(requested_product_response['object'].uuid)
            response = InvoiceSession.add_qty(request, requested_product_uuid, 1)
            return response
        else:
            return requested_product_response

    elif request_type == 'decrease_product_qty':
        requested_product_response = GetProduct.by_uuid(request_data['requested_product'])
        if requested_product_response['status']:
            requested_product_uuid = str(requested_product_response['object'].uuid)
            response = InvoiceSession.decrease_qty(request, requested_product_uuid, 1)
            return response
        else:
            return requested_product_response

    elif request_type == 'delete_product':
        requested_product_response = GetProduct.by_uuid(request_data['requested_product'])
        if requested_product_response['status']:
            requested_product_uuid = str(requested_product_response['object'].uuid)
            response = InvoiceSession.delete_product(request, requested_product_uuid)
            return response
        else:
            return requested_product_response

    elif request_type == 'create_customer':
        fname = request_data['fname']
        lname = request_data['lname']
        phone = request_data['phone']
        email = request_data['email']
        address = request_data['address']

        customer_validation_response = validate_customer(fname, lname, phone, email, address)

        if customer_validation_response['status']:
            customer_model = Customer(fname=fname, lname=lname, phone=phone, email=email, address=address)
            customer_model.save()
            return {'status': True}
        else:
            return customer_validation_response

    elif request_type == 'select_customer':
        selected_customer_uuid = request_data['selected_customer']
        customer = Customer.objects.filter(uuid=selected_customer_uuid)
        return {'status': True}

    else:
        return {'status': False, 'error_code': 'RNF', 'error_msg': 'Invalid request'}
