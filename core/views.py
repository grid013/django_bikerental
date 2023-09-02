from django.shortcuts import render,redirect, get_object_or_404, HttpResponse
from core.models import Bike, Comment, Contact,Booking
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Avg
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.conf import settings
from core.forms import EditProfileForm

def index(request):
    bikes = Bike.objects.all()[:3]
    return render(request, "index.html", {"bikes":bikes})

@login_required(login_url="/accounts/login/")
def profile(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, "profile.html", {"user":request.user, "bookings":bookings})

@login_required(login_url="/accounts/login/")
def edit(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
        else:
            print(form.errors)
            return render(request, "edit.html" , {"form":form})
    form = EditProfileForm(instance=request.user)
    return render(request, "edit.html" , {"form":form})

@login_required(login_url="/accounts/login/")
def delete(request, id):
    get_object_or_404(Booking, pk=id).delete()
    return redirect("profile")

def gallery(request):
    return render(request, "gallery.html")

def bikes(request):
    bikes = Bike.objects.all()
    return render(request, "bikes.html", {"bikes":bikes})

def bike_detail(request, bike_id):
    bike = get_object_or_404(Bike, pk=bike_id)
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")
        start = request.POST.get("from")
        end = request.POST.get("to")
        rentfor = request.POST.get("rentfor")
        time = request.POST.get("time")
        ctx={
            "bike":bike,
            "start":start,
            "end":end,
            "rentfor":rentfor,
            "time":time,
            "amount":bike.price*int(rentfor)
        }
        request.session["bike"] = bike.id
        request.session["start"] = start
        request.session["end"] = end
        request.session["rentfor"] = rentfor
        request.session["time"] = time
        request.session["amount"] = ctx["amount"]
            
        return render(request, "confirm.html", ctx)
    else:
        ctx={"bike":bike}
        ratings = Comment.objects.filter(bike=bike).values("rating")
        total = ratings.count()
        dcount = ratings.annotate(dcount=Count("rating"))
        if dcount:
            for r in dcount:
                ctx["rating1"]=[r["dcount"], round(r["dcount"]/total)*100] if r["rating"] == 1 else [0,0] 
                ctx["rating2"]=[r["dcount"], round(r["dcount"]/total)*100] if r["rating"] == 2 else [0,0]
                ctx["rating3"]=[r["dcount"], round(r["dcount"]/total)*100] if r["rating"] == 3 else [0,0]
                ctx["rating4"]=[r["dcount"], round(r["dcount"]/total)*100] if r["rating"] == 4 else [0,0]
                ctx["rating5"]=[r["dcount"], round(r["dcount"]/total)*100] if r["rating"] == 5 else [0,0]
            ctx["avg"]=round((1*ctx["rating1"][0]+2*ctx["rating2"][0]+3*ctx["rating3"][0]+4*ctx["rating4"][0]+5*ctx["rating5"][0])/total)
        else:
            ctx["rating1"]=[0,0]
            ctx["rating2"]=[0,0]
            ctx["rating3"]=[0,0]
            ctx["rating4"]=[0,0]
            ctx["rating5"]=[0,0]
        ctx["range"]=range(5)
        ctx["total"]=total
    
        return render(request, "bike_detail.html", ctx)

@login_required(login_url="/accounts/login/")
def post_comment(request, bike_id):
    message = request.POST.get("comment")
    stars = request.POST.get("stars")
    bike = get_object_or_404(Bike, pk=bike_id)
    comment = Comment(bike=bike, user=request.user, message=message, rating=stars)
    comment.save()
    return redirect("bike_detail", bike_id=bike_id)

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        contact = Contact(name=name, email=email, message=message)
        contact.save()
        return render (request, "contact.html")
    return render(request, "contact.html")

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        bike = request.session["bike"]
        amount = request.session["amount"]
        bike = get_object_or_404(Bike, pk=bike)
        domain_url = settings.DOMAIN_URL
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success/{CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        "quantity":1,
                        "price_data":{
                            "unit_amount":int(amount)*100,
                            "product_data":{
                                "name":bike.name
                            },
                            "currency":"gbp"
                        }
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

def canceled(request):
    return redirect("bikes")

def success(request, session_id):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.retrieve(session_id)
    if session.payment_status == "paid":
        try:
            bike = request.session["bike"]
            start = request.session["start"] 
            end = request.session["end"]
            rentfor = request.session["rentfor"]
            time = request.session["time"]
            bb = get_object_or_404(Bike, pk=bike)

            booking = Booking(bike=bb, user=request.user, start=start, end=end, rentfor=rentfor, time=time)
            booking.save()
            for key in ["bike","start","end","rentfor","time"]:
                del request.session[key]
        except:
            raise Http404
    return render(request, "thanks.html")

def test(request):
    return render(request, "thanks.html")