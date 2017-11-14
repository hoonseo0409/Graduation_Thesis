# -*- coding: utf-8 -*-
from Tkinter import *
import time
import random
import math

Pos_lst=[]  #전하의 위치가 담긴 리스트
Pot_lst=[]  #각 점의 위치와 전위값이 담긴 배열
rpress_test=0 #마우스 우클릭 뗀 상태이면 0, 누른 상태이면 1
mheight=300 #창의 높이, 자연수로 입력
mwidth=450  #창의 너비, 자연수로 입력
distance=10 #경계조건으로 사용할 포텐셜 구할 간격(반드시 자연수 값 입력)
selfpot_cons=3.141592  #전하가 있는 위치의 주변 4픽셀에 전하밀도를 1/4씩 나눠서 가져가게 함 여기에 4로 나눈 값을 입력(즉, 이 값의 역수는 전위 재는 위치와 전하의 위치 사이의 거리를 의미함)
relex=2.0  #완화 상수, float으로 입력할 것, 최적완화상수 쓸거면 아무 float이나 입력해도 됨
erl=0.2   #변동의 비율이 이 값보다 작으면 계산 중지하고 iteration 출력
erp=erl
diserl=0.40 #격자점에서의 오차의 비율이 이것보다 작을때까지 유한차 근사
coc=0.5 #색 계수 0~1 float
tie=math.cos(math.pi/mwidth)+math.cos(math.pi/mheight)
relex=float((8-(64-16*tie*tie)**0.5)/(tie*tie)) #최적의 완화상수
Rho_lst=[]  #전하밀도값이 담긴 배열
relex=1.5

class App:
  def __init__(self, master):
    frame = Frame(master)
    frame.pack()
    self.slogan = Button(frame,
                         text="CLEAR potential",
                         command=self.clear_recal)
    self.slogan.pack(side=LEFT)
    self.makerande = Button(frame,text="Make 50 e",command=self.makerandel)
    self.makerande.pack(side=RIGHT)
  def clear_recal(self):
    for x in range(mwidth):
          for y in range(mheight):
              Pot_lst[x][y] = 0.
              Rho_lst[x][y]=0.
  def makerandel(self):
      for i in range(50):
          tmpx=random.randint(0,mwidth-1)
          tmpy=random.randint(0,mheight-1)
          Pos_lst.append([tmpx,tmpy])
          c.create_oval(tmpx, tmpy, tmpx, tmpy, outline="black", fill="black", width=2)


#random.randint(1,10)
def change_distance(event):
    global distance
    tmpdis=distance
    distance=int(entry.get())
    print "distance %d -> %d"%(tmpdis,distance)
    res.configure(text="Distance: " + str(eval(entry.get())))

def change_diserl(event):
    global diserl
    tmperr=diserl
    diserl=float(entry2.get())
    print "error limit %f -> %f"%(tmperr,diserl)
    res.configure(text="error limit: " + str(eval(entry2.get())))



def make_pot_lst(mwidth, mheight): #(0,0)~(mwidth-1,mheight-1)까지 모든 위치를 전위 리스트에 넣고 초기 전위값은 0으로 입력
    for x in range(mwidth): #x차원 생성
      Pot_lst.append([])
      for y in range(mheight):  #x차원 안에 y차원 생성
        Pot_lst[x].append(0.)

def make_rho_lst(mwidth, mheight):
  for x in range(mwidth):
    Rho_lst.append([])
    for y in range(mheight):
      Rho_lst[x].append(0.)

