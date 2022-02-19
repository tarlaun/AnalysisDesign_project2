from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from .forms import AccountCreationForm, LoginForm, SignUpForm
from .models import UserType, Doctor, Account, Order, Expertise, FavDoctors
from django.views import generic
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages

from .forms import AccountCreationForm, LoginForm, SignUpForm
from .models import UserType, Doctor, Order, Expertise, FavDoctors

LOGIN_REDIRECT_URL = "/accounts/signin/"


def being_doctor_check(user):
    return user.user_type == UserType.DOCTOR


# register A User using Account Creation Form And django auth app
@csrf_protect
def register(request):
    # form = AccountCreationForm()
    form = SignUpForm()

    if request.method == "POST":
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("signin")
        else:
            # TODO error
            pass

    context = {"form": form}

    return render(request, "account/register.html", context)


@csrf_protect
def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if being_doctor_check(user):
                return redirect("expertise_orders_list")
            else:
                return redirect("patient_orders_list")
        else:
            return HttpResponse(
                'Username or Password is incorrect. <a href="">Return to login</a>'
            )

    # form = AccountCreationForm()
    form = LoginForm()
    context = {"form": form}
    return render(request, "account/login.html", context)


# log out from site
@login_required(login_url=LOGIN_REDIRECT_URL)
def signout(request):
    logout(request)
    return render(request, "home.html", {})


@login_required(login_url=LOGIN_REDIRECT_URL)
def home(request):
    return HttpResponse("Home Page")


# @login_required
# @user_passes_test(being_doctor_check)
@login_required(login_url=LOGIN_REDIRECT_URL)
def expertise_orders_list(request):
    if not request.user.is_authenticated:
        return HttpResponse("Log in")
    if request.user.user_type == UserType.PATIENT:
        return HttpResponse("You are not a doctor")
    doctor = Doctor.objects.get(user=request.user)
    expertise = doctor.expertise
    orders_list = Order.objects.filter(
        expertise=expertise, doctor=doctor, accepted=False
    )
    return render(
        request, "account/expertise_orders_list.html", {"orders_list": orders_list}
    )


# @login_required
# @user_passes_test(being_doctor_check)
# Change Doctor Status of Order in DB
@login_required(login_url=LOGIN_REDIRECT_URL)
def accept_order(request, order_id):
    if not request.user.is_authenticated:
        return HttpResponse("Log in")
    if request.user.user_type == UserType.PATIENT:
        return HttpResponse("You are not a doctor")
    order = Order.objects.get(id=order_id)
    if order.accepted:
        return HttpResponse("This Order was accepted by another doctor!")
    doctor = Doctor.objects.get(user=request.user)
    # order.doctor = doctor
    order.accepted = True
    order.save()
    # doctor.not_processed_income += order.expertise.price
    doctor.save()
    return redirect("expertise_orders_list")


# View Expertise List For Patient
class ExpertiseView(generic.ListView):
    template_name = "account/expertise_list.html"
    context_object_name = "expertise_list"

    def get_queryset(self):
        return Expertise.objects.all()


@login_required(login_url=LOGIN_REDIRECT_URL)
class DoctorView(generic.ListView):
    template_name = "account/doctor_list.html"
    context_object_name = "doctor_list"

    def get_queryset(self):
        return Doctor.objects.all()


# View Request Page After Choosing Expertise
@login_required(login_url=LOGIN_REDIRECT_URL)
def request_for_chosen_expertise(request, exp_id):
    expertise = get_object_or_404(Expertise, pk=exp_id)
    return render(
        request, "account/request_for_expertise.html", {"expertise": expertise}
    )


# ADD Order Into DB
@login_required(login_url=LOGIN_REDIRECT_URL)
def add_order(request, doc_id):
    if not request.user.is_authenticated:
        return HttpResponse("Log in")
    if request.user.user_type != UserType.PATIENT:
        return HttpResponse("You are not a Patient")
    doctor = get_object_or_404(Doctor, pk=doc_id)
    exp_id = doctor.expertise.id
    address = request.POST["address"]
    details = request.POST["details"]
    o = Order(
        user_id=request.user.id,
        expertise_id=exp_id,
        doctor_id=doctor.user.id,
        address=address,
        details=details,
    )
    o.save()
    return HttpResponseRedirect(reverse("patient_orders_list"))


