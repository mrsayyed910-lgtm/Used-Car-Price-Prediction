// ===============================
// Data from Flask
// ===============================
const brandModel = window.brandModel || {};
const brandModelDetails = window.brandModelDetails || {};

// ===============================
// Brand Logos
// ===============================
const logos = {
    "Audi":"audi.png",
    "BMW":"bmw.png",
    "Bentley":"bentley.png",
    "Datsun":"datsun.png",
    "Ferrari":"ferrari.png",
    "Force":"force.png",
    "Ford":"ford.png",
    "Honda":"honda.png",
    "Hyundai":"hyundai.png",
    "ISUZU":"isuzu.png",
    "Isuzu":"isuzu.png",
    "Jaguar":"jaguar.png",
    "Jeep":"jeep.png",
    "Kia":"kia.png",
    "Land Rover":"landrover.png",
    "Lexus":"lexus.png",
    "MG":"mg.png",
    "Mahindra":"mahindra.png",
    "Maruti":"maruti.png",
    "Maserati":"maserati.png",
    "Mercedes-AMG":"mercedes.png",
    "Mercedes-Benz":"mercedes.png",
    "Mini":"mini.png",
    "Nissan":"nissan.png",
    "Porsche":"porsche.png",
    "Renault":"renault.png",
    "Rolls-Royce":"rollsroyce.png",
    "Skoda":"skoda.png",
    "Tata":"tata.png",
    "Toyota":"toyota.png",
    "Volkswagen":"volkswagen.png",
    "Volvo":"volvo.png"
};

// ===============================
// Car Images
// ===============================
const carImages = {
    "Swift":"swift.jpg",
    "Baleno":"baleno.jpg",
    "Alto":"alto.jpg",
    "Creta":"creta.jpg",
    "i20":"i20.jpg",
    "Verna":"verna.jpg",
    "City":"city.jpg",
    "Amaze":"amaze.jpg",
    "Nexon":"nexon.jpg",
    "Harrier":"harrier.jpg",
    "XUV700":"xuv700.jpg",
    "Scorpio":"scorpio.jpg",
    "Fortuner":"fortuner.jpg",
    "Innova":"innova.jpg"
};

// ===============================
// Brand -> Model
// ===============================
function updateModels(){

    const brand=document.getElementById("brand").value;
    const model=document.getElementById("model");

    model.innerHTML='<option value="">Select Model</option>';

    if(brandModel[brand]){

        brandModel[brand].forEach(function(item){

            let option=document.createElement("option");
            option.value=item;
            option.text=item;

            model.appendChild(option);

        });

    }

    updateLogo();
}

// ===============================
// Auto Fill Details
// ===============================
function updateCarDetails(){

    const brand=document.getElementById("brand").value;
    const model=document.getElementById("model").value;

    if(
        brandModelDetails[brand] &&
        brandModelDetails[brand][model]
    ){

        const details=brandModelDetails[brand][model];

        document.querySelector("input[name='engine']").value=details.engine;
        document.querySelector("input[name='max_power']").value=details.max_power;
        document.querySelector("input[name='mileage']").value=details.mileage;
        document.querySelector("input[name='seats']").value=details.seats;

    }

}

// ===============================
// Vehicle Age
// ===============================
function calculateVehicleAge(){

    const year=document.getElementById("registration_year").value;

    if(year){

        const currentYear=new Date().getFullYear();

        document.getElementById("vehicle_age").value=currentYear-year;

    }

}

// ===============================
// Brand Logo
// ===============================
function updateLogo(){

    const brand=document.getElementById("brand").value;
    const img=document.getElementById("brandLogo");

    if(logos[brand]){

        img.src="/static/images/brands/"+logos[brand];

    }
    else{

        img.src="/static/images/brands/default.png";

    }

}

// ===============================
// Car Image
// ===============================
function updateCarImage(){

    const model=document.getElementById("model").value;
    const img=document.getElementById("carImage");

    if(carImages[model]){

        img.src="/static/images/cars/"+carImages[model];

    }
    else{

        img.src="/static/images/cars/default.jpg";

    }

}

// ===============================
// Dark Mode
// ===============================
const btn=document.getElementById("themeButton");

if(btn){

    btn.onclick=function(){

        document.body.classList.toggle("dark-mode");

        if(document.body.classList.contains("dark-mode")){

            btn.innerHTML="☀️ Light Mode";

        }
        else{

            btn.innerHTML="🌙 Dark Mode";

        }

    }

}

// ===============================
// Loading Button
// ===============================
const form=document.querySelector("form");

if(form){

    form.addEventListener("submit",function(){

        const button=document.querySelector(".predict-btn");

        button.innerHTML="⏳ Predicting...";
        button.disabled=true;

    });

}