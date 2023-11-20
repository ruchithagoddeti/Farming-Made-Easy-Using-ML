from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
			path("AdminLogin.html", views.AdminLogin, name="AdminLogin"),
			path("AdminLoginAction", views.AdminLoginAction, name="AdminLoginAction"),
			path("FarmerLogin.html", views.FarmerLogin, name="FarmerLogin"),
			path("FarmerLoginAction", views.FarmerLoginAction, name="FarmerLoginAction"),
			path("Signup.html", views.Signup, name="Signup"),
			path("SignupAction", views.SignupAction, name="SignupAction"),	    	
			path("AddScheme.html", views.AddScheme, name="AddScheme"),
			path("AddSchemeAction", views.AddSchemeAction, name="AddSchemeAction"),	 
			path("PredictCropPrices.html", views.PredictCropPrices, name="PredictCropPrices"),
			path("PredictCropPricesAction", views.PredictCropPricesAction, name="PredictCropPricesAction"),	 
			path("ViewSchemes", views.ViewSchemes, name="ViewSchemes"),	 
]