import tkinter as tk
from tkinter import messagebox as msg
from PIL import Image,ImageTk

root = tk.Tk()
#Title:
root.title("Calculator")

#Icon:
img = Image.open(r"./Calculator\icon.png")
icon = ImageTk.PhotoImage(img)
root.wm_iconphoto(False,icon)

#Input-Output Labels:
l1 = tk.Label(root,text="",font=('Arial',20),anchor='e',justify='right',borderwidth=2) 
l2 = tk.Label(root,text="",font=('Aptos',15),fg="#3d3c40",anchor='e',justify='right',borderwidth=2) 

#function for check limit:
def limit():
    global exp
    if len(exp)<=15:
        return True
    else:
        msg.showerror("Error","You have exceeded maximum limit")

#Input Functions:
exp = ""
ans = None

#function for number input:
def num_in(n):
    global exp,ans
    if limit():
        """modification of label 1"""
        exp += n
        l1.config(text=exp)

        """modification of label 2"""
        try:
            float(exp)
        except ValueError:
            try:
                ans = eval(exp)
            except SyntaxError:
                br1 = exp.count('(')
                br2 = exp.count(')')
                temp = exp + ')'*(br1-br2)
                a = eval(temp)
                l2.config(text=str(round(float(a),5)))
            except ZeroDivisionError:
                l2.config(text="")
            else:
                l2.config(text=str(round(float(ans),5)))
        else:
            l2.config(text="")

#function for operator input:
def op_in(sym):
    global exp,ans
    if limit():
        """modification of label 1"""
        if exp:
            if exp[-1] not in ['+','-','*','/',]:
                exp += sym
            else:
                exp = exp[:-1] + sym
        l1.config(text=exp)

        """modification of label 2"""
        l2.config(text="")

#function for decimal input:
def decimal():
    global exp,ans
    if limit():
        """modification of label 1"""
        if not exp or exp[-1] in ['+','-','*','/','(']:  # If empty or last char is operator, start new number with "0."
            exp += '0.'
        else:
            i = len(exp) - 1
            while i >= 0 and exp[i] not in ['+','-','*','/','(']: i -= 1 # Find the last number segment
            segment = exp[i+1:]
            if '.' not in segment:
                exp += '.'  # Only add '.' if this segment doesn't already contain one
        l1.config(text=exp)

        """modification of label 2"""
        try:
            ans = eval(exp)
        except (SyntaxError, ZeroDivisionError):
            l2.config(text="")
            return
        # show preview ONLY if expression contains an operator
        if any(op in exp for op in ['+','-','*','/']):
            l2.config(text=str(round(float(ans), 5)))
        else:
            l2.config(text="")
        
#function for bracket open:
def bracket_open():
    global exp
    if limit():
        """modification of label 1"""
        if not exp or exp[-1] in ['+','-','*','/','(']:
            exp += '('
        else:
            exp +='*('
        l1.config(text=exp)

        """modification of label 2"""
        l2.config(text="")

#function for bracket close:
def bracket_close():
    global exp
    if limit():
        """modification of label 1"""
        if exp:
            br1 = exp.count('(')
            br2 = exp.count(')')

            if br1>br2 and exp[-1] not in ['+','-','*','/','(']:
                exp += ')'
        l1.config(text=exp)

        """no modification for label 2"""

#function for percent:
def percent():
    global exp, ans
    if limit():
        if not exp or exp[-1] in ['+','-','*','/','(','%']:
            return

        # find last operator
        i = len(exp) - 1
        while i >= 0 and exp[i] not in ['+','-','*','/']:
            i -= 1

        try:
            if i == -1:
                # only a number → 50% = 50/100
                temp = f"({exp})/100"
            else:
                left = exp[:i]
                op = exp[i]
                right = exp[i+1:]

                if op in ['+','-']:
                    # A + B% = A + (A * B / 100)
                    temp = f"{left}{op}(({left})*({right})/100)"
                else:
                    # A * B% = A * (B / 100)
                    temp = f"{left}{op}(({right})/100)"

            ans = eval(temp)

        except (SyntaxError, ZeroDivisionError):
            l2.config(text="")
        else:
            exp += '%'
            l1.config(text=exp)
            l2.config(text=str(round(float(ans), 5)))

#function for backspace:
def back_space():
    global exp, ans

    """modification of label 1"""
    exp = exp[:-1]
    l1.config(text=exp)

    """modification of label 2"""
    if not exp or exp[-1] in ['+','-','*','/','(']:
        l2.config(text="")
    else:
        try:
            float(exp)
        except ValueError:
            try:
                ans = eval(exp)
            except SyntaxError:
                br1 = exp.count('(')
                br2 = exp.count(')')
                temp = exp + ')'*(br1-br2)
                a = eval(temp)
                l2.config(text=str(round(float(a),5)))
            except ZeroDivisionError:
                l2.config(text="")
            else:
                l2.config(text=str(round(float(ans),5)))

