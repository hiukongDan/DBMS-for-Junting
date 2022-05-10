import eel, json, os, datetime


dataTypes = [
   "stockin", 
   "soldout", 
   "items",
   "stocks"
]


class RuntimeDatabase:
    def __init__(self):
        self.datapath = "./app/data/data.json"
        self.recoverdatapath = "./app/data/.data.json_recover"
        
        # load data
        if(os.path.exists(self.datapath)):
            with open(self.datapath) as f:
                self.data = json.load(f);
        else:
            with open(self.datapath, 'w') as f:
                pass
            self.data = {"items":[], "stocks":[], "stockin":[], "soldout":[]}
        
        # save a recover data for this session
        self.savetofile(self.recoverdatapath)
            
            
    def savetofile(self, filename):
        with open(filename, "w") as f:
            json.dump(self.data, f);
        
        
    def save(self):
        self.savetofile(self.datapath)
        

        
        
        
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
    Database.data[dataType].append(newEntry)
    print("add new entry {} to {}".format(newEntry, dataType))


@eel.expose
def deleteEntry(dataType, index):
    # Primary key
    if(dataType == "items"):
        for type in ["stockin", "soldout", "stocks"]:
            deleteEntries(type, {"item": Database.data[dataType][index]["item"]})
    print("delete {} from {}".format(Database.data[dataType][index], dataType))
    del Database.data[dataType][index]

        
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

    
@eel.expose
def saveAll():
    Database.save()
    print("saved to file {}".format(Database.datapath))


Database = RuntimeDatabase()
if __name__ == "__main__":
    try:
        eel.start("index-en.html")
    except Exception as e:
        print(e)
    finally:
        Database.save()