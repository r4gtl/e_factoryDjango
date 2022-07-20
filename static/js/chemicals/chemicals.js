

//====================================Cercare un fornitore
$('#SearchSupplierModal').on('shown.bs.modal', function () {
    $('#searchSupplier').focus();
})  

$(function() {
$('#supplier-list').on('click', 'button', function(){
    var idbutton=$(this).attr('id');
    let idSupplier=idbutton
    data={
    id_supplier: idSupplier
    }      
    $('#id_id_supplier').val(data.id_supplier);      
    $('#SearchSupplierModal').modal('hide');
});
});


const suppList = document.getElementById('supplier-list')
const searchSupplier = document.getElementById('searchSupplier')
const loadModal = document.getElementById('load-modal')



const getDataSuppliers = () => {    
let searchTxt=$('#searchSupplier').val() 
if (searchTxt){
    url_var=`/chemicals/supplier_list/${searchTxt}/`
} else {
    url_var=`/chemicals/supplier_list/`
}

$.ajax({
    type: 'GET',        
    url: url_var,        
    success: function(response){

        const data = response.data            
        $(suppList).empty()
        for (var i = 0; i < data.length; i++){
            var row = `
            <tr>  
            <td class="text-center"><button type="button" class="btn btn-primary btn-sm" id="${data[i].id_supplier}">
            <span class="bi bi-search"></span> 
            </button></td>
            <td class="text-start" >${data[i].company_name}</td>                
            </tr>  
            `
            suppList.innerHTML+=row
    }},
    error: function(error){
    
    console.log(error)
    
    }
    
})
}

loadModal.addEventListener('click', ()=>{
$('#searchSupplier').val("")
getDataSuppliers()
})


searchSupplier.addEventListener('keyup', ()=>{  
getDataSuppliers()
})


getDataSuppliers()

//====================================Fine ricerca fornitore
