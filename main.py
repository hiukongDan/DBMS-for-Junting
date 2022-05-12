import eel, json, os, datetime, winreg, openpyxl


dataTypes = [
   "stockin", 
   "soldout", 
   "items",
   "stocks"
]

sheetheader = {
	"items": ["item",],
	"stocks": ["item", "count"],
	"stockin": ["item", "count", "date"],
	"soldout": ["item", "count", "date", "name", "contact"]
};


class RuntimeDatabase:
    def __init__(self):
        self.datapath = "./app/data/data.json"
        self.recoverdatapath = "./app/data/.data.json_recover"
        
        # load data
        if(os.path.exists(self.datapath)):
            with open(self.datapath, "r", encoding="utf8") as f:
                self.data = json.load(f);
        else:
            with open(self.datapath, 'w', encoding="utf8") as f:
                pass
            self.data = {"items":[], "stocks":[], "stockin":[], "soldout":[]}
        
        # save a recover data for this session
        self.savetofile(self.recoverdatapath)
            
            
    def savetofile(self, filename):
        with open(filename, "w") as f:
            json.dump(self.data, f);
        
        
    def save(self):
        self.savetofile(self.datapath)
        

class LangData:
    def __init__(self, lang):
        self.changelang(lang)
            
            
    def changelang(self, lang):
        self.lang = lang
        with open("./app/lang/"+lang+".json", "r", encoding="utf8") as f:
            self.data = json.load(f)
        
        
        
eel.init("app")

@eel.expose
def getData(dataType):
    return Database.data[dataType]
    
    
@eel.expose
def insertEntry(dataType, newEntry):
    # Primary key, unique
    if dataType == "items":
        if newEntry in Database.data[dataType]:
            return
        else:
            Database.data["stocks"].append({**newEntry, "count": 0})
    Database.data[dataType].append(newEntry)
    print("add new entry {} to {}".format(newEntry, dataType))
    calculateStocks()


@eel.expose
def deleteEntry(dataType, index):
    # Primary key
    if(dataType == "items"):
        for type in ["stockin", "soldout", "stocks"]:
            deleteEntries(type, {"item": Database.data[dataType][index]["item"]})
    print("delete {} from {}".format(Database.data[dataType][index], dataType))
    del Database.data[dataType][index]
    calculateStocks()
      

@eel.expose
def changeLang(lang):
    langdata.changelang(lang)
    print("Language changed to "+lang)
      
        
def deleteEntries(dataType, entry):
    for i in Database.data[dataType]:
        remove = True
        for k,v in entry.items():
            if i[k] != v:
                remove = False
                break
        if remove:
            print("delete {} from {}".format(i, dataType))
            Database.data[dataType].remove(i)



def calculateStocks():
    itemmap = {}
    i = 0
    for data in Database.data["stocks"]:
        data["count"] = 0
        itemmap[data["item"]] = i
        i += 1
        
    for data in Database.data["stockin"]:
        i = itemmap[data["item"]]
        Database.data["stocks"][i]["count"] += int(data["count"])
        
    for data in Database.data["soldout"]:
        i = itemmap[data["item"]];
        Database.data["stocks"][i]["count"] -= int(data["count"])
 

def jsonToXlsx():
    wb = openpyxl.Workbook()
    sheetsTitle = dataTypes
    sheets = {}
    sheets[sheetsTitle[0]] = wb.active
    sheets[sheetsTitle[0]].title = sheetsTitle[0]
    for i in range(1, len(sheetsTitle)):
        sheet = wb.create_sheet(title=langdata.data[sheetsTitle[i]])
        sheets[sheetsTitle[i]] = sheet
    for k, v in sheets.items():
        i = 1
        for title in sheetheader[k]:
            v.cell(column=i, row=1, value=langdata.data[title])
            i += 1
            
        i = 2
        for data in Database.data[k]:
            for j in range(0, len(data)):
                v.cell(column=j+1, row=i, value=str(data[sheetheader[k][j]]))
            i += 1
    
    return wb
    
    
    
@eel.expose
def saveToExcel():
    try:
        folder = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, 
            "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\User Shell Folders");
        desktoppath = winreg.QueryValueEx(folder, "Desktop")[0]
        
        now = datetime.datetime.now()
        timestamp = "{}_{}_{}_{}.{}.{}".format(now.year,now.month,now.day,now.hour,now.minute,now.second)
        path = os.path.join(desktoppath, "junting_"+timestamp+".xlsx")
        workbook = jsonToXlsx()
        workbook.save(filename=path)
    except Exception as e:
        raise e
    
        
@eel.expose
def saveAll():
    calculateStocks()
    Database.save()
    print("saved to file {}".format(Database.datapath))


Database = RuntimeDatabase()
langdata = LangData("en")
calculateStocks()
if __name__ == "__main__":
    try:
        eel.start("index-cn.html")
    except Exception as e:
        print(e)
    finally:
        Database.save()