from django.test import TestCase
from .models import Account, Expertise, Doctor, Order
from .views import rate_order


class OrderTest(TestCase):
    def create_user(
        self,
        first_name="mmd",
        last_name="mmdi",
        username="mmd.mmdi",
        password="mmdpass",
        email="mmd@gmail.com",
        user_type=2,
        phone_number="09129121112",
    ):
        return Account.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
            user_type=user_type,
            phone_number=phone_number,
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
        complaint='very late'
    ):
        return Order.objects.create(
            user=self.create_user(),
            doctor=self.create_doctor(),
            expertise=self.create_expertise(),
            address=address,
            details=details,
            score=score,
            comment=comment,
            complaint=complaint
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

    def test_rate_order(self):
        test_order = self.create_order()
        score_val = "4"
        response = self.client.post("/accounts/rate/", {"order_id": 1, "val": score_val})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding="utf8"),
            {"success": "true", "score": score_val},
        )

    def test_comment_order(self):
        test_order = self.create_order()
        comment = "از سرویس راضی بودم ممنون"
        response = self.client.post("/accounts/comment/", {"order_id": 1, "comment": comment})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding="utf8"),
            {"success": "true"},
        )

    def test_complaint_order(self):
        test_order = self.create_order()
        complaint = "هزینه بسیار زیاد بود."
        response = self.client.post("/accounts/complaint/", {"order_id": 1, "complaint": complaint})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding="utf8"),
            {"success": "true"},
        )
