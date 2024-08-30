#MongoDB
from pymongo import MongoClient

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Agro

#MongoDB server client conection
client = MongoClient("mongodb+srv://AgroMerc:AgroMerc2023@cluster0.5elomeg.mongodb.net")

#Database
db = client["AgroMerc"]

#Collections
colClients=db['Clientes']
colProducts = db['Productos']
colPurchases = db['Compras']

# User
userOnline = {}


# Create your views here.

def signIn(request):
    exist=False
    correctPassword=False
    trySignIn=False
    inSignIn=False
    if request.method == 'POST':
        trySignIn=True
        userName=str(request.POST['userName'])
        password=str(request.POST['password'])
        # verify if user exist and the password is correct
        for users in colClients.find():
            if (userName==users['userName'] or userName == users['email']):
                exist=True
                #verify password
                if(password == users['password']):
                    #sign In succesfully
                    correctPassword=True
                    inSignIn=True
                    userActive(users)
                    break
    context={"existAccount":exist, "correctPassword":correctPassword,
             "inSignIn":inSignIn,"trySignIn":trySignIn}
    return render(request,'signIn.html',context)
        
                
def signUp(request):
    #boolean data
    existCedula=False
    existEmail=False
    existUserName=False
    registered=False
    textUserName=""
    textCedula=""
    textEmail=""
    if request.method == 'POST':
        name=str(request.POST['name'])
        surnames=str(request.POST['surnames'])
        cedula=str(request.POST['cedula'])
        phoneNumber=str(request.POST['phoneNumber'])
        email=str(request.POST['email'])
        userName=str(request.POST['userName'])
        password=str(request.POST['password'])
        userType=str(request.POST.get('userType'))
        for client in colClients.find():
            if client['userName'] == userName:
                existUserName=True
            if client['cedula'] == cedula:
                existCedula=True
            if client['email'] == email:
                existEmail=True
        if(not existUserName and not existCedula and not existEmail):
            registered = True
            #save data in database
            data={"name":name,"surnames":surnames,"cedula":cedula,
                   "phoneNumber":phoneNumber,"email":email,
                   "userName":userName,"password":password,
                   "userType":userType}
            colClients.insert_one(data)
        if(existUserName):
            textUserName="El usuario "+userName+ " ya existe, intente uno diferente"
        if(existCedula):
            textCedula="La cédula ya se encuentra registrada"
        if(existEmail):
            textEmail="El correo electrónico "+email+" ya se encuentra registrado"
    context={"textUsername":textUserName,"textCedula":textCedula,"textEmail":textEmail,
                 "existUserName":existUserName,"existCedula":existCedula,"existEmail":existEmail,
                 "registered":registered}
    return render(request,'signUp.html',context)

def agroMerc(request):
    return render(request,'AgroMerc.html')

def mainMenu(request):
    global userOnline
    user=userOnline
    productsListName = []
    seller = False
    #verify if is seller
    if user['userType'] == 'seller':
        seller = True
    #look for products list
    for product in colProducts.find():
        #add product at list to be shown
        productsListName.append(product)
    context={"name":user['name'],'surnames':user['surnames'],
             "cedula":user['cedula'],"phoneNumber":user['phoneNumber'],
             "email":user['email'],"userName":user['userName'],
             "password":user['password'],"seller":seller,
             "productsListName":productsListName}
    return render(request,'mainMenu.html',context)

def purchase(request):
    purchaseMade=False
    global userOnline
    user=userOnline
    if request.method=='POST':
        for key, value in request.POST.items():
            if key.startswith('quantityOrdered_'):
                values=key.split('_')
                print(key,value)
                product=searchProduct(values[1],values[4])
                seller=searchSeller(str(values[1]))
                try:
                    quantityOrdered = int(value)
                    context={"buyed":purchaseMade,"product":product,
                         "quantityOrdered":quantityOrdered,"user":user,"seller":seller}
                    return render(request,'purchase.html',context)
                except ValueError:
                    print(type(value),value)
                    print("Value Error")
                    return redirect('mainMenu')
    
    context={"purchaseMade":purchaseMade}
    return render(request,'purchase.html',context)

def madeAPurchase(request):
    global userOnline
    user=userOnline
    purchaseMade=False
    purchaseCancel=False
    if request.method=='POST':
        for key, value in request.POST.items():
            print(value)
            if key.startswith('purchaseMade_'):
                purchaseMade=True
                values=key.split('_')
                quantityOrdered=int(values[1])
                product=searchProduct(values[3],values[2])
                seller=searchSeller(values[3])
                data={"seller":seller['name'],"sellerCedula":product['id'],"productName":product['name']+" "+product['specificName'],"id2Product":product['id2'],"buyer":user['name']+" "+user['surnames'],"quantitySold":quantityOrdered}
                possiblePurchase(product['id2'],str(int(product['maxQuantity'])-quantityOrdered),seller['cedula'])
                addPurchase(data)
            else:
                purchaseCancel=True
    context={"purchaseMade":purchaseMade,"purchaseCancel":purchaseCancel}             
    return render(request,'purchaseMade.html',context)
    
def home(request):
    search_term = request.GET.get('searchProduct', '')
    category_filter = request.GET.get('category', 'Todos')

    if category_filter == 'Todos':
        agros = Agro.objects.filter(title__icontains=search_term)
    else:
        agros = Agro.objects.filter(title__icontains=search_term, category=category_filter)

    categories = Agro.objects.values_list('category', flat=True).distinct()
    categories = ['Todos'] + list(categories)  # Add "Todos" to the list of categories

    context = {
        'searchTerm': search_term,
        'agros': agros,
        'categories': categories,
        'selected_category': category_filter,
    }
    return render(request, 'home.html', context)
def about(request):
    #return HttpResponse('<h1>Welcome to About page</h1>')
    return render(request, 'about.html')

def AddProducts(request):
    if request.method == 'POST':
        product_name = request.POST.get('productName')
        specific_name = request.POST.get('specificName')
        unit = request.POST.get('unit')
        max_quantity = request.POST.get('maxQuantity')
        min_quantity = request.POST.get('minQuiantity')

        # Verifica si se recibieron todos los campos necesarios
        if all([product_name, specific_name, unit, max_quantity, min_quantity]):
            # Crea un nuevo documento para el producto
            product_data = {
                "productName": product_name,
                "specificName": specific_name,
                "unit": unit,
                "maxQuantity": max_quantity,
                "minQuantity": min_quantity
            }
            
            # Inserta el producto en la colección de productos
            colProducts.insert_one(product_data)
            
            # Redirige o muestra un mensaje de éxito
            context = {'message': 'Producto agregado exitosamente'}
        else:
            # Muestra un mensaje de error si faltan datos
            context = {'message': 'Faltan datos para agregar el producto'}
        
        return render(request, 'AddProducts.html', context)
    
    return render(request, 'AddProducts.html')
