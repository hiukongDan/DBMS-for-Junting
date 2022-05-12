langdata = {}



async function start(){
	var lang = document.getElementsByTagName("html")[0].getAttribute("lang");
	const response = await fetch("lang/"+lang+".json");
	langdata = await response.json();
	eel.changeLang(lang);
	
	document.getElementById("changepwd").setAttribute("href", "./changepwd-"+lang+".html");
	document.getElementById("createaccount").setAttribute("href", "./createaccount-"+lang+".html");
	
	document.getElementById("login").addEventListener("click", (event) =>{
		
		const name = document.getElementById("name").value;
		const password = document.getElementById("password").value;

		if(name === "" || password === ""){
			alert(langdata["loginnotvalid"]);
			return;
		}
		eel.verifyUser(name, password)(function(success){
			if(success){
				location.replace("index-"+lang+".html");
			}
			else{
				alert(langdata["loginnotvalid"]);
				return;
			}
		});
	});
}

start();