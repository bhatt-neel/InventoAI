from .validation import *

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

        products = Product.objects.filter(uuid__in = uuidLst)

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
    def decrease_qty(request, product_uuid, qty_to_add):
        existing_qty_in_session = InvoiceSession.get_product_qty_by_uuid(request, product_uuid)
        requested_qty_to_add = abs(qty_to_add)
        total_requested_qty = requested_qty_to_add + existing_qty_in_session

        product = GetProduct.by_uuid(product_uuid)

        if product['status']:
            product_object = product['object']

            availability_status = is_requested_qty_of_product_available(product_object, total_requested_qty)

            if availability_status['status']:
                invoice = request.session.get('invoice')

                if invoice:
                    existing_qty = invoice.get(product_uuid)
                    if existing_qty:
                        if existing_qty == 1:
                            invoice.pop(product_uuid)
                        else:
                            invoice[product_uuid] -= requested_qty_to_add

                request.session['invoice'] = invoice

            else:
                return availability_status

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
        requested_product_response = GetProduct.by_name(request_data['product_name'])
        requested_qty = int(request_data['qty'])
        if requested_product_response['status']:
            requested_product_uuid = str(requested_product_response['object'].uuid)
            response = InvoiceSession.add_qty(request, requested_product_uuid, requested_qty)
            return response
        else:
            return requested_product_response

    elif request_type == 'decrease_product_qty':
        print('decrease_product_qty')

    elif request_type == 'delete_product':
        print('delete_product')



    # product_name = request_data['product_name']
    # initial_requested_qty = int(request_data['qty'])

#     post_data = request.POST
#     request_type = post_data.get('request_type')
#
#         requested_product_validation = GetProduct.by_name(product_name)
#
#         if requested_product_validation['status']:
#             requested_product_object = requested_product_validation['object']
#             product_uuid = str(requested_product_object.uuid)
#             InvoiceSession.add_qty(request, product_uuid, initial_requested_qty)
#             print(InvoiceSession.get_product_qty_by_uuid(request, product_uuid))






