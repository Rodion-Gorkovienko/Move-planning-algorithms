from graphics import *
import msvcrt

#Структура для хранения информации о вершинах графа.
class Vertex:
    def __init__(self, x=0.0, y=0.0, associated={}, value=720000, visited=False, previous=-1, heuristics=-1.0):
        self.associated=associated
        self.value=value
        self.visited=visited
        self.previous=previous
        self.x=x
        self.y=y
        self.heuristics=heuristics

def get_dict(ways):
    d={}
    for i in range(len(ways)):
        if ways[i]!=0:
            d[i]=ways[i]
    return d

def distance(a, b):
    x=(a.x-b.x)
    y=(a.y-b.y)
    return ((x*x)+(y*y))**0.5

def area(a,b,c):
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)

def check_pro(a,b,c,d):
    x=0
    if a>b:
        x=a
        a=b
        b=x
    if c>d:
        x=c
        c=d
        d=x
    return max(a,c) <= min(b,d)

def check_points(a,b,c,d):
    return not((a.x==c.x and a.y==c.y) or (a.x==d.x and a.y==d.y) or (b.x==c.x and b.y==c.y) or (b.x==d.x and b.y==d.y))

def cross(a, b, c, d):
    return check_pro(a.x, b.x, c.x, d.x) and check_pro(a.x, b.x, c.x, d.x) and area(a,b,c) * area(a,b,d) <= 0 and area(c,d,a) * area(c,d,b) <= 0 and check_points(a,b,c,d)

def in_triangle(p, a, b, c):
    ab=Point((a.x+b.x)/2,(a.y+b.y)/2)
    bc=Point((b.x+c.x)/2,(b.y+c.y)/2)
    ca=Point((c.x+a.x)/2,(c.y+a.y)/2)
    flag=0
    if distance(p,a)+distance(p,b)==distance(a,b) or distance(p,b)+distance(p,c)==distance(b,c) or distance(p,c)+distance(p,a)==distance(c,a):
        flag=1
    return flag==1 or not(cross(p,a,b,c) or cross(p,b,a,c) or cross(p,c,a,b) or cross(p,ab,a,c) or cross(p,ab,c,b) or cross(p,bc,b,a) or cross(p,bc,a,c) or cross(p,ca,c,b) or cross(p,ca,b,a)) 

def in_polygon(p, polygon):
    chenge_st=0
    i=0
    polygonc=polygon.copy()
    for i in range(len(polygonc)):
        if p.x==polygonc[i].x and p.y==polygonc[i].y:
            chenge_st=1
    if chenge_st==0:
        while len(polygonc)>2:
            if in_triangle(p,polygonc[-1],polygonc[-2],polygonc[-3]):
                if not(distance(p,polygonc[-1])+distance(p,polygonc[-3])==distance(polygonc[-1],polygonc[-3])):
                    chenge_st+=1
            polygonc.pop(-2)
    return chenge_st%2==1
def det(a, b, c, d):
    return a*d-b*c

def between(a, b, c):
    return min(a,b)<=c and c<=max(a,b)

def cross_point(a, b, c, d):
    a1=a.y-b.y
    b1=b.x-a.x
    c1=-a1*a.x-b1*a.y
    a2=c.y-d.y
    b2=d.x-c.x
    c2=-a2*c.x-b2*c.y
    zn=det (a1, b1, a2, b2)
    if zn!=0:
        x =-det(c1, b1, c2, b2)/ zn
        y =-det(a1, c1, a2, c2)/ zn
        if between(a.x, b.x, x) and between(a.y, b.y, y) and between(c.x, d.x, x) and between (c.y, d.y, y):
            ans=Point(x, y)
        else:
            ans=Point(-1, -1)
    else:
        ans=Point(-1, -1)
    return ans

def sort(p, points_def):
    dis=[]
    points_dis=[]
    points=[]
    for i in range(len(points_def)):
        points_dis.append([points_def[i],distance(p,points_def[i])])
    points_dis=sorted(points_dis, key=lambda x: x[1])
    for i in range(len(points_dis)):
        points.append(points_dis[i][0])
    return points

