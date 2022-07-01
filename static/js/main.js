
  
const date = new Date();
document.querySelector('.year').innerHTML = date.getFullYear();

$('select').selectpicker();



const loadBtn = document.getElementById('load-btn')

const loadIdChem = document.getElementById('id_id_chemical')

let idchem=loadIdChem.val();
console.log('Hello World')
console.log(idchem)

const getData = () => {
    $.ajax({
        type: 'GET',
        url: `/data/${idchem}/`,
        success: function(response){
            console.log('Hello World')
            console.log(response)
        }
        
    })
}


loadBtn.addEventListener('click', ()=>{
    
    let idchem=loadIdChem.val();
    console.log('Hello World')
    console.log(idchem)
    getData()
})


getData()



