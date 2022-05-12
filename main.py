import eel, json, os, datetime, winreg, openpyxl, bcrypt, string


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
    def __init__(self, user):
        self.datapath = "./app/data/data_"+user+".json"
        self.recoverdatapath = "./app/data/.data.json_recover"
        
        # load data
        if(os.path.exists(self.datapath)):
            with open(self.datapath, "r", encoding="utf8") as f:
                self.data = json.load(f);
        else:
            with open(self.datapath, 'w', encoding="utf8") as f:
                self.data = {"items":[], "stocks":[], "stockin":[], "soldout":[]}
                json.dump(self.data, f)
        
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
  

class LoginManager:
    def __init__(self):
        self.datapath = "./app/user/user.json"
        if not os.path.exists(self.datapath): 
            with open(self.datapath, "w") as f:
                f.write("{}");
        
        with open(self.datapath, "r") as f:
            self.data = json.load(f)
    
    
    def addUser(self, name, password):
        for usr, pwd in self.data.items():
            if usr == name:
                return False
        for c in password:
            if (c not in string.digits) and (c not in string.ascii_letters) and\
                (c not in string.punctuation):
                return False
                
        pwd = bytes(password, encoding="utf8")
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(pwd, salt)
        print("added user {}".format(name))
        self.data[name] = str(hashed, encoding="utf8")
        self.savetofile()
        return True
    
    
    def verifyUser(self, name, password):
        password = bytes(password, encoding="utf8")
        for user, pwd in self.data.items():
            if name == user and bcrypt.checkpw(password, bytes(pwd, encoding="utf8")):
                return True
        return False
        
        
    def changePwd(self, name, newpwd):
        newpwd = bytes(newpwd, encoding="utf8")
        for user, pwd in self.data.items():
            if name == user:
                salt = bcrypt.gensalt()
                hashed = bcrypt.hashpw(newpwd, salt)
                self.data[user] = str(hashed, encoding="utf8")
                self.savetofile()
                return True
        return False
        
        
    def savetofile(self):
        with open(self.datapath, "w") as f:
            json.dump(self.data, f);
        
        
        
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
            Database.data["stocks"].insert(0, {**newEntry, "count": 0})
    Database.data[dataType].insert(0, newEntry)
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
    
@eel.expose
def addUser(user, pwd):
    return loginManager.addUser(user, pwd)
      
      
@eel.expose
def verifyUser(user, pwd):
    success = loginManager.verifyUser(user, pwd)
    if (success):
        global Database
        Database = RuntimeDatabase(user)
        calculateStocks()
        print("user {} log in successfully".format(user))
    return success
    
    
@eel.expose
def changePwd(user, pwd):
    return loginManager.changePwd(user, pwd)
    

      
        
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
    
    

Database = None
langdata = LangData("en")
loginManager = LoginManager()
if __name__ == "__main__":
    try:
        eel.start("login-zh.html")
    except Exception as e:
        print(e)
    finally:
        if Database: Database.save()