def delayed(pa, pb, surface):
    lines_cross=[]
    for i_s in range(len(surface)):
        size=len(surface[i_s])
        points_cross=[]
        for j_s in range(size):
            if cross(pa, pb, surface[i_s][j_s], surface[i_s][(j_s+1)%len(surface[i_s])]):
                crp=cross_point(pa, pb, surface[i_s][j_s], surface[i_s][(j_s+1)%len(surface[i_s])])
                points_cross.append(crp)
        points_cross=sort(pa, points_cross)
        if len(points_cross)>0:
            if in_polygon(Point(pa.x+points_cross[0].x, pa.y+points_cross[0].y), surface[i_s]):
                lines_cross.append([pa, points_cross[0]])
                points_cross.pop(0)
            while len(points_cross)>1:
                lines_cross.append([points_cross[0], points_cross[1]])
                points_cross.pop(0)
                points_cross.pop(0)
            if len(points_cross)==1:
                lines_cross.append([points_cross[0], pb])
                points_cross.pop(0)
    i_s=0
    while i_s<len(lines_cross)-1:
        j_s=i_s+1
        while j_s<len(lines_cross):
            if between(distance(pa,lines_cross[i_s][0]),distance(pa,lines_cross[i_s][1]),distance(pa,lines_cross[j_s][0])) or between(distance(pa,lines_cross[i_s][0]),distance(pa,lines_cross[i_s][1]),distance(pa,lines_cross[j_s][1])):
                if distance(pa,lines_cross[i_s][0])>distance(pa,lines_cross[i_s][1]):
                    change_line=lines_cross[i_s][0]
                    lines_cross[i_s][0]=lines_cross[i_s][1]
                    lines_cross[i_s][1]=change_line
                if distance(pa,lines_cross[j_s][0])>distance(pa,lines_cross[j_s][1]):
                    change_line=lines_cross[j_s][0]
                    lines_cross[j_s][0]=lines_cross[j_s][1]
                    lines_cross[j_s][1]=change_line
                if distance(pa,lines_cross[i_s][0])>distance(pa,lines_cross[j_s][0]):
                    lines_cross[i_s][0]=lines_cross[j_s][0]
                if distance(pa,lines_cross[i_s][1])<distance(pa,lines_cross[j_s][1]):
                    lines_cross[i_s][1]=lines_cross[j_s][1]
            j_s+=1
        i_s+=1
    i_s=0
    flag=0
    for i_s in range(len(surface)):
        for j_s in range(len(surface[i_s])):
            if (surface[i_s][j_s]==pa and surface[i_s][(j_s+1)%len(surface[i_s])]==pb) or (surface[i_s][j_s]==pb and surface[i_s][(j_s+1)%len(surface[i_s])]==pa):
                flag=1
        if (in_polygon(pa, surface[i_s]) and in_polygon(pb, surface[i_s])) and flag==0:
            lines_cross=[[pa,pb]]
    return lines_cross

def final_distance(pa, pb, surface):
    lines_del=delayed(pa, pb, surface)
    del_dis=0
    for i in range(len(lines_del)):
        del_dis+=distance(lines_del[i][0], lines_del[i][1])
    return distance(pa, pb)+del_dis*0.5

def division(point0, point1):
    dx=point1.x-point0.x
    dy=point1.y-point0.y
    dis=distance(point0,point1)
    nx=(dx/dis)*3
    ny=(dy/dis)*3
    x=point0.x+nx
    y=point0.y+ny
    points=[]
    for i in range(int(dis/3)):
        points.append(Point(x,y))
        x+=nx
        y+=ny
    return points

def cross_p_p(p1,p2,n,polygons,surface):
    flag=0
    i=0
    while i<n and flag==0:
        j=0
        size=len(polygons[i])
        while j<size and flag==0:
            if cross(p1, p2, polygons[i][j], polygons[i][(j+1)%len(polygons[i])]):
                flag=1
            j+=1
        i+=1
    if flag==0:
        res=final_distance(p1,p2,surface)
    else:
        res=0
    return res

def cross_p_p_sur(p1,p2,n,polygons,n_s,surface,i_sp,j_sp):
    flag=0
    i=0
    while i<n and flag==0:
        j=0
        size=len(polygons[i])
        while j<size and flag==0:
            if cross(p1, p2, polygons[i][j], polygons[i][(j+1)%len(polygons[i])]):
                flag=1
            j+=1
        i+=1
    i=0
    while i<n_s and flag==0:
        j=0
        size=len(surface[i])
        while j<size and flag==0:
            if i!=i_sp or j!=j_sp:
                if cross(p1, p2, surface[i][j], surface[i][(j+1)%len(surface[i])]):
                    flag=1
            j+=1
        i+=1
    if flag==0:
        res=final_distance(p1,p2,surface)
    else:
        res=0
    return res

