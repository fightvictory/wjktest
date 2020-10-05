# while True:
#     str=input("please input a string:")#输入一个字符串
#     length=len(str)#求字符串长度
#     left=0#定义左右‘指针’
#     right=length-1
#     while left<right:#判断
#         if str[left]==str[right]:
#             left+=1
#             right-=1
#         else:
#             break;
#     if left==right:
#         print("yes")
#     else :
#         print("no")

def computeLcm(x,y):
    if (x > y): 
        greater = x
    else:
        greater = y
    while(True):
        if((greater%x == 0) & (greater%y == 0)):
            lcm = greater
            break
        greater += 1
    return lcm

print(computeLcm(24, 16))

def NonRecursiveGcd(x,y):
    
    while(y):
       
        x , y = y , x % y
        print('~~~~~')
        print(x,y)
    return x 

def RecursiveGcd(x,y):
 
    if y == 0:
        return x
    else:
        return RecursiveGcd(y, x%y)
print(NonRecursiveGcd(15, 24))
print(RecursiveGcd(15, 24))
def fib_recur(n):
  assert n >= 0, "n > 0"
  if n <= 1:
    return n
  return fib_recur(n-1) + fib_recur(n-2)

# for i in range(1, 3):
#     print(fib_recur(i))
# # print(fib_recur(3))

def fib_loop(n):
  a, b = 0, 1
  for i in range(n + 1):
    a, b = b, a + b
    print(a, b, end=':  ')
  return a
for i in range(0, 20):
  print('（%d）' % i, end= ' ')
  print( fib_loop(i))
