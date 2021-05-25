import pymysql
import tkinter as tk
import tkinter.messagebox


on_hit1 = False
def query_allfoundation():
    #展示所有基金
    global on_hit1
    if on_hit1 == False:
        on_hit1 = True
        window_foundation = tk.Tk()
        window_foundation.title('基金市场')
        window_foundation.geometry('500x300')
        cur = db.cursor()
        sql = "select * from foundation"
        cur.execute(sql)
        results = cur.fetchall()

        lb1 = tk.Listbox(window_foundation)
        lb1.insert('end', 'foundationid')
        for row in results:
            lb1.insert('end', row[0])
        lb1.pack(fill="y", side="left")

        lb2 = tk.Listbox(window_foundation)
        lb2.insert('end', 'foundation')
        for row in results:
            lb2.insert('end', row[1])
        lb2.pack(fill="y", side="left")

        lb3 = tk.Listbox(window_foundation)
        lb3.insert('end', 'price')
        for row in results:
            lb3.insert('end', row[2])  # 从最后一个位置开始加入值
        lb3.pack(fill="y", side="left")
        window_foundation.mainloop()
    else:
        on_hit1 = False

on_hit2 = False
def query_people():
    #查询所有交易记录
    global on_hit2
    if on_hit2 == False:
        on_hit2 = True
        window_all_list = tk.Tk()
        window_all_list.title('交易记录')
        window_all_list.geometry('550x300')
        cur = db.cursor()
        sql = "select * from people"
        cur.execute(sql)
        results = cur.fetchall()

        lb1 = tk.Listbox(window_all_list)
        lb1.insert('end', 'id')
        for row in results:
            lb1.insert('end', row[0])
        lb1.pack(fill="y", side="left")

        lb2 = tk.Listbox(window_all_list)
        lb2.insert('end', 'name')
        for row in results:
            lb2.insert('end', row[1])
        lb2.pack(fill="y", side="left")

        lb3 = tk.Listbox(window_all_list)
        lb3.insert('end', 'foundationid')
        for row in results:
            lb3.insert('end', row[2])
        lb3.pack(fill="y", side="left")

        lb3 = tk.Listbox(window_all_list)
        lb3.insert('end', 'shares')
        for row in results:
            lb3.insert('end', row[3])
        lb3.pack(fill="y", side="left")

        window_all_list.mainloop()
    else:
        on_hit2 = False

on_hit3 = False
def transaction():
    #交易窗口内容
    global on_hit3
    if on_hit3 == False:
        on_hit3 = True
        window_transaction = tk.Tk()
        window_transaction.title('交易窗口')
        window_transaction.geometry('700x300')

        b1 = tk.Button(window_transaction, bg='green', fg='white', text='增加交易', width=15, height=2, command=add_foundation)
        b1.place(x=50, y=100, anchor='nw')
        b2 = tk.Button(window_transaction, bg='green', fg='white', text='删除记录', width=15, height=2, command=delete_foundation)
        b2.place(x=200, y=100, anchor='nw')
        b3 = tk.Button(window_transaction, bg='green', fg='white', text='修改交易', width=15, height=2, command=update_foundation)
        b3.place(x=350, y=100, anchor='nw')
        b4 = tk.Button(window_transaction, bg='green', fg='white', text='搜索交易', width=15, height=2, command=query_foundation)
        b4.place(x=500, y=100, anchor='nw')
        b5 = tk.Button(window_transaction, bg='green', fg='white', text='关闭', width=15, height=2, command=window_transaction.destroy)
        b5.place(x=275, y=200, anchor='nw')

        window_transaction.mainloop()
    else:
        on_hit3 = False