def cross_p_p_self_sur(p1,p2,n,polygons,n_s,surface,i_sp,j_sp,i2,j2):
    flag=0
    i=0
    while i<n and flag==0:
        j=0
        size=len(polygons[i])
        while j<size and flag==0:
            if cross(p1, p2, polygons[i][j], polygons[i][(j+1)%len(polygons[i])]):
                flag=1
            j+=1
        i+=1
    i=0
    while i<n_s and flag==0:
        j=0
        size=len(surface[i])
        while j<size and flag==0:
            if (i!=i_sp or j!=j_sp) and (i!=i2 or j!=j2):
                if cross(p1, p2, surface[i][j], surface[i][(j+1)%len(surface[i])]):
                    flag=1
            j+=1
        i+=1
    if flag==0:
        res=final_distance(p1,p2,surface)
    else:
        res=0
    return res
#ВВОД---------------------------------------------------------------------------
choice=0
while choice==0:
    print("Выберите один из вариантов:")
    print("1 - Построить схему вручную")
    print("2 - Использовать готовую схему")
    text_choice=input()
    if text_choice=="1" or text_choice=="2":
        choice=int(text_choice)
    else:
        print("Ошибка. Повторите попытку")
if choice==1:
    print("Для премещения курсора используйте клавиши w,a,s,d.")
    print("Включить/выключить режим расстановки точек начала/конца - z")
    print("Включить/выключить режим расстановки точек многоугольников - x")
    print("Включить/выключить режим расстановки точек зон плохой проходимости - c")
    print("Установить точку в текущем режиме - space")
    print("Завершить многоугольник в текущем режиме - e")
    print("Подтвердить схему - f")
    win=GraphWin("Схема движения", 600, 600)
    cursor=[]
    cursor.append(Line(Point(300,300),Point(295,305)))
    cursor.append(Line(Point(300,300),Point(305,305)))
    cursor[0].setOutline("blue")
    cursor[1].setOutline("blue")
    cursor[0].draw(win)
    cursor[1].draw(win)
    status=0
    point_a=Point(601,601)
    point_b=Point(601,601)
    point_a.setOutline("green")
    point_b.setOutline("green")
    point_a.draw(win)
    point_b.draw(win)
    polygons=[]
    i=-1
    surface=[]
    i_s=-1
    while True:
        key=msvcrt.getch()
        if ord(key)==ord('w'):
            if cursor[0].p1.y>0:
                cursor[0].move(0,-2)
                cursor[1].move(0,-2)
        elif ord(key)==ord('s'):
            if cursor[0].p1.y<600:
                cursor[0].move(0,2)
                cursor[1].move(0,2)
        elif ord(key)==ord('d'):
            if cursor[0].p1.x<600:
                cursor[0].move(2,0)
                cursor[1].move(2,0)
        elif ord(key)==ord('a'):
            if cursor[0].p1.x>0:
                cursor[0].move(-2,0)
                cursor[1].move(-2,0)
        elif ord(key)==ord('z'):
            if status==0:
                status=1
                turn=0
                cursor[0].setOutline("green")
                cursor[1].setOutline("green")
            elif status==1:
                status=0
                cursor[0].setOutline("blue")
                cursor[1].setOutline("blue")
            elif status==2:
                status=1
                if j>1:
                    Line(polygons[i][j],polygons[i][0]).draw(win)
                turn=0
                cursor[0].setOutline("green")
                cursor[1].setOutline("green")
            elif status==3:
                status=1
                if j_s>1:
                    l_s=Line(surface[i_s][j_s],surface[i_s][0])
                    l_s.setOutline("orange")
                    l_s.draw(win)
                turn=0
                cursor[0].setOutline("green")
                cursor[1].setOutline("green")
        elif ord(key)==ord('x'):
            if status==0:
                status=2
                polygons.append([])
                i+=1
                j=-1
                cursor[0].setOutline("black")
                cursor[1].setOutline("black")
            elif status==1:
                status=2
                polygons.append([])
                i+=1
                j=-1
                cursor[0].setOutline("black")
                cursor[1].setOutline("black")
            elif status==2:
                status=0
                if j>1:
                    Line(polygons[i][j],polygons[i][0]).draw(win)
                cursor[0].setOutline("blue")
                cursor[1].setOutline("blue")
            elif status==3:
                status=2
                polygons.append([])
                i+=1
                j=-1
                if j_s>1:
                    l_s=Line(surface[i_s][j_s],surface[i_s][0])
                    l_s.setOutline("orange")
                    l_s.draw(win)
                cursor[0].setOutline("black")
                cursor[1].setOutline("black")
        elif ord(key)==ord('c'):
            if status==0:
                status=3
                surface.append([])
                i_s+=1
                j_s=-1
                cursor[0].setOutline("orange")
                cursor[1].setOutline("orange")
            elif status==1:
                status=3
                surface.append([])
                i_s+=1
                j_s=-1
                cursor[0].setOutline("orange")
                cursor[1].setOutline("orange")
            elif status==2:
                status=3
                if j>1:
                    Line(polygons[i][j],polygons[i][0]).draw(win)
                surface.append([])
                i_s+=1
                j_s=-1
                cursor[0].setOutline("orange")
                cursor[1].setOutline("orange")
            elif status==3:
                status=0
                if j_s>1:
                    l_s=Line(surface[i_s][j_s],surface[i_s][0])
                    l_s.setOutline("orange")
                    l_s.draw(win)
                cursor[0].setOutline("blue")
                cursor[1].setOutline("blue")
        elif ord(key)==ord(' '):
            if status==1:
                if turn==0:
                    point_a.move(cursor[0].p1.x-point_a.x, cursor[0].p1.y-point_a.y)
                    turn=1
                elif turn==1:
                    point_b.move(cursor[0].p1.x-point_b.x, cursor[0].p1.y-point_b.y)
                    turn=0
            elif status==2:
                point_p=Point(cursor[0].p1.x,cursor[0].p1.y)
                point_p.draw(win)
                polygons[i].append(point_p)
                j+=1
                if j>0:
                    Line(polygons[i][j],polygons[i][j-1]).draw(win)
            elif status==3:
                point_s=Point(cursor[0].p1.x,cursor[0].p1.y)
                point_s.setOutline("orange")
                point_s.draw(win)
                surface[i_s].append(point_s)
                j_s+=1
                if j_s>0:
                    l_s=Line(surface[i_s][j_s],surface[i_s][j_s-1])
                    l_s.setOutline("orange")
                    l_s.draw(win)

        elif ord(key)==ord("e"):
            if status==2:
                if j>1:
                    Line(polygons[i][j],polygons[i][0]).draw(win)
                polygons.append([])
                i+=1
                j=-1
            elif status==3:
                if j_s>1:
                    l_s=Line(surface[i_s][j_s],surface[i_s][0])
                    l_s.setOutline("orange")
                    l_s.draw(win)
                surface.append([])
                i_s+=1
                j_s=-1


        elif ord(key)==ord('f'):
            if status==3 and j_s>1:
                    l_s=Line(surface[i_s][j_s],surface[i_s][0])
                    l_s.setOutline("orange")
                    l_s.draw(win)
            break;
    n=i+1
    n_s=i_s+1
