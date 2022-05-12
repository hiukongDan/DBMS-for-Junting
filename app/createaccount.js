langdata = {}



async function start(){
	var lang = document.getElementsByTagName("html")[0].getAttribute("lang");
	const response = await fetch("lang/"+lang+".json");
	langdata = await response.json();
	eel.changeLang(lang);
	
	document.getElementById("login").setAttribute("href", "./login-"+lang+".html");

	document.getElementById("create").addEventListener("click", (event) =>{
		
		const name = document.getElementById("name").value;
		const password_1 = document.getElementById("password_1").value;
		const password_2 = document.getElementById("password_2").value;

		if(name === "" || password_1 === ""){
			alert(langdata["loginnotvalid"]);
			return;
		}
		else if(password_1 != password_2){
			alert(langdata["pwdnosame"]);
			return;
		}
		
		eel.addUser(name, password_1)(function(success){
			if(success){
				location.replace("login-"+lang+".html");
			}
			else{
				alert(langdata["loginnotvalid"]);
				return;
			}
		});
	});
}

start();
	