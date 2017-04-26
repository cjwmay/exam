from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from models import User,Trip
import bcrypt
# Create your views here.
def index(request):
	return render(request, "examapp/index.html")
def logout(request):
	request.session.flush()
	return redirect('/main')
def checkregister(request):
	if request.method == "POST":
		data  = {
			"f_name" : request.POST['f_name'],
			"l_name" : request.POST['l_name'],
			"email" : request.POST['email'],
			"password": request.POST["con_pw"],
			"con_pw": request.POST["con_pw"],
		}
		print data['email']
		result = User.objects.register(data)
		if result['error'] == None:
			request.session['user'] = result['user'].first_name + result['user'].last_name
			request.session['userid'] = result['user'].id
			return redirect('/travels')
		else:
			for error in result['error']:
				messages.add_message(request,messages.ERROR,error)
			print result['error']
			return redirect('/main')
	else:
		messages.add_message(request,messages.ERROR,'Please Login or register')
		return redirect('/main')
def checklogin(request):
	if request.method == "POST":
		data  = {
			"email" : request.POST['email'],
			"password": request.POST['password'],
		}
		result = User.objects.login(data)
		if result['error'] == None:
			request.session['user'] = result['user'].first_name + result['user'].last_name
			request.session['userid'] = result['user'].id
			print request.session['userid']
			return redirect('/travels')
		else:
			for error in result['error']:
				messages.add_message(request,messages.ERROR,error)
			print result['error']
			print User.objects.all().values()
			return redirect('/main')
	return redirect('/main')
def success(request):
	try:
		# Trip.objects.all().delete()
		print Trip.objects.all()
		request.session['user']
		user = User.objects.get(id = request.session['userid'])
		trips = Trip.objects.filter(user = user)
		allusertrips = Trip.objects.all()
		context = {
			"trips":trips,
			"allusertrips":allusertrips,
		}
		return render(request,"examapp/success.html",context)
	except:
		messages.add_message(request,messages.ERROR,"Please Log in!!!!")
		return redirect('/main')
def add(request):
	print Trip.objects.all()
	try:
		request.session['user']
		return render(request,"examapp/add.html")
	except:
		messages.add_message(request,messages.ERROR,"Please Log in!!!!")
		return redirect('/main')
def addcheck(request):
	if request.method == "POST":
		user = User.objects.get(id = request.session['userid'])
		data = {
			"plan_user":user,
			"user":user,
			"destination":request.POST['destination'],
			"plan":request.POST['plan'],
			"start_date":request.POST['start_date'],
			"end_date":request.POST['end_date'],
		}
		result = Trip.objects.addtrip(data)
		if result["errors"] != None:
			for error in result['errors']:
				messages.add_message(request, messages.ERROR, error)
			return redirect('/add')
		else:
			return redirect('/travels')
	return redirect('/add')
def tripbyid(request,id):
	try:
		request.session['user']
		trip = Trip.objects.filter(id = id)
		context={
			"trips":trip,
		}
		return render(request,"examapp/trip1.html",context)
	except:
		messages.add_message(request,messages.ERROR,"Please Log in!!!!")
		return redirect('/main')
def join(request):
	if request.method == "POST":
		tripid = request.POST['tripid']
		trip = Trip.objects.get(id = tripid)
		userid = request.session['userid']
		user = User.objects.get(id = userid)
		user.tripusers.add(trip)
		return redirect('/travels')
	else:
		return redirect('/main')