else:
    while choice==2:
        print("Введте название файла:")
        nof=input()
        nof=nof+".txt"
        f=open(nof)
        l = [line.strip() for line in f]
        x,y=map(float, l[0].split())
        point_a=Point(x,y)
        l.pop(0)
        x,y=map(float, l[0].split())
        point_b=Point(x,y)
        l.pop(0)
        n=int(l[0])
        l.pop(0)
        polygons=[]
        for i in range(n):
            polygons.append([])
            size=int(l[0])
            l.pop(0)
            for j in range(size):
                x,y=map(float, l[0].split())
                l.pop(0)
                polygons[i].append(Point(x,y))
        n_s=int(l[0])
        l.pop(0)
        surface=[]
        for i in range(n_s):
            surface.append([])
            size=int(l[0])
            l.pop(0)
            for j in range(size):
                x,y=map(float, l[0].split())
                l.pop(0)
                surface[i].append(Point(x,y))
        win=GraphWin("Схема движения", 600, 600)
        for i in range(n_s):
            for j in range(len(surface[i])):
                l_s=Line(surface[i][j],surface[i][(j+1)%len(surface[i])])
                l_s.setOutline("orange")
                l_s.draw(win)
        for i in range(n):
            for j in range(len(polygons[i])):
                whole=Line(polygons[i][j], polygons[i][(j+1)%len(polygons[i])])
                whole.draw(win)
        point_a.setOutline("green")
        point_a.draw(win)
        point_b.setOutline("green")
        point_b.draw(win)
        choice=0
        while choice==0:
            print("Выберите действие:")
            print("1 - Подтвердить")
            print("2 - Изменить координаты точек начала/конца.")
            print("3 - Выбрать другую схему.")
            text_choice=input()
            if text_choice=="1" or text_choice=="2" or text_choice=="3":
                choice=int(text_choice)
            else:
                print("Ошибка. Повторите попытку")
        if choice==3:
            win.close()
            choice=2
            f.close()
        elif choice==2:
            turn=0
            print("Для премещения курсора используйте клавиши w,a,s,d.")
            print("Установить точку - space")
            print("Подтвердить схему - f")
            cursor=[]
            cursor.append(Line(Point(300,300),Point(295,305)))
            cursor.append(Line(Point(300,300),Point(305,305)))
            cursor[0].setOutline("green")
            cursor[1].setOutline("green")
            cursor[0].draw(win)
            cursor[1].draw(win)

            while True:
                key=msvcrt.getch()
                if ord(key)==ord('w'):
                    if cursor[0].p1.y>0:
                        cursor[0].move(0,-2)
                        cursor[1].move(0,-2)
                elif ord(key)==ord('s'):
                    if cursor[0].p1.y<600:
                        cursor[0].move(0,2)
                        cursor[1].move(0,2)
                elif ord(key)==ord('d'):
                    if cursor[0].p1.x<600:
                        cursor[0].move(2,0)
                        cursor[1].move(2,0)
                elif ord(key)==ord('a'):
                    if cursor[0].p1.x>0:
                        cursor[0].move(-2,0)
                        cursor[1].move(-2,0)
                elif ord(key)==ord(' '):
                    if turn==0:
                        point_a.move(cursor[0].p1.x-point_a.x, cursor[0].p1.y-point_a.y)
                        turn=1
                    elif turn==1:
                        point_b.move(cursor[0].p1.x-point_b.x, cursor[0].p1.y-point_b.y)
                        turn=0
                elif ord(key)==ord('f'):
                    break;
            choice=0
        elif choice==1:
            f.close()

