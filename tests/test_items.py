import http
import json
import pytest
from market import api, app, db
from market.models import Item, User
from unittest.mock import patch
from api import routes


class TestItems:
    id = []

    def test_get_items_with_db(self):
        client = app.test_client()
        resp = client.get('/items')

        assert resp.status_code == http.HTTPStatus.OK

    @patch('api.services.item_service.ItemService.fetch_all_items', autospec=True)
    def test_get_items_mock_db(self, mock_db_call):
        client = app.test_client()
        resp = client.get('/items')

        mock_db_call.assert_called_once()
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json) == 0

    def test_create_item_with_db(self):
        client = app.test_client()
        data = {
            'name': 'tester',
            'price': 12,
            'barcode': '9214789632188',
            'description': 'st',

        }

        resp = client.post('/items', data=json.dumps(data), content_type='application/json')
        assert resp.status_code == http.HTTPStatus.CREATED
        assert data['name'] == 'tester'
        TestItems.id.append(data['name'])

    def test_create_item_with_mock_db(self):
        with patch("api.db.session.add", autospec=True) as mock_session_add, \
                patch("api.db.session.commit", autospec=True) as mock_session_commit:
            client = app.test_client()
            data = {
                'name': 'tester',
                'price': 12,
                'barcode': '9214789632188',
                'description': 'st',
            }
            resp = client.post('/items', data=json.dumps(data), content_type='application/json')
            mock_session_add.assert_called_once()
            mock_session_commit.assert_called_once()

    def test_update_item_with_db(self):
        client = app.test_client()
        url = f'/items/{self.id[0]}'
        data = {
            'name': 'Update name2',
            'price': 32,
            'barcode': '3214755532172',
            'description': 'Updated desciption',
        }
        client.put(url, data=json.dumps(data), content_type='application/json')

        assert data['name'] == 'Update name2'


class Test_Flask_App:
    def test_home_page(self):
        client = app.test_client()
        resp = client.get('/home')

        assert resp.status_code == http.HTTPStatus.OK

    def test_market_page(self):
        client = app.test_client()
        resp = client.get('/market')
        assert resp.status_code == http.HTTPStatus.FOUND

    def test_register_page(self):
        client = app.test_client()
        resp = client.get('/register')
        assert resp.status_code == http.HTTPStatus.OK

    def test_login_page(self):
        client = app.test_client()
        resp = client.get('/login')
        assert resp.status_code == http.HTTPStatus.OK

    def test_logout_page(self):
        client = app.test_client()
        resp = client.get('/logout')
        assert resp.status_code == http.HTTPStatus.FOUND


class Test_Model:
    def test_password_hashing(self):
        u1 = User(username='u1')
        u1.password = 'topolya'
        assert u1.check_password_correction('tut') == False
        assert u1.check_password_correction('topolya') == True

    def test_can_purchase(self):
        budget = 2000
        i = Item(name='Iphone 10', description='description', barcode='123456789123', price=300)
        assert budget > i.price

    def test_can_sell(self):
        i1 = Item(name='TurboBookPro', description='The best invention by Apple', barcode='123456654456', price=2500)
        i2 = Item(name='MacBookPro', description='description2', barcode='123456789321', price=2000)
        item_obj = 'TurboBookPro'
        items = [i1.name, i2.name]
        assert item_obj in items

    def test_buy(self):
        u = User(username='Test_name', budget=1000)
        i = Item(name='TurboBookPro',description='The best invention ', barcode='123456654450', price=500)
        return u.budget >= i.price

    def test_sell(self):
        u = User(username='Test_name', budget=1000)
        i = Item(name='TurboBookPro',description='The best ', barcode='123456654458', price=500)
        start_budget = u.budget
        u.budget += i.price
        return u.budget >= start_budget
