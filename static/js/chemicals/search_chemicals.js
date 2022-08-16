
//====================================Cercare un prodotto chimico


const choiceProd = document.getElementById('div_id_id_chemical') //combo box con l'elenco dei prodotti chimici
const loadModalChemicals = document.getElementById('load-modal') //pulsante per carciare il modal di ricerca
const url = window.location.href + "data/"
const recentBox = document.getElementById('recent-box') //elenco degli ordini recenti
const chemList = document.getElementById('chem-list') //lista dei prodotti chimici
const searchChemical = document.getElementById('searchChemical') //input box nel modal per cercare il prodotto chimico
const loadBtn = document.getElementById('load-btn') //pulsante per caricare il modal di ricerca
const spinnerBox = document.getElementById('spinner-box')
const endBox = document.getElementById('end-box')


$('#SearchChemModal').on('shown.bs.modal', function () {
    $('#searchChemical').focus();
    
})  

prev = document.getElementById("previous_page");
    prev.value = document.referrer;

    $(function() {
    $('#chem-list').on('click', 'button', function(){
        var prova=$(this).attr('id');      
        let idChem=prova
        data={
            id_chemical: idChem
        }
        $('#id_id_chemical').val(data.id_chemical);
        getData()
        $('#SearchChemModal').modal('hide');
    });
});


const getData = () => {
    let idchem=document.querySelector('#id_id_chemical').value
    $.ajax({
        type: 'GET',        
        url: `/chemicals/data/${idchem}/`,
        
        
        success: function(response){
            const data = response.data
            console.log('You did it!!!')
            
            $(recentBox).empty()
            for (var i = 0; i < data.length; i++){
                var row = `
                <tr>  
                <td class="text-center"><a href="">${data[i].id_order}</a></td>
                <td class="text-center">${data[i].order_date}</td>
                <td class="text-center">${data[i].id_chemical}</td>
                <td class="text-center">${data[i].um}</td>
                <td class="text-center">${data[i].quantity}</td>
                <td class="text-center">${data[i].id_packaging_type}</td>
                </tr>  
                `
            recentBox.innerHTML+=row
        }},
        error: function(error){
        
        console.log(error)
        
        }
        
    })
}


choiceProd.addEventListener('change', ()=>{  
    getData()
})


let visible = 3
const getDataChemicals = () => {
    let idsup=document.getElementById('supplier').innerText  
    $(chemList).empty()
    $.ajax({
        type: 'GET',
        url: `/chemicals/chemlist/${idsup}/${visible}/`,
        success: function(response){            
            const data = response.data
            
            setTimeout(()=>{
                spinnerBox.hidden=true    
                data.forEach(el => {
                    
                    
                    chemList.innerHTML += `
                        <tr>  
                            <td class="text-center"><button type="button" class="btn btn-primary btn-sm" id="${el.pk_chem}">
                            <span class="bi bi-search"></span> 
                            </button></td>
                            <td class="text-center" >${el.id_chemical}</td>
                            <td class="text-center">${el.last_price}</td>
                            <td class="text-center">${el.cov}</td>                
                        </tr>  
                        `
                
                });
            }, 300)                    
            if (response.size === 0) {
                endBox.textContent = 'No posts added yet...'
            }
            else if (response.size <= visible) {
                //loadBtn.classList.add('not-visible')
                //loadBtn.hidden=true
                endBox.textContent = 'No more posts to load...'
            }
        },
        error: function(error){
            console.log(error)
        }
    })
}



loadBtn.addEventListener('click', ()=>{
    spinnerBox.hidden=false
    visible += 3    
    getDataChemicalsFiltered()
})




loadModalChemicals.addEventListener('click', ()=>{    
    searchChemical.value = ''
    $(chemList).empty()
    $(loadBtn).hidden=false
    endBox.textContent = ''
  //let idsup=document.getElementById('#supplier')
    getDataChemicalsFiltered()
})


const getDataChemicalsFiltered = () => {
    let idsup=document.getElementById('supplier').innerText      
    let searchTxt=$('#searchChemical').val() 
    if (searchTxt){
        url_var=`/chemicals/chemlist/${idsup}/${searchTxt}/${visible}/`
    } else {
        url_var=`/chemicals/chemlist/${idsup}/${visible}/`
    }
    $.ajax({
        type: 'GET',        
        url: url_var,
        
        
        success: function(response){
            const data = response.data
            if (searchTxt){
                $(chemList).empty()
            }            
            //
            spinnerBox.hidden=true
            for (var i = 0; i < data.length; i++){
                var row = `
                <tr>  
                <td class="text-center"><button type="button" class="btn btn-primary btn-sm" id="${data[i].pk_chem}">
                <span class="bi bi-search"></span> 
                </button></td>
                <td class="text-center" >${data[i].id_chemical}</td>
                <td class="text-center">${data[i].last_price}</td>
                <td class="text-center">${data[i].description}</td>                
                </tr>  
                `
            chemList.innerHTML+=row
        }
        if (response.size === 0) {
            endBox.textContent = 'Nessun prodotto ancora aggiunto...'
    }
    else if (response.size <= visible) {
        //loadBtn.classList.add('not-visible')
        //loadBtn.hidden=true
        endBox.textContent = 'Non ci sono altri prodotti da caricare...'
    }
    },
        error: function(error){
        
        console.log(error)
        
        }
        
    })
}

searchChemical.addEventListener('keyup', ()=>{  
    getDataChemicalsFiltered()
})


//====================================Fine ricerca prodotto chimico