#СОСТАВЛЕНИЕ ГРАФА--------------------------------------------------------------
print("Построение графа начато...")
#Очистка списков от пустых многоугольников
i=0
while i<len(polygons):
    if len(polygons[i])==0:
        polygons.pop(i)
        n-=1
    else:
        i+=1
i=0
while i<len(surface):
    if len(surface[i])==0:
        surface.pop(i)
        n_s-=1
    else:
        i+=1
#Формирование списка точек на рёбрах многоульников замедляющих поверхнстей
surface_points=[]
for i in range(len(surface)):
    surface_points.append([])
    for j in range(len(surface[i])):
        surface_points[i].append(division(surface[i][j],surface[i][(j+1)%len(surface[i])]))

graph=[]#Граф - список вершин
ways=[]#Список стоимостей пути для текущей вершины в другие
ways.append(0)
flag=0
#Проверка возможности попасть из A в Б 
ways.append(cross_p_p(point_a,point_b,n,polygons,surface))
#Проверка возможности попасть из A в каждую вершину многоугольников
for i in range(n):
    for j in range(len(polygons[i])):
        ways.append(cross_p_p(point_a,polygons[i][j],n,polygons,surface))
#Проверка возможности попасть из A в каждую вершину многоугольников замедляющих поверхнстей
for i in range(n_s):
    for j in range(len(surface[i])):
        ways.append(cross_p_p(point_a,surface[i][j],n,polygons,surface))
#Проверка возможности попасть из A в каждую точку многоугольников замедляющих поверхнстей
for i in range(len(surface_points)):
    for j in range(len(surface_points[i])):
        for k in range(len(surface_points[i][j])):
            ways.append(cross_p_p_sur(point_a,surface_points[i][j][k],n,polygons,n_s,surface,i,j))
graph.append(Vertex(point_a.x, point_a.y, get_dict(ways), 0))

#Заполнение ways для уже известных вершин (А)
ways=[]
if graph[0].associated.get(1)!=None:
    ways.append(graph[0].associated[1])
else:
    ways.append(0)