# View Patient's Previous Orders List
@login_required(login_url=LOGIN_REDIRECT_URL)
def patient_orders_list(request):
    orders_list = Order.objects.filter(user_id=request.user.id)
    return render(
        request, "account/patient_orders_list.html", {"orders_list": orders_list[::-1]}
    )


# save a score for orders
@login_required(login_url=LOGIN_REDIRECT_URL)
def rate_order(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        val = request.POST.get("val")
        order = Order.objects.get(id=order_id)
        order.score = val
        order.save()
        return JsonResponse({"success": "true", "score": val}, safe=False)
    return JsonResponse({"success": "false"})


# save comment for orders
@login_required(login_url=LOGIN_REDIRECT_URL)
def comment_for_order(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        order = Order.objects.get(id=order_id)
        comment = request.POST.get("comment")
        order.comment = comment
        order.save()
        return JsonResponse({"success": "true"}, safe=False)
    return JsonResponse({"success": "false"})


# save complaint for orders
@login_required(login_url=LOGIN_REDIRECT_URL)
def complaint_for_order(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        order = Order.objects.get(id=order_id)
        complaint = request.POST.get("complaint")
        order.complaint = complaint
        order.save()
        return JsonResponse({"success": "true"}, safe=False)
    return JsonResponse({"success": "false"})


# gives list of all doctors
@login_required(login_url=LOGIN_REDIRECT_URL)
def doctor_list(request, exp_id):
    expertise = get_object_or_404(Expertise, pk=exp_id)
    docs_list = Doctor.objects.filter(expertise=expertise)
    return render(
        request,
        "account/doctor_list.html",
        {"doctor_list": docs_list, "exp_name": expertise.name},
    )


# get all requests for doctor which she/he has not accepted yet
@login_required(login_url=LOGIN_REDIRECT_URL)
def request_for_chosen_doctor(request, doc_id):
    doctor = get_object_or_404(Doctor, pk=doc_id)
    exp = doctor.expertise.name
    return render(
        request,
        "account/request_for_doc.html",
        {
            "doc_name": doctor.user.first_name,
            "doc_lname": doctor.user.last_name,
            "doc_id": doctor.user.id,
            "exp": exp,
        },
    )


# get requests for doctor which she/he accepted but not finished
@login_required(login_url=LOGIN_REDIRECT_URL)
def active_orders(request):
    doctor = Doctor.objects.get(user=request.user)
    expertise = doctor.expertise
    orders_list = Order.objects.filter(
        expertise=expertise, doctor=doctor, accepted=True, finished=False
    )
    return render(request, "account/active_orders.html", {"orders_list": orders_list})


# get requests for doctor which she/he finished
@login_required(login_url=LOGIN_REDIRECT_URL)
def finished_orders(request):
    doctor = Doctor.objects.get(user=request.user)
    expertise = doctor.expertise
    orders_list = Order.objects.filter(
        expertise=expertise, doctor=doctor, accepted=True, finished=True
    )
    return render(request, "account/finished_orders.html", {"orders_list": orders_list})


@login_required(login_url=LOGIN_REDIRECT_URL)
def all_doctors(request):
    doctors_list = Doctor.objects.all()
    if FavDoctors.objects.filter(user=request.user).exists():
        fav_doctors = get_object_or_404(FavDoctors, user=request.user)
        all_fav_doctors = fav_doctors.favorite_doctors.all()
    else:
        all_fav_doctors = []

    return render(
        request,
        "account/list_of_doctors.html",
        {"doctors_list": doctors_list, "fav_doctors": all_fav_doctors},
    )


@login_required(login_url=LOGIN_REDIRECT_URL)
def doc_pro(request, doc_id):
    doctor = get_object_or_404(Doctor, pk=doc_id)
    scores = 0
    count = 0
    orders_list = Order.objects.filter(doctor=doctor, accepted=True)
    final_orders = []
    for order in orders_list:
        if order.score > 0 or order.comment != "":
            if order.score > 0:
                scores += order.score
                count += 1
            final_orders.append(order)

    if count == 0:
        score_mean = 0
    else:
        score_mean = scores / count
    score_mean = round(score_mean, 1)
    if len(final_orders) > 0:
        final_orders = final_orders[::-1]

    return render(
        request,
        "account/doctor_profile.html",
        {"doctor": doctor, "orders": final_orders, "score_mean": score_mean},
    )


@login_required(login_url=LOGIN_REDIRECT_URL)
def fav_doctor(request, doc_id):
    doctor = get_object_or_404(Doctor, pk=doc_id)

    if FavDoctors.objects.filter(user=request.user).exists():
        fav_doctors = get_object_or_404(FavDoctors, user=request.user)
    else:
        fav_doctors = FavDoctors(user=request.user)
        fav_doctors.save()

    fav_doctors.favorite_doctors.add(doctor)
    fav_doctors.save()

    return redirect("all_doctors")
    # return render(request, 'account/list_of_doctors.html', {'doctors_list': doctors_list, 'fav_doctors': fav_doctors.favorite_doctors.all()})


@login_required(login_url=LOGIN_REDIRECT_URL)
def unfav_doctor(request, doc_id):
    doctor = get_object_or_404(Doctor, pk=doc_id)
    fav_doctors = get_object_or_404(FavDoctors, user=request.user)

    fav_doctors.favorite_doctors.remove(doctor)
    fav_doctors.save()

    return redirect("all_doctors")


@login_required(login_url=LOGIN_REDIRECT_URL)
def favorite_doctors(request):
    if FavDoctors.objects.filter(user=request.user).exists():
        fav_doctors = get_object_or_404(FavDoctors, user=request.user)
        all_fav_doctors = fav_doctors.favorite_doctors.all()
    else:
        all_fav_doctors = []

    return render(
        request, "account/fav-doctors.html", {"fav_doctors_list": all_fav_doctors}
    )


@login_required(login_url=LOGIN_REDIRECT_URL)
def unfav_doctor_from_favs(request, doc_id):
    doctor = get_object_or_404(Doctor, pk=doc_id)
    fav_doctors = get_object_or_404(FavDoctors, user=request.user)

    fav_doctors.favorite_doctors.remove(doctor)
    fav_doctors.save()

    return redirect("favorite_doctors")


@login_required(login_url=LOGIN_REDIRECT_URL)
def online_payment(request):
    return render(request, 'account/payment-page.html')

@login_required(login_url=LOGIN_REDIRECT_URL)
def online_payment_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.paid = True
    if order.expertise.price <= order.user.wallet:
        order.doctor.user.wallet += order.expertise.price
        order.user.wallet -= order.expertise.price
        order.save()
        order.user.save()
        order.doctor.user.save()
        return redirect("patient_orders_list")
        # TODO notification for successful
    else:
        temp = order.expertise.price
        order.expertise.price -= order.user.wallet
        order.doctor.user.wallet += temp
        order.save()
        order.doctor.user.save()
        return render(request, 'account/payment-page.html', context={"order": order})

@login_required(login_url=LOGIN_REDIRECT_URL)
def add_to_wallet(request):
    if request.method == "POST":
        user = request.user
        current_wallet = user.wallet
        user.wallet = current_wallet + int(request.POST.get("amount"))
        user.save()
        messages.add_message(request, messages.SUCCESS, 'Successfully added to you wallet')
        # print("---------", request.POST.get("amount"))
        # print("---------", request.POST.get("card_number1"))
        # print("---------", request.POST.get("card_number2"))
        # print("---------", request.POST.get("card_number3"))
        # print("---------", request.POST.get("card_number4"))
        # print("---------", request.POST.get("card_type"))
        # print("---------", request.POST.get("exp_date"))
        # print("---------", request.POST.get("cvv"))

        return redirect("patient_orders_list")
    return JsonResponse({"success": "false"})


@login_required(login_url=LOGIN_REDIRECT_URL)
def pay(request, order_id):
    if request.method == "POST":
        user = request.user
        order = get_object_or_404(Order, pk=order_id)
        user.wallet = user.wallet + int(request.POST.get("amount")) - order.expertise.price
        user.save()
        return redirect("patient_orders_list")
    return JsonResponse({"success": "false"})

# Finish the order aftre doctor confirmed payment
@login_required(login_url=LOGIN_REDIRECT_URL)
def finish_the_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.finished = True
    order.save()
    return redirect("active_orders")


@login_required(login_url=LOGIN_REDIRECT_URL)
def delete_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.delete()
    return redirect("patient_orders_list")


def help(request):
    return render(request, 'account/help.html')