def cal_box(event):   #자기 자신 전위빼고 나머지 전위 기여 계산
  #전하와 인접한 4개 픽셀 측정위치에 전하밀도 전위 더해주기
  box_start=time.time() #외곽과 격자점 전위 측정 시작
  for i in range(len(Pos_lst)):
      Rho_lst[Pos_lst[i][0]][Pos_lst[i][1]] += selfpot_cons
      if (Pos_lst[i][0] != 0):
          Rho_lst[Pos_lst[i][0]-1][Pos_lst[i][1]] += selfpot_cons
      if (Pos_lst[i][1] != 0):
          Rho_lst[Pos_lst[i][0]][Pos_lst[i][1]-1] += selfpot_cons
      if ((Pos_lst[i][0] != 0) and (Pos_lst[i][1] != 0)):
          Rho_lst[Pos_lst[i][0]-1][Pos_lst[i][1]-1] += selfpot_cons


  #격자점에서의 정확한 전위 구하기
  global erp
  iteration=0
  er_sum=0.
  mean_diser=1.0

  if(mwidth%distance==0):
    xnumber=mwidth/distance #한 가로줄에 찍히는 위치 수(맞아 떨어지는 경우)
  else:
    xnumber = mwidth / distance + 1 #한 가로줄에 찍히는 위치 수(맨 처음 좌표는 무조건 찍어서 +1)
  if(mheight%distance==0):
    ynumber=mheight/distance
  else:
    ynumber=mheight/distance+1 #한 세로줄에 찍히는 위치 수(맨 처음 좌표는 무조건 찍어서 +1)
  for i in range(xnumber):
      for j in range(ynumber):
        add=0.
        for k in range(len(Pos_lst)):
          add+=1/(((i*distance-Pos_lst[k][0]+0.5)**2+(j*distance-Pos_lst[k][1]+0.5)**2)**0.5)
        Pot_lst[i*distance][j*distance]+=add+Rho_lst[i*distance][j*distance]

    #윗줄에서의 정확한 전위 구하기
  for i in range(mwidth-1):
    if(i%distance!=0):
        add = 0.
        for k in range(len(Pos_lst)):
          add += 1 / (((i  - Pos_lst[k][0]+0.5) ** 2 + (0 - Pos_lst[k][1]+0.5) ** 2) ** 0.5)
        Pot_lst[i][0] += add+Rho_lst[i][0]
    #아랫줄
  for i in range(mwidth-1):
    if((mheight%distance!=1)or(i%distance!=0)):
        add = 0.
        for k in range(len(Pos_lst)):
          add += 1 / (((i  - Pos_lst[k][0]+0.5) ** 2 + (mheight-1 - Pos_lst[k][1]+0.5) ** 2) ** 0.5)
        Pot_lst[i][mheight-1] += add+Rho_lst[i][mheight-1]
    #왼쪽 줄
  for i in range(1, mheight-1):
    if(i%distance!=0):
        add = 0.
        for k in range(len(Pos_lst)):
          add += 1 / (((0  - Pos_lst[k][0]+0.5) ** 2 + (i - Pos_lst[k][1]+0.5) ** 2) ** 0.5)
        Pot_lst[0][i] += add+Rho_lst[0][i]
  #오른쪽 줄
  for i in range(mheight):
    if((mwidth%distance!=1)or(i%distance!=0)):
        add = 0.
        for k in range(len(Pos_lst)):
          add += 1 / (((mwidth-1  - Pos_lst[k][0]+0.5) ** 2 + (i - Pos_lst[k][1]+0.5) ** 2) ** 0.5)
        Pot_lst[mwidth-1][i] += add+Rho_lst[mwidth-1][i]

  box_end=time.time()
  FDM_start=time.time()
  #유한차 근사 계산 시작

  #유한차 근사 격자점에서의 오차가 어떤 수 이하가 될때까지 근사하는 방법

  while (mean_diser >= diserl):
    sum_diser = 0.
    number=0.
    for y in range(1, mheight - 1):
      for x in range(1, mwidth - 1):
        tmp = Pot_lst[x][y]
        if ((x % distance != 0) or (y % distance != 0)):  # distance 격자점은 건너 뜀
          Pot_lst[x][y] = (relex / 4.) * (Pot_lst[x][y - 1] + Pot_lst[x + 1][y] + Pot_lst[x][y + 1] + Pot_lst[x - 1][y]+Rho_lst[x][y])+(1-relex)*(tmp)
        else:
          test = (relex / 4.) * (Pot_lst[x][y - 1] + Pot_lst[x + 1][y] + Pot_lst[x][y + 1] + Pot_lst[x - 1][y]+Rho_lst[x][y])+(1-relex)*(tmp)
          sum_diser+=abs((test-Pot_lst[x][y])/Pot_lst[x][y])
          number+=1
    mean_diser=sum_diser/number
    iteration += 1
  FDM_end=time.time()
  print "**********\tFDM END\t**********\ndistance=%d\nlimit error percentage=%f percent\niteration %d done\nnumber of electrons are %d\nFDM time taken = %d sec\nRelaxation constant=%f\n********************"%(distance, diserl*100, iteration, len(Pos_lst), FDM_end-FDM_start+box_end-box_start,relex)

