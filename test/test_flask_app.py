import unittest
import json
import requests

class VoCTest(unittest.TestCase):

    def test_main_page(self):
        url = "http://localhost:3000/"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

    def test_product_list(self):
        url = "http://localhost:3000/"
        response = requests.get(url+'api/product-list')
        self.assertTrue('products' in response.json())

    def test_get_product(self):
        url = "http://localhost:3000/"
        response = requests.get(url+'api/product-list')
        products_list = response.json()['products']
        product_id = products_list[0]['id']
        response_prod = requests.get(url+'api/product?productId=' + product_id)
        self.assertTrue('features' in response_prod.json())

if __name__ == '__main__':
    unittest.main()