ways.append(0)
flag=0
#Аналогичные проверки для Б
for i in range(n):
    for j in range(len(polygons[i])):
        ways.append(cross_p_p(point_b,polygons[i][j],n,polygons,surface))
for i in range(n_s):
    for j in range(len(surface[i])):
        ways.append(cross_p_p(point_b,surface[i][j],n,polygons,surface))
for i in range(len(surface_points)):
    for j in range(len(surface_points[i])):
        for k in range(len(surface_points[i][j])):
            ways.append(cross_p_p_sur(point_b,surface_points[i][j][k],n,polygons,n_s,surface,i,j))
graph.append(Vertex(point_b.x, point_b.y, get_dict(ways)))

#Аналогичные проверки для каждой вершины многоугольников
q=1
complited=0
for i1 in range(n):
    for j1 in range(len(polygons[i1])):
        ways=[]
        q+=1
        for i in range(2+complited):
            if graph[i].associated.get(q)!=None:
                ways.append(graph[i].associated[q])
            else:
                ways.append(0)
        miss=0
        flag=0
        for i in range(n):
            for j in range(len(polygons[i])):
                if miss<complited:
                    miss+=1
                else:
                    if not(i==i1 and j==j1):
                        if (i==i1 and (j==(j1+1)%len(polygons[i1]) or j1==(j+1)%len(polygons[i1]))) or not(in_polygon(Point((polygons[i1][j1].x+polygons[i][j].x)/2, (polygons[i1][j1].y+polygons[i][j].y)/2), polygons[i1])):
                            ways.append(cross_p_p(polygons[i1][j1],polygons[i][j],n,polygons,surface))
                        else:
                            ways.append(0)
                    else:
                        ways.append(0)
        flag=0
        for i in range(n_s):
            for j in range(len(surface[i])):
                if miss<complited:
                    miss+=1
                else:
                    if not(in_polygon(Point((polygons[i1][j1].x+surface[i][j].x)/2, (polygons[i1][j1].y+surface[i][j].y)/2), polygons[i1])):
                        ways.append(cross_p_p(polygons[i1][j1],surface[i][j],n,polygons,surface))
                    else:
                        ways.append(0)
        flag=0
        for i in range(len(surface_points)):
            for j in range(len(surface_points[i])):
                for k in range(len(surface_points[i][j])):
                    if miss<complited:
                        miss+=1
                    else:
                        if not(in_polygon(Point((polygons[i1][j1].x+surface_points[i][j][k].x)/2, (polygons[i1][j1].y+surface_points[i][j][k].y)/2), polygons[i1])):
                            ways.append(cross_p_p_sur(polygons[i1][j1],surface_points[i][j][k],n,polygons,n_s,surface,i,j))
                        else:
                            ways.append(0)
        complited+=1
        graph.append(Vertex(polygons[i1][j1].x, polygons[i1][j1].y, get_dict(ways)))
#Аналогичные проверки для каждой вершины многоугольников замедляющих поверхностей
q=len(graph)-1
pre_len=len(graph)
complited=0
for i1 in range(n_s):
    for j1 in range(len(surface[i1])):
        ways=[]
        q+=1
        for i in range(pre_len+complited):
            if graph[i].associated.get(q)!=None:
                ways.append(graph[i].associated[q])
            else:
                ways.append(0)
        miss=0
        for i in range(n_s):
            for j in range(len(surface[i])):
                if miss<complited:
                    miss+=1
                else:
                    if i!=i1 or j!=j1:
                        ways.append(cross_p_p(surface[i1][j1],surface[i][j],n,polygons,surface))
                    else:
                        ways.append(0)
        for i in range(len(surface_points)):
            for j in range(len(surface_points[i])):
                for k in range(len(surface_points[i][j])):
                    if miss<complited:
                        miss+=1
                    else:
                        ways.append(cross_p_p_sur(surface[i1][j1],surface_points[i][j][k],n,polygons,n_s,surface,i,j))
        complited+=1
        graph.append(Vertex(surface[i1][j1].x, surface[i1][j1].y, get_dict(ways)))
