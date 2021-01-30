from tkinter import *
from neo4j import GraphDatabase

class Mywindow:
    def __init__(self, win):
        self.lbl1=Label(win, text='Username')
        self.lbl2=Label(win, text='Top')
        self.lbl3=Label(win, text='Search')
        self.lbl4=Label(win, text='Recommendation')
        self.t1=Entry(width=40)
        self.t2=Entry(width=40)
        self.t3=Entry(width=40)
        self.t4=Entry(width=60)
        self.lbl1.place(x=100, y=50)
        self.t1.place(x=200, y=50)
        self.lbl2.place(x=100, y=100)
        self.t2.place(x=200, y=100)
        self.lbl3.place(x=100, y=150)
        self.t3.place(x=200, y=150)
        self.btn1 = Button(win, text='Check')
        self.b1=Button(win, text='recommendation', command=self.Getrecommendation)
        self.b1.place(x=100, y=200)
        self.lbl4.place(x=100, y=250)
        self.t4.place(x=200, y=250)
    
    def Getrecommendation(self):
        self.t4.delete(0, 'end')
        user=self.t1.get()
        if(self.t2.get()==""):
            top=""
        else:
            top=int(self.t2.get())
            
        search=self.t3.get()
        uri = "neo4j://localhost:7687"
        connect = GraphDatabase.driver(uri, auth=("neo4j", "123"))
        session = connect.session()
       
        #get favorite_tags and played_game
        query1= "Match(n:User) where n.name='"+user+"' return n.favorite_tags";
        query2= "Match(n:User) where n.name='"+user+"' return n.played_game";
        
        matchall1 = session.run(query1)
        matchall2 = session.run(query2)
        
        query3=""
        for i in matchall2:
            played_game=i[0].split(', ')
            for j in played_game:
                query3= query3+'AND p.game_name<>"'+j+'" '
        
        #rekomendasi game
        query4 = 'MATCH (n:User)-[r:Played]->(m:Game)-[s:Contains]->(o:Tags)<-[t:Contains]-(p:Game)'
        query4 = query4 + ' WHERE n.name="'+user+'" '+query3
        query4 = query4 + ' MERGE (p)-[u:Recommended_to {weight:s.weight*r.weight}]->(n)'
        query4 = query4 + ' RETURN n.name,p.game_name,u.weight'
        matchall4 = session.run(query4)
       
        
        #rekomendasi game berdasarkan favorit genre
        for i in matchall1:
            favorite_tags=i[0].split(' , ')
            total_tags= len(favorite_tags)
            query5 = "MATCH (n:Game)-[r1:Recommended_to]->(m:User)"
            query5 = query5 + " MATCH (m)-[r2:Favorite_tag]->(o:Tags)"
            query5 = query5 + " WHERE m.name='"+user+"' AND toLower(n.popular_tags) contains toLower(o.tag_name)" 
            query5 = query5 + " SET r1.weight = r1.weight+(0.25/"+str(total_tags)+") "
            query5 = query5 + " RETURN m.name,n.game_name,r1.weight" 
			matchall5 = session.run(query5)
            
			
        #rekomendasi game berdasarkan harga
        query6 = "MATCH (n:Game)-[r1:Recommended_to]->(m:User)"
        query6 = query6 + " MATCH(n)-[r2:hasPrice]->(o:Price)"
        query6 = query6 + " WHERE m.name='"+user+"' AND m.game_wallet<toFloat(n.price)" 
        query6 = query6 + " SET r1.weight = r1.weight+(r2.weight*0.5) "
        query6 = query6 + " RETURN m.name,n.game_name,r1.weight"
        matchall6 = session.run(query6)
         
        query7 = "MATCH (n:Game)-[r1:Recommended_to]->(m:User)"
        query7 = query7 + " MATCH(n)-[r2:hasPrice]->(o:Price)"
        query7 = query7 + " WHERE m.name='"+user+"' AND m.game_wallet>=toFloat(n.price)" 
        query7 = query7 + " SET r1.weight = r1.weight+(r2.weight) "
        query7 = query7 + " RETURN m.name,n.game_name,r1.weight"
        matchall7 = session.run(query7)
        
        #rekomendasi game berdasarkan review (dalam persen)
        query8 = "MATCH (n:Game)-[r1:Recommended_to]->(m:User)"
        query8 = query8 + " WHERE m.name='"+user+"'"
        query8 = query8 + " SET r1.weight = r1.weight+(0.25*(toFloat(n.all_reviews)/100))"
        query8 = query8 + " RETURN m.name,n.game_name,r1.weight"
        matchall8 = session.run(query8)

        
        #Sorting
        if(top!=""):
            query9="MATCH (n:Game)-[r:Recommended_to]->(p:User) WHERE p.name= '"+user+"' AND toLower(n.game_name) CONTAINS toLower('"+search+"') RETURN p.name,n.game_name,r.weight ORDER BY r.weight DESC LIMIT "+str(top)
        else:
            query9="MATCH (n:Game)-[r:Recommended_to]->(p:User) WHERE p.name= '"+user+"' AND toLower(n.game_name) CONTAINS toLower('"+search+"') RETURN p.name,n.game_name,r.weight ORDER BY r.weight DESC "
        matchall9 = session.run(query9)
        
        all_result=""
        for i in matchall9:
            print_result(i[0],i[1])
            print("Game: ", i[0])
            print("Weight: ", i[1])
            all_result= get_result(i[1])
            
        self.t4.insert(END, str(result))

window=Tk()
mywin=Mywindow(window)
window.title('Recommendation')
window.geometry("600x400+10+10")
window.mainloop()