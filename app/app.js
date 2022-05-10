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
		
		// table header
		var header = document.createElement("tr");
		tab.appendChild(header);
		tableheader[tabName].forEach((element, index) => {
			var td = document.createElement("td");
			header.appendChild(td);
			td.textContent = langdata[element].toUpperCase();
			td.setAttribute("class", "table-header");
		});
		
		// table entries
		var tbody = document.createElement("tbody");
		tab.appendChild(tbody);
		data.forEach((entry, index) => {
			var tr = document.createElement("tr");
			tbody.appendChild(tr);
			tableheader[tabName].forEach((element, index) => {
				var td = document.createElement("td");
				tr.appendChild(td);
				td.textContent = entry[element];
			});
		});
	});
}



start();