q=len(graph)-1
pre_len=len(graph)
complited=0
#Аналогичные проверки для каждой вершины точек замедляющих поверхностей
for i1 in range(len(surface_points)):
    for j1 in range(len(surface_points[i1])):
        for k1 in range(len(surface_points[i1][j1])):
            ways=[]
            q+=1
            for i in range(pre_len+complited):
                if graph[i].associated.get(q)!=None:
                    ways.append(graph[i].associated[q])
                else:
                    ways.append(0)
            miss=0
            for i in range(len(surface_points)):
                for j in range(len(surface_points[i])):
                    for k in range(len(surface_points[i][j])):
                        if miss<complited:
                            miss+=1
                        else:
                            ways.append(cross_p_p_self_sur(surface_points[i1][j1][k1],surface_points[i][j][k],n,polygons,n_s,surface,i,j,i1,j1))
            complited+=1
            graph.append(Vertex(surface_points[i1][j1][k1].x, surface_points[i1][j1][k1].y, get_dict(ways)))
print("Построение графа завершено.")
#ПОИСК ПУТИ (АЛГОРИТМ A*)-------------------------------------------------
print("Поиск пути начат...")
i_v=0
while graph[1].visited==False:
    min=720000
    visit=0
    for i in range(len(graph)):
        if graph[i].heuristics==-1:
            graph[i].heuristics=distance(Point(graph[i].x, graph[i].y), point_b)
        if graph[i].value + graph[i].heuristics <min and graph[i].visited==False:
            min=graph[i].value + graph[i].heuristics
            visit=i
    for i in graph[visit].associated:
        if graph[i].heuristics==-1:
            graph[i].heuristics=distance(Point(graph[i].x, graph[i].y), point_b)
        if graph[i].visited==False and graph[visit].associated[i] + graph[visit].value < graph[i].value:
            graph[i].value=graph[visit].associated[i]+graph[visit].value
            graph[i].previous=visit
    graph[visit].visited=True
    i_v+=1
print("Поиск пути завершён.")
print("Посещено вершин:")
print(i_v)
#ВЫВОД--------------------------------------------------------------------------
if choice==2:
    win=GraphWin("Схема движения", 600, 600)
    for i in range(n_s):
        for j in range(len(surface[i])):
            l_s=Line(surface[i][j],surface[i][(j+1)%len(surface[i])])
            l_s.setOutline("orange")
            l_s.draw(win)
    point_a.setOutline("green")
    point_a.draw(win)
    point_b.setOutline("green")
    point_b.draw(win)
for i in range(n):
    for j in range(len(polygons[i])):
        whole=Line(polygons[i][j], polygons[i][(j+1)%len(polygons[i])])
        whole.draw(win)
points=[]
points.append(point_a)
points.append(point_b)
for i in range(n):
    for j in range(len(polygons[i])):
        points.append(polygons[i][j])
for i in range(n_s):
    for j in range(len(surface[i])):
        points.append(surface[i][j])
for i in range(n_s):
    for j in range(len(surface_points[i])):
        for k in range(len(surface_points[i][j])):
            points.append(surface_points[i][j][k])
step=1
while step!=0:
    next=graph[step].previous
    way=Line(points[step],points[next])
    way.setOutline("green")
    way.draw(win)
    step=next
ta=Text(Point(point_a.x+10,point_a.y-10),"А")
tb=Text(Point(point_b.x+10,point_b.y-10),"Б")
ta.draw(win)
tb.draw(win)
print("Кликние ЛКМ по схеме, чтобы завершить просмотр.")
win.getMouse()
win.close()
choice=0
while choice==0:
    print("Сохранить схему?")
    print("1 - Да")
    print("2 - Нет")
    text_choice=input()
    if text_choice=="1" or text_choice=="2":
        choice=int(text_choice)
    else:
        print("Ошибка. Повторите попытку")
if choice==1:
    print("Введте название файла:")
    nof=input()
    nof=nof+".txt"
    f=open(nof, 'w')
    f.write(str(point_a.x)+' '+str(point_a.y)+'\n')
    f.write(str(point_b.x)+' '+str(point_b.y)+'\n')
    f.write(str(n)+'\n')
    for i in range(n):
        size=len(polygons[i])
        f.write(str(size)+'\n')
        for j in range(size):
            f.write(str(polygons[i][j].x)+' '+str(polygons[i][j].y)+'\n')
    f.write(str(n_s)+'\n')
    for i in range(n_s):
        size=len(surface[i])
        f.write(str(size)+'\n')
        for j in range(size):
            f.write(str(surface[i][j].x)+' '+str(surface[i][j].y)+'\n')
    f.close()

    