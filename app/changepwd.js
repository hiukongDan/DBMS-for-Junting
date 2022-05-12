langdata = {}


async function start(){
	var lang = document.getElementsByTagName("html")[0].getAttribute("lang");
	const response = await fetch("lang/"+lang+".json");
	langdata = await response.json();
	eel.changeLang(lang);
	
	const login = document.getElementById("login");
	login.setAttribute("href", "login-"+lang+".html");
	
	document.getElementById("submit").addEventListener("click", (event) =>{
		const name = document.getElementById("name").value;
		const password_old = document.getElementById("password_old").value;
		const password_new_1 = document.getElementById("password_new_1").value;
		const password_new_2 = document.getElementById("password_new_2").value;
		
		if(name === ""||password_old === ""||password_new_1 === ""||password_new_2 === ""){
			alert(langdata["loginnotvalid"]);
			return;
		}
		else if(password_new_1 != password_new_2){
			alert(langdata["pwdnosame"]);
			return;
		}
		eel.verifyUser(name, password_old)(function(success){
			if(success){
				eel.changePwd(name, password_new_1)(function(){
					alert(langdata["success"]);
					location.replace("login-"+lang+".html");
				});
			}
			else{
				alert(langdata["loginnotvalid"]);
			}
		});
	});
}

start();