#function for clear all:
def clear():
    global exp

    """modification of label 1"""
    exp=""
    l1.config(text=exp)

    """modification of label 2"""
    l2.config(text="")
    
#Output Function:
def answer():
    global exp,ans

    """modification of label 1"""
    try:
        exp = exp.replace('%', '/100')
        ans = eval(exp)
    except SyntaxError:
        msg.showerror("Error","Syntax Error!")
        br1 = exp.count('(')
        br2 = exp.count(')')
        if br1>br2:
            msg.showwarning("Warning","'(' was never closed")
        elif br1<br2:
            msg.showwarning("Warning","')' was never opened")
        return
    except ZeroDivisionError:
        msg.showerror("Error","Cannot divide by Zero")
        return
    exp = str(ans)
    l1.config(text=exp)

    """modification of label 2"""
    l2.config(text="")

#number buttons
b0 = tk.Button(root,text='0',padx=6,pady=2,font=15,width=4,bg='white',command=lambda: num_in('0'))
b1 = tk.Button(root,text='1',padx=6,pady=2,font=15,width=4,bg='white',command=lambda: num_in('1'))
b2 = tk.Button(root,text='2',padx=6,pady=2,font=15,width=4,bg='white',command=lambda: num_in('2'))
b3 = tk.Button(root,text='3',padx=6,pady=2,font=15,width=4,bg='white',command=lambda: num_in('3'))
b4 = tk.Button(root,text='4',padx=6,pady=2,font=15,width=4,bg='white',command=lambda: num_in('4'))
b5 = tk.Button(root,text='5',padx=6,pady=2,font=15,width=4,bg='white',command=lambda: num_in('5'))
b6 = tk.Button(root,text='6',padx=6,pady=2,font=15,width=4,bg='white',command=lambda: num_in('6'))
b7 = tk.Button(root,text='7',padx=6,pady=2,font=15,width=4,bg='white',command=lambda: num_in('7'))
b8 = tk.Button(root,text='8',padx=6,pady=2,font=15,width=4,bg='white',command=lambda: num_in('8'))
b9 = tk.Button(root,text='9',padx=6,pady=2,font=15,width=4,bg='white',command=lambda: num_in('9'))

#symbol buttons
dot = tk.Button(root,text='.',padx=6,pady=2,font=15,width=4,bg='#bdbdbf',command=decimal)

plus = tk.Button(root,text='+',padx=6,pady=2,font=15,width=4,bg='#bdbdbf',command=lambda: op_in('+'))
minus = tk.Button(root,text='-',padx=6,pady=2,font=15,width=4,bg='#bdbdbf',command=lambda: op_in('-'))
mul = tk.Button(root,text='*',padx=6,pady=2,font=15,width=4,bg='#bdbdbf',command=lambda: op_in('*'))
div = tk.Button(root,text='/',padx=6,pady=2,font=15,width=4,bg='#bdbdbf',command=lambda: op_in('/'))

per = tk.Button(root,text='%',padx=6,pady=2,font=15,width=4,bg='#bdbdbf',command=percent)

eq = tk.Button(root,text='=',padx=6,pady=2,font=15,width=4,bg='#4865f7',fg='white',command=answer) 

open_bracket = tk.Button(root,text='(',pady=2,font=15,width=2,bg='#bdbdbf',command=bracket_open)
close_bracket = tk.Button(root,text=')',pady=2,font=15,width=2,bg='#bdbdbf',command=bracket_close)

bksp = tk.Button(root,text='DEL',padx=6,pady=2,font=1,width=4,bg='#cf5f70',fg='white',command=back_space)
clr = tk.Button(root,text='AC',padx=6,pady=2,font=1,width=4,bg='#cf5f70',fg='white',command=clear)

#placing widgets
l1.grid(row=0,columnspan=5,sticky='e')

l2.grid(row=1,columnspan=5,sticky='e')

per.grid(row=2,column=0)
open_bracket.grid(row=2,column=1)
close_bracket.grid(row=2,column=2)
clr.grid(row=2,column=3)
bksp.grid(row=2,column=4)

b7.grid(row=3,column=0)
b8.grid(row=3,column=1,columnspan=2)
b9.grid(row=3,column=3)
div.grid(row=3,column=4)

b4.grid(row=4,column=0)
b5.grid(row=4,column=1,columnspan=2)
b6.grid(row=4,column=3)
mul.grid(row=4,column=4)

b1.grid(row=5,column=0)
b2.grid(row=5,column=1,columnspan=2)
b3.grid(row=5,column=3)
minus.grid(row=5,column=4)

dot.grid(row=6,column=0)
b0.grid(row=6,column=1,columnspan=2)
eq.grid(row=6,column=3)
plus.grid(row=6,column=4)

root.mainloop()