def add_foundation():
    def add():
        name = add_name.get()
        foundationid = add_foundationid.get()
        shares = add_shares.get()
        if(int(foundationid) > l):
            tkinter.messagebox.showinfo(title='消息', message='没有该基金')
            window_add.destroy()
            return

        cur = db.cursor()
        sql = "insert into people (name, foundationid, shares) values (%s, %s, %s);"

        try:
            cur.execute(sql, (name, foundationid, shares))
            db.commit()
            tkinter.messagebox.showinfo(title='消息', message='成功')
            window_add.destroy()
        except Exception as e:
            raise e
            db.rollback()
            tkinter.messagebox.showinfo(title='消息', message='失败')
            window_add.destroy()
        cur.close()

    window_add = tk.Toplevel()
    window_add.geometry('300x200')
    window_add.title('增加窗口')

    add_name = tk.StringVar()
    tk.Label(window_add, text='姓名: ').place(x=10, y=10)
    entry_add_name = tk.Entry(window_add, textvariable=add_name)
    entry_add_name.place(x=130, y=10)

    add_foundationid = tk.StringVar()
    tk.Label(window_add, text='基金编号: ').place(x=10, y=50)
    entry_add_foundationid = tk.Entry(window_add, textvariable=add_foundationid)
    entry_add_foundationid.place(x=130, y=50)

    add_shares = tk.StringVar()
    tk.Label(window_add, text='购买股数: ').place(x=10, y=90)
    entry_add_shares = tk.Entry(window_add, textvariable=add_shares)
    entry_add_shares.place(x=130, y=90)

    btn_comfirm = tk.Button(window_add, text='确认', command=add)
    btn_comfirm.place(x=180, y=120)

    window_add.mainloop()

def delete_foundation():
    def delete():
        name = delete_name.get()
        foundationid = delete_foundationid.get()
        if (int(foundationid) > l):
            tkinter.messagebox.showinfo(title='消息', message='没有该基金')
            window_delete.destroy()
            return

        cur = db.cursor()
        sql = "delete from people where name = %s and foundationid = %s;"
        try:
            cur.execute(sql, (name, foundationid))
            db.commit()
            tkinter.messagebox.showinfo(title='消息', message='成功')
            window_delete.destroy()
        except Exception as e:
            raise e
            db.rollback()
            tkinter.messagebox.showinfo(title='消息', message='失败')
            window_delete.destroy()
        cur.close()

    window_delete = tk.Toplevel()
    window_delete.geometry('300x200')
    window_delete.title('删除窗口')

    delete_name = tk.StringVar()
    tk.Label(window_delete, text='姓名: ').place(x=10, y=10)
    entry_delete_name = tk.Entry(window_delete, textvariable=delete_name)
    entry_delete_name.place(x=130, y=10)

    delete_foundationid = tk.StringVar()
    tk.Label(window_delete, text='基金编号: ').place(x=10, y=50)
    entry_delete_foundationid = tk.Entry(window_delete, textvariable=delete_foundationid)
    entry_delete_foundationid.place(x=130, y=50)

    btn_comfirm = tk.Button(window_delete, text='确认', command=delete)
    btn_comfirm.place(x=180, y=90)

    window_delete.mainloop()

def update_foundation():
    def update():
        name = update_name.get()
        foundationid = update_foundationid.get()
        shares = update_shares.get()
        if (int(foundationid) > l):
            tkinter.messagebox.showinfo(title='消息', message='没有该基金')
            window_update.destroy()
            return
        cur = db.cursor()
        sql = "update people set shares = %s where name = %s and foundationid = %s;"
        try:
            cur.execute(sql, (shares, name, foundationid))
            db.commit()
            tkinter.messagebox.showinfo(title='消息', message='成功')
            window_update.destroy()
        except Exception as e:
            raise e
            db.rollback()
            tkinter.messagebox.showinfo(title='消息', message='失败')
            window_update.destroy()
        cur.close()

    window_update = tk.Toplevel()
    window_update.geometry('300x200')
    window_update.title('修改窗口')

    update_name = tk.StringVar()
    tk.Label(window_update, text='姓名: ').place(x=10, y=10)
    entry_update_name = tk.Entry(window_update, textvariable=update_name)
    entry_update_name.place(x=130, y=10)

    update_foundationid = tk.StringVar()
    tk.Label(window_update, text='基金编号: ').place(x=10, y=50)
    entry_update_foundationid = tk.Entry(window_update, textvariable=update_foundationid)
    entry_update_foundationid.place(x=130, y=50)

    update_shares = tk.StringVar()
    tk.Label(window_update, text='购买股数: ').place(x=10, y=90)
    entry_update_shares = tk.Entry(window_update, textvariable=update_shares)
    entry_update_shares.place(x=130, y=90)

    btn_comfirm = tk.Button(window_update, text='确认', command=update)
    btn_comfirm.place(x=180, y=120)

    window_update.mainloop()

