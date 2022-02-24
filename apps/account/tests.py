from cgi import test
from django.test import TestCase, RequestFactory
from .models import Account, Expertise, Doctor, Order, FavDoctors
from django.urls import reverse
from .views import (
    all_doctors,
    fav_doctor,
    unfav_doctor,
    favorite_doctors,
    unfav_doctor_from_favs,
    finish_the_order,
    active_orders,
    finished_orders,
    add_to_wallet,
    delete_order,
    pay,
    confirm_cash_pay
)


class OrderTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = Account.objects.create(
            username="baharkh", email="baharkh127@gmail.com", password="top_secret"
        )

    def create_user(
        self,
        first_name="mmd",
        last_name="mmdi",
        username="mmd.mmdi",
        password="mmdpass",
        email="mmd@gmail.com",
        user_type=2,
        phone_number="09129121112",
        wallet=0
    ):
        return Account.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
            user_type=user_type,
            phone_number=phone_number,
            wallet=wallet,
        )

    def create_doctor(
        self,
        not_processed_income=40,
    ):
        return Doctor.objects.create(
            expertise=self.create_expertise(),
            user=self.create_user(username="X", user_type=1),
            not_processed_income=not_processed_income,
        )

    def create_expertise(
        self,
        name="Brain",
        price=1000,
    ):
        return Expertise.objects.create(
            name=name,
            price=price,
        )

    def create_order(
        self,
        address="Tehran",
        details="I am sick",
        score="3",
        comment="Not bad!",
        complaint="very late",
    ):
        return Order.objects.create(
            user=self.create_user(),
            doctor=self.create_doctor(),
            expertise=self.create_expertise(),
            address=address,
            details=details,
            score=score,
            comment=comment,
            complaint=complaint,
        )

    def create_fav_doctors(self, user):
        return FavDoctors.objects.create(
            user=user,
        )

    def test_order_creation(self):
        test_order = self.create_order()
        self.assertTrue(isinstance(test_order, Order))

    def test_user_creation(self):
        test_user = self.create_user()
        self.assertTrue(isinstance(test_user, Account))

    def test_expertise_creation(self):
        test_expertise = self.create_expertise()
        self.assertTrue(isinstance(test_expertise, Expertise))

    def test_doctor_creation(self):
        test_doctor = self.create_doctor()
        self.assertTrue(isinstance(test_doctor, Doctor))

    def test_fav_doctors_creation(self):
        test_user = self.create_user(username="X", user_type=1)
        test_fav_doctos = self.create_fav_doctors(test_user)
        self.assertTrue(isinstance(test_fav_doctos, FavDoctors))

    def test_rate_order(self):
        user = Account.objects.create_user(username="mmd", password="mmdpass")
        self.client.login(username="mmd", password="mmdpass")
        test_order = self.create_order()
        score_val = "4"
        response = self.client.post(
            "/accounts/rate/", {"order_id": 1, "val": score_val}
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding="utf8"),
            {"success": "true", "score": score_val},
        )

    def test_comment_order(self):
        user = Account.objects.create_user(username="mmd", password="mmdpass")
        self.client.login(username="mmd", password="mmdpass")
        test_order = self.create_order()
        comment = "از سرویس راضی بودم ممنون"
        response = self.client.post(
            "/accounts/comment/", {"order_id": 1, "comment": comment}
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding="utf8"),
            {"success": "true"},
        )

    def test_complaint_order(self):
        user = Account.objects.create_user(username="mmd", password="mmdpass")
        self.client.login(username="mmd", password="mmdpass")
        test_order = self.create_order()
        complaint = "هزینه بسیار زیاد بود."
        response = self.client.post(
            "/accounts/complaint/", {"order_id": 1, "complaint": complaint}
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding="utf8"),
            {"success": "true"},
        )

    def test_all_doctors(self):
        request = self.factory.get("/account/all_doctors/")
        request.user = self.user

        url = reverse("all_doctors")
        response = all_doctors(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "List of Doctors")

    def test_favorite_doctor(self):
        request = self.factory.get("/account/all_doctors/favorite/")
        request.user = self.user

        test_fav_doctors = self.create_fav_doctors(request.user)
        test_doctor = self.create_doctor()
        test_fav_doctors.favorite_doctors.add(test_doctor)

        response = fav_doctor(request, test_doctor.user.id)

        self.assertEqual(response.status_code, 302)

    def test_unfavorite_doctor(self):
        request = self.factory.get("/account/all_doctors/favorite/")
        request.user = self.user

        test_fav_doctors = self.create_fav_doctors(request.user)
        test_doctor = self.create_doctor()
        test_fav_doctors.favorite_doctors.add(test_doctor)

        response = unfav_doctor(request, test_doctor.user.id)

        self.assertEqual(response.status_code, 302)

    def test_favorite_doctors_list(self):
        request = self.factory.get("/account/fav_doctors/")
        request.user = self.user

        response = favorite_doctors(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "List of Favorite Doctors")

    def test_unfavorite_from_favs_doctor(self):
        request = self.factory.get("/account/fav_doctors")
        request.user = self.user

        test_fav_doctors = self.create_fav_doctors(request.user)
        test_doctor = self.create_doctor()
        test_fav_doctors.favorite_doctors.add(test_doctor)

        response = unfav_doctor_from_favs(request, test_doctor.user.id)

        self.assertEqual(response.status_code, 302)
        
    def test_active_orders(self):
        request = self.factory.get("/account/active_orders/")
        test_doctor = self.create_doctor()
        request.user = test_doctor.user
        
        response = active_orders(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Active Orders")
        
    def test_finished_orders(self):
        request = self.factory.get("/account/finished_orders/")
        test_doctor = self.create_doctor()
        request.user = test_doctor.user

        response = finished_orders(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Done Orders")

    def test_charge_wallet(self):
        request = self.factory.get("/accounts/add-to-wallet/")
        test_user = self.create_user()
        request.user = test_user

        response = add_to_wallet(request)
        self.assertEqual(response.status_code, 200)

    def test_payment(self):
        request = self.factory.get("/accounts/pay/1")
        test_order = self.create_order()
        request.user = test_order.user
        response = pay(request, 1)
        self.assertEqual(response.status_code, 200)


    def test_delete_order(self):
        order = self.create_order()
        pk = order.pk
        order_by_pk = Order.objects.get(pk=order.pk)
        order_by_pk.delete()
        self.assertFalse(Order.objects.filter(pk=pk).exists())


    def test_confirm_cash_pay(self):
        request = self.factory.get("/accounts/confirm_cash_pay/1")
        test_order = self.create_order()
        request.user = test_order.user
        response = confirm_cash_pay(request, 1)
        self.assertEqual(response.status_code, 302)

