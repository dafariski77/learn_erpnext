import frappe
import json
from werkzeug.wrappers import Response   
from learn_erpnext.utils.api_response import ApiResponse
from typing import List
from learn_erpnext.types.doctype.product.types import IProduct
from pydantic import ValidationError
from learn_erpnext.api.products.dto.create_product import CreateProductDto
from learn_erpnext.api.products.dto.update_product import UpdateProductDto


@frappe.whitelist(methods=["GET"], allow_guest=True)
def get_all() -> Response:
    products: List[IProduct] = frappe.get_list("Product", {}, ["*"])

    return ApiResponse(200, "Success", products)


@frappe.whitelist(methods=["GET"], allow_guest=True)
def get_by_id():
    try:
        params = frappe.form_dict
        product_id = params.get("id")

        if not frappe.db.exists("Product", product_id):
            return ApiResponse(404, "Product not found")

        product: IProduct = frappe.get_doc("Product", product_id)

        return ApiResponse(200, "Success", product.as_dict())
    except Exception as e:
        return ApiResponse(500, "Internal server error")


@frappe.whitelist(methods=["POST"], allow_guest=True)
def create():
    try:
        request = frappe.local.request.data
        request_body = json.loads(request)

        data = CreateProductDto.from_request(request_body)

        product_doc = frappe.get_doc({
            "doctype": "Product",
            "product_name": data.product_name,
            "description": data.description,
            "stock": data.stock,
            "price": data.price,
        }).insert()

        return ApiResponse(201, "Success", product_doc.as_dict())
    except ValidationError as e:
        return ApiResponse(400, "Failed create new product", None, str(e))
    except Exception as e:
        return ApiResponse(500, "Internal server error", None, str(e))


@frappe.whitelist(methods=["PUT"], allow_guest=True)
def update():
    try:
        request = frappe.local.request.data
        request_body = json.loads(request)

        data = UpdateProductDto.from_request(request_body)

        if not frappe.db.exists("Product", data.product_id):
            return ApiResponse(404, "Product not found")

        product_doc: IProduct = frappe.get_doc("Product", data.product_id)

        product_doc.product_name = data.product_name
        product_doc.description = data.description
        product_doc.stock = data.stock
        product_doc.price = data.price

        product_doc.save()

        return ApiResponse(201, "Success", product_doc.as_dict())
    except ValidationError as e:
        return ApiResponse(400, "Failed create new product", None, str(e))
    except Exception as e:
        return ApiResponse(500, "Internal server error", None, str(e))


@frappe.whitelist(methods=["DELETE"], allow_guest=True)
def destroy():
    params = frappe.form_dict
    product_id = params.get("id")

    if not frappe.db.exists("Product", product_id):
        return ApiResponse(404, "Product not found")

    product_doc = frappe.get_doc("Product", product_id)

    product_doc.delete()

    return ApiResponse(200, "Success")
