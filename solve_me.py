class TasksCommand:
    TASKS_FILE = "tasks.txt"
    COMPLETED_TASKS_FILE = "completed.txt"

    current_items = {}
    completed_items = []

    def read_current(self):
        try:
            file = open(self.TASKS_FILE, "r")
            for line in file.readlines():
                item = line[:-1].split(" ")
                self.current_items[int(item[0])] = " ".join(item[1:])
            file.close()
        except Exception:
            pass

    def read_completed(self):
        try:
            file = open(self.COMPLETED_TASKS_FILE, "r")
            self.completed_items = file.readlines()
            file.close()
        except Exception:
            pass

    def write_current(self):
        with open(self.TASKS_FILE, "w+") as f:
            f.truncate(0)
            for key in sorted(self.current_items.keys()):
                f.write(f"{key} {self.current_items[key]}\n")

    def write_completed(self):
        with open(self.COMPLETED_TASKS_FILE, "w+") as f:
            f.truncate(0)
            for item in self.completed_items:
                f.write(f"{item}\n")

    def run(self, command, args):
        self.read_current()
        self.read_completed()
        if command == "add":
            self.add(args)
        elif command == "done":
            self.done(args)
        elif command == "delete":
            self.delete(args)
        elif command == "ls":
            self.ls()
        elif command == "report":
            self.report()
        elif command == "help":
            self.help()

    def help(self):
        print(
            """Usage :-
$ python tasks.py add 2 hello world # Add a new item with priority 2 and text "hello world" to the list
$ python tasks.py ls # Show incomplete priority list items sorted by priority in ascending order
$ python tasks.py del PRIORITY_NUMBER # Delete the incomplete item with the given priority number
$ python tasks.py done PRIORITY_NUMBER # Mark the incomplete item with the given PRIORITY_NUMBER as complete
$ python tasks.py help # Show usage
$ python tasks.py report # Statistics"""
        )

    def add(self, args):
        priority = args[0];
        taskString = args[1];
        #check duplication
        if priority in self.current_items.keys():
            return
        self.current_items[priority] = taskString
        self.write_current()
        print("Added task: \""+taskString+"\" with priority "+priority);

    def done(self, args):
        priority = args[0];
        #check task existance
        if(priority in self.current_items):
            #check if already completed by checking completed list
            if(priority not in self.completed_items):
                self.completed_items.append(priority)
                self.write_completed()
                print("Marked item as done")
        else:
            print("Error: no incomplete item with priority "+ priority +" exists.")

    def delete(self, args):
        priority = args[0]
        #check task existence
        if(priority in self.current_items.keys()):
            self.current_items.pop(priority)
            #check completed list for existence
            if(priority in self.completed_items):
                self.completed_items.remove(priority)
            self.write_completed()
            self.write_current()
            print("Deleted item with priority "+priority)
        else:
            print("Error: item with priority "+ priority +" does not exist. Nothing deleted.")

    def ls(self):
        for index, (priority, taskString) in enumerate(self.current_items.items()):
            print(str(index+1)+". "+taskString+ " ["+priority+"]")


    def report(self):
        COMPLETED_TASKS_COUNT = len(self.completed_items)
        PENDING_TASKS_COUNT = len(self.current_items) - COMPLETED_TASKS_COUNT
        #print pending
        print("Pending : "+str(PENDING_TASKS_COUNT))
        for index, (priority, taskString) in enumerate(self.current_items.items()):
            if(priority not in self.completed_items):
                print(str(index+1)+". "+taskString+ " ["+priority+"]")
        #print completed
        print("Completed : "+str(COMPLETED_TASKS_COUNT))
        for index, (priority, taskString) in enumerate(self.current_items.items()):
            if(priority in self.completed_items):
                print(str(index+1)+". "+taskString)
        pass