def query_foundation():
    def query_1():
        window_query.destroy()

        name = query_name.get()

        cur = db.cursor()
        sql = "select id, name, foundationid, shares from people where name = %s"
        try:
            cur.execute(sql, (name))
            results = cur.fetchall()

            window_list = tk.Tk()
            window_list.title('交易记录')
            window_list.geometry('550x300')

            lb1 = tk.Listbox(window_list)
            lb1.insert('end', 'id')
            for row in results:
                lb1.insert('end', row[0])
            lb1.pack(fill="y", side="left")

            lb2 = tk.Listbox(window_list)
            lb2.insert('end', 'name')
            for row in results:
                lb2.insert('end', row[1])
            lb2.pack(fill="y", side="left")

            lb3 = tk.Listbox(window_list)
            lb3.insert('end', 'foundationid')
            for row in results:
                lb3.insert('end', row[2])
            lb3.pack(fill="y", side="left")

            lb3 = tk.Listbox(window_list)
            lb3.insert('end', 'shares')
            for row in results:
                lb3.insert('end', row[3])
            lb3.pack(fill="y", side="left")

            window_list.mainloop()

        except Exception as e:
            raise e

    def query_2():
        window_query.destroy()

        foundationid = query_foundationid.get()

        if (int(foundationid) > l):
            tkinter.messagebox.showinfo(title='消息', message='没有该基金')
            return

        cur = db.cursor()
        sql = "select id, name, foundationid, shares from people where foundationid = %s"
        try:
            cur.execute(sql, (foundationid))
            results = cur.fetchall()

            window_list = tk.Tk()
            window_list.title('交易记录')
            window_list.geometry('550x300')

            lb1 = tk.Listbox(window_list)
            lb1.insert('end', 'id')
            for row in results:
                lb1.insert('end', row[0])
            lb1.pack(fill="y", side="left")

            lb2 = tk.Listbox(window_list)
            lb2.insert('end', 'name')
            for row in results:
                lb2.insert('end', row[1])
            lb2.pack(fill="y", side="left")

            lb3 = tk.Listbox(window_list)
            lb3.insert('end', 'foundationid')
            for row in results:
                lb3.insert('end', row[2])
            lb3.pack(fill="y", side="left")

            lb3 = tk.Listbox(window_list)
            lb3.insert('end', 'shares')
            for row in results:
                lb3.insert('end', row[3])
            lb3.pack(fill="y", side="left")

            window_list.mainloop()

        except Exception as e:
            raise e

    window_query = tk.Toplevel()
    window_query.geometry('300x200')
    window_query.title('搜索窗口')

    query_name = tk.StringVar()
    tk.Label(window_query, text='姓名: ').place(x=10, y=10)
    entry_query_name = tk.Entry(window_query, textvariable=query_name)
    entry_query_name.place(x=130, y=10)

    btn_comfirm = tk.Button(window_query, text='按姓名搜索', command=query_1)
    btn_comfirm.place(x=180, y=40)

    query_foundationid = tk.StringVar()
    tk.Label(window_query, text='基金编号: ').place(x=10, y=100)
    entry_query_foundationid = tk.Entry(window_query, textvariable=query_foundationid)
    entry_query_foundationid.place(x=130, y=100)

    btn_comfirm = tk.Button(window_query, text='按编号搜索', command=query_2)
    btn_comfirm.place(x=180, y=140)


l = 0

if __name__ == '__main__':
    db = pymysql.connect(host='localhost', user='root', password='loves81595619ZMY', db='test1', port=3306)

    cur = db.cursor()
    sql = "select * from foundation"
    cur.execute(sql)
    results = cur.fetchall()
    l = len(results)

    mainwindow = tk.Tk()
    mainwindow.title('基金交易系统')
    mainwindow.geometry('500x300')

    b1 = tk.Button(mainwindow, bg='green', fg='white', text='基金市场', width=15, height=2, command=query_allfoundation).pack()
    b2 = tk.Button(mainwindow, bg='green', fg='white', text='交易记录', width=15, height=2, command=query_people).pack()
    b3 = tk.Button(mainwindow, bg='green', fg='white', text='交易', width=15, height=2, command=transaction).pack()
    b4 = tk.Button(mainwindow, bg='green', fg='white', text='关闭', width=15, height=2, command=mainwindow.quit).pack()

    mainwindow.mainloop()

    #tkinter.messagebox.showinfo(title='消息', message='感谢使用')

    db.close()




