from django.shortcuts import render,redirect
from .models import Meds,Expiry
from datetime import datetime
# Create your views here.



def index(request):
    en = Meds.objects.all()
    data = {
        'title':"Home",
        'en':en,
    }
    return render(request,'index.html',data)
def addmednew(request):
    if request.method == "POST":
        name = request.POST['name']
        medsperstrip = request.POST['medperstrip']
        repday = request.POST['repday']
        try:
            desc = request.POST['desc']
        except:
            desc = ""
        m = Meds(name=name,perstrip=medsperstrip,description=desc,rtime=repday)
        m.save()
        data={
            'title':'Add New Med',
            'msg':True,
        }
        return render(request,'addmednew.html',data)
    else:
        data={
            'title':'Add New Med',
        }
        return render(request,'addmednew.html',data)

def schedule(request):
    return render(request,'schedule.html')

def caldate(expdate):
    a = datetime.today().strftime('%Y-%m-%d')
    ap = a.split('-')
    ep = str(expdate).split("-")
    final = list()
    i = 0
    while(i<3):
        final.append(int(ep[i])-int(ap[i]))
        i += 1
    i = (final[0]*365) + (final[1]*30) + final[2]
    return i
def addstock(request):
    m = Meds.objects.all()
    if request.method == 'POST':
        id = request.POST['id']
        qty = request.POST['qty']
        exp = request.POST['exp']
        med = Meds.objects.get(id=id)
        ms = Expiry(name=med,qty=qty,expiry=exp)
        ms.save()
        med.qty += int(qty)
        stkdays = int(med.qty)*int(med.perstrip)/int(med.rtime)
        expdays = caldate(exp)
        if stkdays>expdays and med.stkdays <= expdays:
            med.stkdays = expdays
        elif stkdays<expdays:
            med.stkdays = stkdays
        med.save()
        


        # try:
        #     ms = Expiry.objects.get(name=med)        #   name.id = id check this out
        #     ms.qty = qty
        #     ms.expiry = exp
        #     ms.save()
        #     med.qty=qty
        #     med.stkdays = med.qty*med.perstrip/med.rtime
        #     med.save()
        # except:
        #     ms = Expiry(name=med,qty=qty,expiry=exp)
        #     ms.save()
        #     med.qty=qty
        #     med.stkdays = int(med.qty)*int(med.perstrip)/int(med.rtime)
        #     med.save()
        data = {
            'title':"Update Med",
            'm':m,
            'msg':True,
        }
        return render(request,'addstock.html',data)
    else:
        data = {
            'title':"Update Med",
            'm':m,
        }
        return render(request,'addstock.html',data)
    return render(request,'addstock.html')

def meddetail(request,id):
    en = Meds.objects.get(id=id)
    em = Expiry.objects.all().filter(name=en)
    data ={
        'en':em,
        'id':id,
        'title':'Medicine Detail',
    }
    return render(request,'meddetail.html',data)

def deleteexp(request,id,rid):
    e = Expiry.objects.get(id=id)
    en = Meds.objects.get(id=rid)
    en.qty -= e.qty
    en.stkdays = int(en.qty)*int(en.perstrip)/int(en.rtime)
    en.save()
    e.delete()
    return redirect(f'/meddetail/{rid}')

def updatestock(request,id,rid):
    en = Expiry.objects.get(id=id)
    e = Meds.objects.get(id=rid)
    if request.method == "POST":
        qty = request.POST['qty']
        exp = request.POST['exp']
        if exp != "" : en.expiry = exp
        e.qty -= en.qty
        e.qty += int(qty)
        en.qty=qty
        en.save()
        e.stkdays = int(e.qty)*int(e.perstrip)/int(e.rtime)
        e.save()
        return redirect(f'/meddetail/{rid}', title="Medicine Detail")

    else:
        data={
            "title":'Update Stock',
            'en':en,
        }
        return render(request,'updatestock.html',data)
    
def deletemed(request):
    if request.method == "POST":
        id = request.POST['id']
        Meds.objects.get(id=id).delete()
        return redirect('/')
    else:
        m = Meds.objects.all()
        return render(request,'deletemed.html',{'m':m})

def countdown():
    en = Meds.objects.all()
    for i in en:
        i.stkdays = i.stkdays - i.rtime
