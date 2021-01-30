from tkinter import *
from neo4j import GraphDatabase

class MyWindow:
    def __init__(self, win):
        self.lbl1=Label(win, text='Name')
        self.lbl2=Label(win, text='Age')
        self.lbl5=Label(win, text='Game')
        self.lbl3=Label(win, text='Favorite Tags (maks 3)')
        self.lbl4=Label(win, text='Game wallet')
        self.t1=Entry(width=40)
        self.t2=Entry(width=40)
        self.t5=Entry(width=40)
        self.t3=Entry(width=40)
        #warning: don't input string
        self.t4=Entry(width=40)
        self.btn1 = Button(win, text='Register')
        self.lbl1.place(x=100, y=50)
        self.t1.place(x=300, y=50)
        self.lbl2.place(x=100, y=100)
        self.t2.place(x=300, y=100)
        self.lbl5.place(x=100, y=150)
        self.t5.place(x=300, y=150)
        self.lbl3.place(x=100, y=200)
        self.t3.place(x=300, y=200)
        self.lbl4.place(x=100, y=250)
        self.t4.place(x=300, y=250)
        self.b1=Button(win, text='Add', command=self.add)
        self.b1.place(x=100, y=300)
       
    
    def add(self):
        num1=self.t1.get()
        try:
            num2=int(self.t2.get())
        except:
            raise TypeError("please input number")
        
        num3=self.t3.get()
        tags=num3.split(" , ")
        total_tags= len(tags)
        num4=float(self.t4.get())
        num5=self.t5.get()
        num5=num5.split(" , ")
        is_requirement = int(num2)>= 13 and len(num5)> 0 and num4 >= 0
        if(is_requirement == True):          
            uri = "neo4j://localhost:7687"
            connect = GraphDatabase.driver(uri, auth=("neo4j", "123"))
            session = connect.session()
        
            query1= "MERGE (n:User { name: '"+num1+"', age: '"+num2+"', played_game: '"+num5+"', favorite_tags: '"+num3+"', game_wallet: "+str(num4)+" })"
            matchall1 = session.run(query1)   
            
            query2= "MATCH (n:User),(m:Game) WHERE n.name='"+num1+"' AND toLower(n.played_game) Contains toLower(m.game_name) MERGE (n)-[r:Played]->(m)"
            matchall2 = session.run(query2)  
            
            query3= "MATCH (n:User),(m:Tags) WHERE n.name='"+num1+"' AND toLower(n.favorite_tags) Contains toLower(m.tag_name) MERGE (n)-[r:Favorite_tag]->(m)"
            matchall3 = session.run(query3)   
        
        

window=Tk()
mywin=MyWindow(window)
window.title('Recommendation')
window.geometry("600x600+10+10")
window.mainloop()