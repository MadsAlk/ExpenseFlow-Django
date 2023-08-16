const usernameField = document.querySelector("#usernameField");
const feedBackArea=document.querySelector('.invalid_feedback');
const emailField = document.querySelector("#emailField");
const emailArea=document.querySelector('.invalid_email');
const usernameSuccessOutput=document.querySelector('.usernameSuccessOutput');
const emailSuccessOutput=document.querySelector('.emailSuccessOutput');
const passwordToggle=document.querySelector('.passwordToggle');
const passwordField = document.querySelector("#passwordField");
const submitBtn=document.querySelector('.submitBtn');

username_valid = false;
email_valid = false;
submitBtn.disabled = true;


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



usernameField.addEventListener("keyup", (e)=> { 
  const usernameVal = e.target.value;
  console.log('val:', usernameVal);

  usernameField.classList.remove("is-invalid");
  feedBackArea.style.display='none';
  usernameSuccessOutput.style.display='block';
  usernameSuccessOutput.textContent=`Checking ${usernameVal}`;

  if(usernameVal.length > 0){
    fetch("/authentication/validate-username", {
      body: JSON.stringify({username: usernameVal }),
      method: "POST"
    })
    .then((res) => res.json())
    .then((data) => {
      usernameSuccessOutput.style.display='none';
      console.log("data", data);
      if (data.username_error){
        submitBtn.disabled = true;
        usernameField.classList.add("is-invalid");
        feedBackArea.style.display='block';
        feedBackArea.innerHTML = `<p>${data.username_error}</p>`
      }else{
        username_valid = true;
        if(email_valid == true){
          submitBtn.disabled = false;
        }
      }
    });
  }

});


emailField.addEventListener("keyup", (e)=> { 
  const emailVal = e.target.value;
  console.log('emailval:', emailVal);

  emailField.classList.remove("is-invalid");
  emailArea.style.display='none';
  emailSuccessOutput.style.display='block';
  emailSuccessOutput.textContent=`Checking ${emailVal}`;

  if(emailVal.length > 0){
    fetch("/authentication/validate-email", {
      body: JSON.stringify({email: emailVal }),
      method: "POST"
    })
    .then((res) => res.json())
    .then((data) => {
      emailSuccessOutput.style.display='none';
      console.log("data", data);
      if (data.email_error){
        submitBtn.disabled = true;
        emailField.classList.add("is-invalid");
        emailArea.style.display='block';
        emailArea.innerHTML = `<p>${data.email_error}</p>`
      }else{
        email_valid = true;
        if(username_valid == true){
          submitBtn.disabled = false;
        }
      }
    });
  }

});