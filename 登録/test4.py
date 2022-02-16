import time
import smtplib, ssl
from email.mime.text import MIMEText
import concurrent.futures
import tkinter as tk
from tkinter import messagebox

#Gmailの設定
gmail_account = 'nabe.tackey@gmail.com'
gmail_password = 'Wtakuki0531'

#メールの送信先
mail_to = 'nabe.tackey@gmail.com'

#メールデータ(MIME)の作成
subject = 'keyword:KIT'
body1 = 'ネットワーク家電と許可されていない端末との通信を確認しました。確認してください'
body2 = 'インターネットからコントローラーに不正操作が確認されました。確認してください'

msg1 = MIMEText(body1, "html")
msg1["Subject"] = subject
msg1["To"] = mail_to
msg1["From"] = gmail_account

msg2 = MIMEText(body2, "html")
msg2["Subject"] = subject
msg2["To"] = mail_to
msg2["From"] = gmail_account

#メインウィンドウを作成
baseGround = tk.Tk()
#ウィンドウサイズを設定
baseGround.geometry('500x300')
#画面タイトル
baseGround.title('確認画面')

#ラベル
label = tk.Label(text = '確認')
label.place(x = 30, y = 40)

#テキストボックス
textBox = tk.Entry(width = 40)
textBox.place(x = 30, y = 60)

#flg1、flg2の初期状態をTrueに設定する
flg1 = True
flg2 = True

#指定したファイルを開く
path1 = 'C:\\Users\\Owner\\Documents\\python_game\\lab\\test4.txt'

#指定したファイルをリスト化する
def list_open():
    with open( path1, encoding = "utf-8_sig" ) as f:
        lines = f.read().split()
        return lines

#.txtの更新
def list_update():
    global path1
    print('リストの更新があるか確認します')
    path2 = 'C:\\Users\\Owner\\Documents\\python_game\\lab\\test4.txt'
    if path2 != path1:
        print('リストの更新があったので行います')
        path1 = path2
    else:
        print('リストの更新はありませんでした')

#異常な通信があるか判定する処理
def send_action():
    global flg1, flg2
    while 1:
        if flg2 == False:
            time.sleep(1)
            list_update()
            print('再開します')
            flg2 = True
        else:
            if ('異常な通信1' in list_open()):
                #Gmailに接続(ポート番号は465)
                server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context = ssl.create_default_context())
                server.login(gmail_account, gmail_password)
                server.send_message(msg1) #メールの送信
                print('ok1.')
                time.sleep(10)
                #テキストボックスに確認しましたと送信したときの処理
                if flg1 == False:
                    print('停止します')
                    time.sleep(19)
                    flg1 = True
                else:
                    pass
            elif('異常な通信2' in list_open()):
                #Gmailに接続(ポート番号は465)
                server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context = ssl.create_default_context())
                server.login(gmail_account, gmail_password)
                server.send_message(msg2) #メールの送信
                print('ok2.')
                time.sleep(10)
                #テキストボックスに確認しましたと送信したときの処理
                if flg1 == False:
                    print('停止します')
                    time.sleep(19)
                    flg1 = True
            else:
                print('攻撃されていません')
                list_update()
                time.sleep(10)
            
#GUIのアクション処理
def stop():
    global flg1,flg2
    if (textBox.get() == '確認しました'):
        flg1 = False
        flg2 = False
        messagebox.showinfo('確認', '1日停止します')
    elif (textBox.get() == ""):
        pass
    else:
        messagebox.showerror('エラー', '指定されたワードではありません')

#ボタンアクション
button = tk.Button(baseGround, text = '送信', command = stop).place(x = 30, y = 180)

#マルチスレッド処理
if __name__ == "__main__":
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    executor.submit(send_action)
    executor.submit(stop)

#ウィンドウを表示する
baseGround.mainloop()