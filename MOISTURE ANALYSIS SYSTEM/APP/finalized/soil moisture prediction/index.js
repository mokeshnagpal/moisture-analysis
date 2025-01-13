import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.6.0/firebase-app.js'
import { getDatabase,ref,onValue,set } from 'https://www.gstatic.com/firebasejs/10.6.0/firebase-database.js'

const appSettings = {
  databaseURL: "https://soil-moisture-analysis-default-rtdb.asia-southeast1.firebasedatabase.app/",
};

const app = initializeApp(appSettings);
const database = getDatabase(app)

const change_ref = ref(database, "change");
const plant_type_ref = ref(database,"plant_type")
const ph_ref = ref(database,"ph");
const soil_ec_ref = ref(database,"soil_ec");
const phosphorus_ref = ref(database,"phosphorus");
const potassium_ref = ref(database,"potassium");
const tsp_ref = ref(database,"tsp");
const mop_ref = ref(database,"mop");
const urea_ref = ref(database,"urea");
const override_ref = ref(database,"override");
const moisture_value_ref = ref(database,"moisture_value");

const plant_type_html = document.getElementById("plant_type");
const ph_html = document.getElementById("ph");
const soil_ec_html = document.getElementById("soil_ec");
const phosphorus_html = document.getElementById("phosphorus");
const potassium_html = document.getElementById("potassium");
const tsp_html = document.getElementById("tsp");
const mop_html = document.getElementById("mop");
const urea_html = document.getElementById("urea");
const moisture_value_html = document.getElementById("moisture_value");
const override_html = document.getElementById("override");

plant_type_html.addEventListener("input", handleInputChange);
ph_html.addEventListener("input", handleInputChange);
soil_ec_html.addEventListener("input", handleInputChange);
phosphorus_html.addEventListener("input", handleInputChange);
potassium_html.addEventListener("input", handleInputChange);
tsp_html.addEventListener("input", handleInputChange);
mop_html.addEventListener("input", handleInputChange);
urea_html.addEventListener("input", handleInputChange);
override_html.addEventListener("click", override_func);


onValue(moisture_value_ref,function(moisture_value)   //used for initialization
{
    moisture_value = moisture_value.val();
    moisture_value_html.value =  moisture_value;
})
onValue(plant_type_ref, function(plant_type) {
    plant_type = plant_type.val();
    plant_type_html.value = plant_type;
});
onValue(ph_ref,function(ph)   //used for initialization
{
    ph = ph.val();
    ph_html.value =  ph;
})
onValue(soil_ec_ref,function(soil_ec)   //used for initialization
{
    soil_ec = soil_ec.val();
    soil_ec_html.value =  soil_ec;
})
onValue(phosphorus_ref,function(phosphorus)   //used for initialization
{
    phosphorus = phosphorus.val();
    phosphorus_html.value =  phosphorus;
})
onValue(potassium_ref,function(potassium)   //used for initialization
{
    potassium = potassium.val();
    potassium_html.value =  potassium;
})
onValue(tsp_ref,function(tsp)   //used for initialization
{
    tsp = tsp.val();
    tsp_html.value =  tsp;
})
onValue(mop_ref,function(mop)   //used for initialization
{
    mop = mop.val();
    mop_html.value =  mop;
})
onValue(urea_ref,function(urea)   //used for initialization
{
    urea = urea.val();
    urea_html.value =  urea;
})
onValue(override_ref,function(override)   //used for initialization
{
    override = override.val();
    override_html.value =  override;
    if(override == 1) {
        document.getElementById("override").innerText = "Turn Off";
    }
    else {
        document.getElementById("override").innerText = "Override";
    }
})
function handleInputChange() {
    var ph_val=parseFloat(ph_html.value);
    var soil_ec_val=parseFloat(soil_ec_html.value);
    var potassium_val=parseFloat(potassium_html.value);   
    var urea_val=parseFloat(urea_html.value);
    var mop_val=parseFloat(mop_html.value);
    var tsp_val=parseFloat(tsp_html.value);    
    var phosphorus_val=parseFloat(phosphorus_html.value);
    var plant_type_val=parseInt(plant_type_html.value);
    
    set(change_ref, 1);
    set(plant_type_ref, plant_type_val);
    set(ph_ref, ph_val);
    set(urea_ref, urea_val);
    set(phosphorus_ref, phosphorus_val);
    set(potassium_ref, potassium_val);
    set(soil_ec_ref, soil_ec_val);
    set(tsp_ref, tsp_val);
    set(mop_ref, mop_val);
}

function override_func() {
    if(document.getElementById("override").innerText == "Override"){
        document.getElementById("override").innerText = "Turn Off";
        set(override_ref, 1); 
    } 
    else if(document.getElementById("override").innerText == "Turn Off"){
        document.getElementById("override").innerText = "Override";
        set(override_ref, 0);
    } 
}


