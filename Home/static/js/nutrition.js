$('#product-select').hide();

$(document).ready(() => {
    const search_bar = $('#search_bar');
    const product_index = $("#product-index");
    const searched_product = $("#searched-product");
    const product_list = $('#product_list');
    const search_product = $('#search-product');
    const product_select = $('#product-select');
    
    search_bar.val("");
    search_bar.on('input', (e) => {
        product_select.hide();
        product_index.text(0);
        if (searched_product.length > 0)
            searched_product.remove();
        let formData = new FormData();
        formData.append("product", search_bar.val());
        $.ajax({
            url: "autocomplete",
            enctype: 'multipart/form-data',
            type: 'POST',
            processData: false,
            contentType: false,
            data: formData,
            success: (data) => {
                product_list.empty();
                if (data["products"].length == 0) {
                    search_product.show();
                    product_list.css('height', 0);
                } else {
                    product_list.css('height', 300);
                    search_product.hide();
                    const template = Handlebars.compile($("#product-template").html());
                    product_list.html(template(data)); 

                    document.querySelectorAll(".product").forEach(element => {
                        element.addEventListener("click", function(e) {
                            let nom = element.querySelector(".product-name").childNodes[1].textContent;
                            nom = nom.substring(1, nom.length - 1)
                            product_select.show();
                            $('#selected-product-name')[0].textContent = nom;
                            search_bar.val(nom);
                            product_list.hide();
                        });
                    });
                }
            },
            error: function(xhr) {
                if (xhr.status == 400) {
                    // handle the error here
                }
            }
        });
    });
});



function search_product (which = "current") {
    let formData = new FormData();
    formData.append('product', $('#search_bar').val());
    product_index = parseInt($("#product-index").text());
    formData.append('product-index',
        which === "next" ?                      product_index + 1 :
        which === "prev" && product_index > 0 ? product_index - 1 :
                                                product_index
    );
    $.ajax({
        url: "search_product",
        enctype: 'multipart/form-data',
        type: 'POST',
        processData: false,
        contentType: false,
        data: formData,
        success: (data) => {
            $("#searched-product").remove();
            const template = Handlebars.compile($("#searched-product-template").html());
            $("#product-container").html(template(data));
            $("#product-index").text(formData.get('product-index'));
        },
        error: function(xhr) {
            if (xhr.status == 400)
                ;
        }
    });
}


function add_product() {
    product_data = {"product": {}};
    nutrients = ["energy", "lipid", "carbohydrate", "sugar", "protein", "fiber", "water"];
    product_data['name'] = $(' #product-name').val();
    $.each(nutrients, function(_, nutrient) {
        product_data[nutrient] = $(".product-" + nutrient).text().match(/\d+(?:\.\d+)?/)[0];
    });
    let formData = new FormData(produc_data);
    $.ajax({
        url: "add_product_to_db",
        enctype: 'multipart/form-data',
        type: 'POST',
        processData: false,
        contentType: false,
        data: formData,
        success: (data) => {
            console.log("The product has been added");
        },
        error: function(xhr) {
            if (xhr.status == 400)
                ;
        }
    });
}


var addButton = document.getElementById('add');
var divSelect = document.getElementById('div_select');
var isShown = false;

addButton.addEventListener("click", function() {
  if (isShown) {
    divSelect.style.display = "none";
    isShown = false;
  } else {
    divSelect.style.display = "block";
    isShown = true;
  }
});

//Affichage de la div d'ajout
var add = document.getElementById('cancel');
add.addEventListener("click", (e) =>{
    document.getElementById("div_select").style.display="none";
    isShown = false;
});

//Affichage de la div d'ajout
var add = document.getElementById('save');
add.addEventListener("click", (e) => {
    let formData = new FormData();
    console.log($('#selected-product-category'))
    formData.append("period", $('#selected-product-period').val());
    formData.append("category", "MEAL");
    formData.append("name", $('#search_bar').val());
    formData.append("quantity", $('#selected-product-quantity').val());
    console.log(formData)
    $.ajax({
        url: "add_product_to_user",
        type: 'POST',
        processData: false,
        contentType: false,
        data: formData,
        // TODO: fix chart update
        success: (data) => {
            nex_chart.data.datasets[0].data.push(data);
            nex_chart.update();
        },
        error: function(xhr) {
            if (xhr.status == 400)
                ;
        }

    })
    // document.getElementById("div_select").style.display="none";
    // a modifier pour faire la sauvegarde dans la base de donné et mettre à jour le graph
});

//Création du graphique du résumé des calories
const myChart = document.getElementById("my_chart");

// début du code pour écrire le pourcentage au milieu du graphique si nécessaire
//const counter = {
    //id: 'counter',
    //beforeDraw(chart, args, options);
//}

const color = ['rgb( 255, 105, 180)', 'rgb( 255, 215, 0)', 'rgb( 144, 238, 144)', 'rgb(100, 149, 237)', 'rgb(255, 127, 80)', 'rgb(230, 233, 236)']

const chartData = {
    labels : ["Petit-déjeuner", "Collation matinale", "Déjeuner", "Goûter", "Diner", "A consommer"],
    datasets : [{
        label: '% des calories de la journée',
        data : [
            parseFloat($("#calories-breakfast").text()),
            parseFloat($("#calories-morning-snack").text()),
            parseFloat($("#calories-lunch").text()),
            parseFloat($("#calories-snack").text()),
            parseFloat($("#calories-dinner").text()),
            parseFloat($("#calories-to-consume").text())
        ],
        backgroundColor:[
            color[0],
            color[1],
            color[2],
            color[3],
            color[4],
            color[5]
        ],
        borderColor : [
            'rgb(255, 255, 255)'
        ]
    }]
};

const config = {
    type: "doughnut",
    data : chartData,
    options: {
        plugins: {
            tooltip: {
                callbacks: {
                    label: (context) => {
                        return `${context.parsed}% des calories de la journée`;
                    }
                }
            }
        }
    },
    //plugins : [counter]
};

const nex_chart = new Chart(
    myChart,
    config
);


// console.log($('#cancel')[0]);
// $('#cancel').addEventListener("click", function(e){
//     // $('#div_select').style.display = "none";
//     console.log('test');
// });
// function Enregistrer_produit(){
//     const nDiv = document.createElement("div");
//     console.log("ajout");
//     nDiv.classList.add("row");
//     document.div_precedente.appendChild(nDiv);
// }