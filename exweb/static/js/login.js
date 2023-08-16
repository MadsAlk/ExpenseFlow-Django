const passwordToggle=document.querySelector('.passwordToggle');
const passwordField = document.querySelector("#passwordField");
const submitBtn=document.querySelector('.submitBtn');


const toggleFunction=(e)=>{
  if(passwordToggle.textContent==='SHOW'){
    passwordToggle.textContent = 'HIDE';
    passwordField.setAttribute('type', 'text');
  }else{
    passwordToggle.textContent = 'SHOW';
    passwordField.setAttribute('type', 'password');
  }
};
passwordToggle.addEventListener('click', toggleFunction);