#FDM 방식으로 전위 색칠하기
  min_lst=[]
  max_lst=[]
  for i in range(mwidth):
      max_lst.append(max(Pot_lst[i]))
  maxpot=max(max_lst)
  for i in range(mwidth):
      min_lst.append(min(Pot_lst[i]))
  minpot=min(min_lst)

  for i in range(mwidth):
      for j in range(mheight):
        c.create_oval(i, j, i, j, outline='#%02x%02x%02x' % (int(255 * ((Pot_lst[i][j]-minpot) / (maxpot-minpot))**coc), int(255 * ((Pot_lst[i][j]-minpot) / (maxpot-minpot))**coc), int(255 * ((Pot_lst[i][j]-minpot) / (maxpot-minpot))**coc)),
                      fill='#%02x%02x%02x' %  (int(255 * ((Pot_lst[i][j]-minpot) / (maxpot-minpot))**coc), int(255 * ((Pot_lst[i][j]-minpot) / (maxpot-minpot))**coc), int(255 * ((Pot_lst[i][j]-minpot) / (maxpot-minpot))**coc)), width=1)

  #모든 픽셀에 대해 정확한 계산 시작
  EX_start=time.time()
  number=0.
  for y in range(1,mheight-1):
    for x in range(1,mwidth-1):
      if((x%distance!=0)or(y%distance!=0)):
        tmp=Pot_lst[x][y]
        potsum = 0.
        for k in range(len(Pos_lst)):
          potsum += 1. / (((x - Pos_lst[k][0]+0.5) ** 2 + (y - Pos_lst[k][1]+0.5) ** 2) ** 0.5)
        Pot_lst[x][y] = potsum+Rho_lst[x][y]
        er_sum+=abs((tmp-Pot_lst[x][y])/Pot_lst[x][y])
        number+=1
  er_mean=er_sum/number
  EX_end=time.time()
  print "**********\tEXM END\t**********\nmean of percentage difference is %f\nEX time taken = %d sec\n********************"%(er_mean*100,EX_end-EX_start+box_end-box_start)

  #정확한 전위값에 비례해서 흰색 칠하기

  min_lst = []
  max_lst = []
  for i in range(mwidth):
    max_lst.append(max(Pot_lst[i]))
  maxpot = max(max_lst)
  for i in range(mwidth):
    min_lst.append(min(Pot_lst[i]))
  minpot = min(min_lst)
  for i in range(mwidth):
      for j in range(mheight):
        if(Pot_lst[i][j]<=0):
            print "DM nagative potential at (%d, %d)"%(i,j)
        c2.create_oval(i, j, i, j, outline='#%02x%02x%02x' % (int(255 * ((Pot_lst[i][j]-minpot) / (maxpot-minpot))**coc), int(255 * ((Pot_lst[i][j]-minpot) / (maxpot-minpot))**coc), int(255 * ((Pot_lst[i][j]-minpot) / (maxpot-minpot))**coc)),
                      fill='#%02x%02x%02x' % (int(255 * ((Pot_lst[i][j]-minpot) / (maxpot-minpot))**coc), int(255 * ((Pot_lst[i][j]-minpot) / (maxpot-minpot))**coc), int(255 * ((Pot_lst[i][j]-minpot) / (maxpot-minpot))**coc)), width=1)
def moving(event):  #마우스 움직일 때
  if ((mwidth>event.x >= 0) and (mheight>event.y >= 0)):
      if(rpress_test==1): #우클릭 누른 상태
        Pos_lst.append([event.x, event.y])  #전하의 위치리스트에 마우스 위치 추가
        c.create_oval(event.x, event.y, event.x, event.y, outline="black", fill="black", width=2) #전하의 위치에 검은색 점이고 크기는 2인 원 그리기
      print Pot_lst[event.x][event.y]
  return

def left_press(event):
  Pos_lst.append([event.x, event.y])
  c.create_oval(event.x, event.y, event.x, event.y, outline="black", fill="black", width=2)
  return

def right_press(event):
  global rpress_test
  rpress_test=1

def right_release(event):
  global rpress_test
  rpress_test=0


#메인 코드 시작

make_pot_lst(mwidth, mheight)
make_rho_lst(mwidth, mheight)
root = Tk()
root.title("Electron Input and FDM Potential")
root.resizable(0,0)
root2 = Tk()
root2.title("EX Potential")
root2.resizable(0,0)
root3=Tk()

c=Canvas(root,height=mheight,width=mwidth)
c.pack()
c2=Canvas(root2, height=mheight, width=mwidth)
c2.pack()
c.bind('<Motion>',moving)
c2.bind('<Motion>',moving)
c.bind('<Button-1>',left_press)
#c.bind('<Button-1>',clear_recal)
c.bind('<Button-2>',cal_box)
c.bind('<Button-3>',right_press)
c.bind('<ButtonRelease-3>',right_release)

#초기화 및 변수 변환창
Label(root3, text="Your Distance integer:").pack()
entry = Entry(root3)
entry2=Entry(root3)
entry.bind("<Return>", change_distance)
entry2.bind("<Return>", change_diserl)
entry.pack()
Label(root3, text="Your Error Limit 0~1 float:").pack()
entry2.pack()
res = Label(root3)
res.pack()

app=App(root3)


mainloop()



