# DociCome

# سامانه درمان سیار

## overview    
با توجه به شیوع اپیدمی کرونا، اغلب مردم از حضور در بیمارستان‌ها -از خوف ابتلا به این بیماری- جهت درمان بیماری‌های غیر حاد و انجام آزمایش‌ها امتناع می‌ورزند. به همین جهت برخی از این بیماری‌ها درمان یا شناسایی نمی‌شود و در نهایت موجب حاد شدن این بیماری‌ها می‌شود.
هدف این سامانه این است که دسترسی بیماران را به خدمات درمانی و پزشکان متخصص هر حوزه در محل حضور بیمار تسهیل کند.

# نحوه نصب پیش نیاز‌ها و اجرای پروژه:

## Install Requirements
    pip install -r requirements.txt 

## Run Server
    python3 manage.py runserver 0:8000

## Create Migrations
    python3 manage.py migrate

## Create Admin User
    python3 manage.py createsuperuser


# ویژگی‌های سامانه

### مشاهده امکانات وبسایت
![help](images/help.png)

## بیماران
![landing](images/landing.png)
### امکان ورود و ثبت نام بیماران در سامانه
![login](images/login.png)
![signup](images/signup.png)
### امکان انتخاب خدمات مورد نیاز از میان لیست خدمات موجود
![expertises](images/expertises.png)
### امکان مشاهده درخواست‌های داده شده
![orders](images/orders.png)
### امکان ثبت امتیاز
![score](images/score.png)
### امکان ثبت نظر
![comment](images/comment.png)
### امکان ثبت شکایت
![comment](images/comment.png)
### امکان مشاهده پزشکان هر تخصص
![expertise'sDoctor](images/expertise'sDoctor.png)
### امکان ثبت درخواست
![submitOrder](images/submitOrder.png)
### مشاهده لیست پزشکان
![docList](images/docList.png)
### مشخص کردن لیست پزشکان موردعلاقه و مشاهده لیست آنها
![fav](images/fav.png)
### شارژ کیف پول و پرداخت آنلاین
![payment](images/payment.png)
### مشاهده پروفایل پزشکان و ثبت درخواست مستقیم
![pro](images/pro.png)

## پزشکان

### امکان ورود به سامانه 
![login](images/login.png)
### امکان مشاهده درخواست‌های موجود مرتبط با تخصص
![orders](images/doctor.png)
### امکان مشاهده درخواست‌های پذیرفته شده
![accepted](images/accepted.png)
### امکان مشاهده درخواست‌های اتمام یافته
![done](images/done.png)
