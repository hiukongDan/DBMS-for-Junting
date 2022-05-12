var langdata = {};

const dataTypes = [
   "stockin", 
   "soldout", 
   "items",
   "stocks"
];

const colorconfig = {
	"tab-select": "#bb9311",
	"tab-normal": "#306b7b"
};

const tableheader = {
	"items": ["item",],
	"stocks": ["item", "count"],
	"stockin": ["item", "count", "date"],
	"soldout": ["item", "count", "date", "name", "contact"]
};

const inputtypes = {
	"items": {"item": "text"},
	"stockin": {"item": "select", "count": "number", "date": "date"},
	"soldout": {"item": "select", "count": "number", "date": "date", "name": "text", "contact": "tel"}
};

const btns = {};
dataTypes.forEach((element, index) => {
	btns[element] = document.querySelector(".navigation #"+element);
});

const tabs = {};
dataTypes.forEach((element, index) => {
	tabs[element] = document.querySelector(".table #"+element);
})


for (const [key, value] of Object.entries(btns)){
	value.addEventListener("click", function(){
		tabClearall();
		tabShow(key);
	});
}

async function loadLangData(){
	var lang = document.getElementsByTagName("html")[0].getAttribute("lang");
	const response = await fetch("lang/"+lang+".json");
	langdata = await response.json();
	
	dataTypes.forEach((element, index) =>{
		btns[element].textContent = langdata[element];
	});
	
	eel.changeLang(lang);
}


async function start(){
	await loadLangData();
	await tabShow("stocks");
}

async function tabClearall(){
	for ([key, value] of Object.entries(tabs)){
		var t = value.getElementsByTagName("table")[0];
		if(t){
			value.removeChild(t);
		}
		var table = document.createElement("table");
		table.textContent = "";
		btns[key].style.backgroundColor = colorconfig["tab-normal"];
		value.appendChild(table);
	}
}

async function tabShow(tabName){
	await tabClearall();
	btns[tabName].style.backgroundColor = colorconfig["tab-select"];
	eel.getData(tabName)(function(data){
		// console.log(data)
		var tab = tabs[tabName].getElementsByTagName("table")[0];
		
		// functional buttons
		var tr = document.createElement("tr");
		tab.appendChild(tr);
		buildButton(tr, langdata["saveall"]).addEventListener("click", function(){
			eel.saveAll()(function(){
				alert(langdata["done"]);
			});
		});
		buildButton(tr, langdata["savetoexcel"]).addEventListener("click", function(){
			eel.saveToExcel()(function(){
				alert(langdata["done"]);
			});
		});
		buildButton(tr, langdata["logout"]).addEventListener("click", function(){
			eel.saveAll()(function(){
				var lang = document.getElementsByTagName("html")[0].getAttribute("lang");
				location.replace("login-"+lang+".html");
			});
		});
		
		
		
		
		// table header
		var header = document.createElement("tr");
		tab.appendChild(header);
		tableheader[tabName].forEach((element, index) => {
			var td = document.createElement("td");
			header.appendChild(td);
			td.textContent = langdata[element].toUpperCase();
			td.setAttribute("class", "table-header");
		});
		
		var tbody = document.createElement("tbody");
		tab.appendChild(tbody);
		
		// input field
		if(tabName != "stocks"){
			const inputs = [];
			var itemSelect = null;
			
			header = document.createElement("tr");
			tbody.appendChild(header);
			tableheader[tabName].forEach((element, index) =>{
				if(element === "item" && inputtypes[tabName]["item"] === "select"){
					itemSelect = buildSelections(header);
				}
				else{
					var td = document.createElement("td");
					header.appendChild(td);
					td.setAttribute("class", "input");
					var input = document.createElement("input");
					input.setAttribute("type", inputtypes[tabName][element]);
					input.setAttribute("id", element);
					td.appendChild(input);
					
					inputs.push(input);
				}
			});
			
			
			// submit button
			var td = document.createElement("td");
			header.appendChild(td);
			td.setAttribute("class", "input");
			const submit = document.createElement("input");
			submit.setAttribute("type", "submit");
			submit.setAttribute("value", langdata["add"]);
			submit.setAttribute("id", "submit");
			td.appendChild(submit);
			
			submit.addEventListener("click",  (event) =>{
				var senddata = {};
				var isValid = true;
				if(itemSelect){
					if(itemSelect.options.length > 0){
						senddata["item"] = itemSelect.options[itemSelect.selectedIndex].value;
					}
					else{
						isValid = false;
					}
				}
				
				inputs.forEach((input) => {
					if(input.value == ""){
						isValid = false;
					}
					senddata[input.getAttribute("id")] = 
						input.getAttribute("id") == "count" ? parseInt(input.value) : input.value;
				});
				
				if(!isValid){
					alert(langdata["inputinvalid"]);
				}
				else{
					eel.insertEntry(tabName, senddata)(function(){
						tabShow(tabName);
					});					
				}
				
			});
		}

		
		// table entries
		data.forEach((entry, index) => {
			var tr = document.createElement("tr");
			tbody.appendChild(tr);
			tableheader[tabName].forEach((element, index) => {
				var td = document.createElement("td");
				tr.appendChild(td);
				td.textContent = entry[element];
			});
			
			if(tabName != "stocks"){
				// Add a delete button for each entry
				var btn = document.createElement("input");
				var td = document.createElement("td");
				tr.appendChild(td);
				td.appendChild(btn);
				td.setAttribute("class", "input");
				btn.setAttribute("type", "submit");
				btn.setAttribute("value", langdata["delete"]);
				
				btn.addEventListener("click", function(){
					eel.deleteEntry(tabName, index)(function(){
						tabShow(tabName);
					});
				});
			}
		});
		

	});
}


function buildButton(tr, value){
	var td = document.createElement("td");
	tr.appendChild(td);
	td.setAttribute("class", "input");
	
	var btn = document.createElement("input");
	btn.setAttribute("type", "submit");
	btn.setAttribute("value", value);
	td.appendChild(btn);
	
	return btn;
}

function buildSelections(tr){
	var td = document.createElement("td");
	td.setAttribute("class", "input");
	tr.appendChild(td);
	
	var sel = document.createElement("select");
	sel.setAttribute("id", "item");
	td.appendChild(sel);
	
	eel.getData("items")(function(data){
		data.forEach((element, index) =>{
			var op = document.createElement("option");
			op.setAttribute("value", element["item"]);
			op.textContent = element["item"];
			sel.appendChild(op);
		});
	});
	return sel;
}



start();