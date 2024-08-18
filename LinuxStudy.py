import tkinter as tk
from tkinter import messagebox, simpledialog


commands = {
    "ls": {
            "description": "ディレクトリの内容を一覧表示します",
            "options": {
                "-l": "長い形式でリストします",
                "-a": "隠しファイルも表示します",
                "-h": "人間が読みやすい形式でサイズを表示します"
            },
            "example": "ls -l",
            "additional_info": "例: 'ls -a' は隠しファイルを含む全てのファイルを表示します。"
        },
    "pwd": {
            "description": "現在の作業ディレクトリを表示します",
            "options": {},
            "example": "pwd",
            "additional_info": "例: 'pwd' は現在のディレクトリのパスを表示します。"
        },
    "cd": {
            "description": "ディレクトリを変更します",
            "options": {},
            "example": "cd /home/user",
            "additional_info": "例: 'cd ..' は親ディレクトリに移動します。"
        },
    "mkdir": {
            "description": "ディレクトリを作成します",
            "options": {
                "-p": "親ディレクトリも一緒に作成します"
            },
            "example": "mkdir new_folder",
            "additional_info": "例: 'mkdir -p /new/dir' は親ディレクトリも一緒に作成します。"
        },
    "rmdir": {
            "description": "ディレクトリを削除します",
            "options": {},
            "example": "rmdir old_folder",
            "additional_info": "例: 'rmdir /dir' は空のディレクトリを削除します。"
        },
    "cp": {
          "description": "ファイルやディレクトリをコピーします",
            "options": {
                "-r": "ディレクトリを再帰的にコピーします",
                "-i": "上書きする前に確認します",
                "-v": "コピーの詳細を表示します"
            },
            "example": "cp file1.txt file2.txt",
            "additional_info": "例: 'cp -r dir1 dir2' はディレクトリを再帰的にコピーします。"
        },
    "mv": {
            "description": "ファイルやディレクトリを移動/名前変更します",
            "options": {
                "-i": "上書きする前に確認します",
                "-v": "移動の詳細を表示します"
            },
            "example": "mv oldname.txt newname.txt",
            "additional_info": "例: 'mv file.txt /new/location/' はファイルを新しい場所に移動します。"
        },
    "rm": {
            "description": "ファイルやディレクトリを削除します",
            "options": {
                "-r": "ディレクトリを再帰的に削除します",
                "-f": "確認せずに強制的に削除します",
                "-i": "削除する前に確認します"
            },
            "example": "rm file.txt",
            "additional_info": "例: 'rm -rf /dir' はディレクトリとその内容を強制的に削除します。"
        },
    "touch": {
            "description": "ファイルのタイムスタンプを変更します",
            "options": {},
            "example": "touch newfile.txt",
            "additional_info": "例: 'touch file.txt' はファイルのタイムスタンプを現在の時間に更新します。"
        },
        "chmod": {
            "description": "ファイルのモードやアクセス制御リストを変更します",
            "options": {
                "-R": "ディレクトリを再帰的に変更します",
                "-v": "変更の詳細を表示します"
            },
            "example": "chmod 755 script.sh",
            "additional_info": "例: 'chmod -R 755 /dir' はディレクトリとその内容の権限を変更します。"
        },
    "grep": {
            "description": "パターンに一致する行を表示します",
            "options": {
                "-i": "大文字と小文字を区別しません",
                "-v": "一致しない行を表示します",
                "-r": "ディレクトリを再帰的に検索します"
            },
            "example": "grep 'pattern' file.txt",
            "additional_info": "例: 'grep -r 'pattern' /dir' はディレクトリ内の全てのファイルを検索します。"
        },
    "awk": {
            "description": "パターンのスキャンと処理言語",
            "options": {},
            "example": "awk '{print $1}' file.txt",
            "additional_info": "例: 'awk '{print $1, $3}' file.txt' はファイルの1列目と3列目を表示します。"
        },
    "sed": {
            "description": "ストリームエディタ",
            "options": {
                "-e": "スクリプトを指定します",
                "-i": "ファイルを直接編集します"
            },
            "example": "sed 's/old/new/g' file.txt",
            "additional_info": "例: 'sed -i 's/old/new/g' file.txt' はファイル内の全ての 'old' を 'new' に置換します。"
        },
    "find": {
            "description": "ディレクトリ階層内のファイルを検索します",
            "options": {
                "-name": "名前で検索します",
                "-type": "ファイルの種類で検索します"
            },
            "example": "find /home -name '*.txt'",
            "additional_info": "例: 'find /dir -type f -name '*.txt'' はディレクトリ内の全てのテキストファイルを検索します。"
        },
    "xargs": {
            "description": "標準入力からコマンドラインを構築して実行します",
            "options": {
                "-0": "ヌル文字で区切られた入力を処理します",
                "-I": "置換文字列を指定します"
            },
            "example": "find . -name '*.txt' | xargs rm",
            "additional_info": "例: 'find . -name '*.txt' | xargs -I {} mv {} /new/location/' は全てのテキストファイルを新しい場所に移動します。"
        }
    }

completed_commands = []

def show_command_info(command, info):
    def on_close():
        practice_window.destroy()

    def modify_command():
        description = simpledialog.askstring("説明", f"{command} の新しい説明を入力してください:", initialvalue=info["description"])
        example = simpledialog.askstring("例", f"{command} の新しい例を入力してください:", initialvalue=info["example"])
        additional_info = simpledialog.askstring("追加情報", f"{command} の新しい追加情報を入力してください:", initialvalue=info["additional_info"])
        options = {}
        while True:
            option = simpledialog.askstring("オプション", "新しいオプションを入力してください（終了するには空白のままにしてください）:")
            if not option:
                break
            option_desc = simpledialog.askstring("オプション説明", f"{option} の説明を入力してください:")
            options[option] = option_desc

        commands[command] = {
            "description": description,
            "options": options,
            "example": example,
            "additional_info": additional_info
        }
        practice_window.destroy()
        refresh_commands()

    def delete_command():
        del commands[command]
        practice_window.destroy()
        refresh_commands()

    practice_window = tk.Toplevel(root)
    practice_window.title(f"Practice Command: {command}")
    practice_window.geometry("500x500")
    
    label = tk.Label(practice_window, text=f"{command}: {info['description']}", font=("Arial", current_font_size))
    label.pack(pady=10)
    
    options_label = tk.Label(practice_window, text="オプション:", font=("Arial", current_font_size))
    options_label.pack(pady=5)
    
    for opt, desc in info['options'].items():
        opt_label = tk.Label(practice_window, text=f"{opt}: {desc}", font=("Arial", current_font_size))
        opt_label.pack(pady=2)
    
    example_label = tk.Label(practice_window, text=f"例: {info['example']}", font=("Arial", current_font_size))
    example_label.pack(pady=5)
    
    additional_info_label = tk.Label(practice_window, text=f"追加情報: {info['additional_info']}", font=("Arial", current_font_size))
    additional_info_label.pack(pady=5)
    
    button_frame = tk.Frame(practice_window)
    button_frame.pack(pady=10)
    
    modify_button = tk.Button(button_frame, text="修正", command=modify_command, font=("Arial", current_font_size))
    modify_button.pack(side="left", padx=5)
    
    delete_button = tk.Button(button_frame, text="削除", command=delete_command, font=("Arial", current_font_size))
    delete_button.pack(side="left", padx=5)
    
    close_button = tk.Button(practice_window, text="閉じる", command=on_close, font=("Arial", current_font_size))
    close_button.pack(pady=10)
    
    # Adjust window size based on font size
    practice_window.update_idletasks()
    width = practice_window.winfo_width()
    height = practice_window.winfo_height()
    practice_window.geometry(f"{int(width * (current_font_size / 18))}x{int(height * (current_font_size / 18))}")

def add_command():
    command = simpledialog.askstring("コマンド名", "追加するコマンド名を入力してください:")
    if not command:
        return
    
    description = simpledialog.askstring("説明", f"{command} の説明を入力してください:")
    if not description:
        return
    
    example = simpledialog.askstring("例", f"{command} の例を入力してください:")
    if not example:
        return
    
    additional_info = simpledialog.askstring("追加情報", f"{command} の追加情報を入力してください:")
    if not additional_info:
        return
    
    options = {}
    while True:
        option = simpledialog.askstring("オプション", "オプションを入力してください（終了するには空白のままにしてください）:")
        if not option:
            break
        option_desc = simpledialog.askstring("オプション説明", f"{option} の説明を入力してください:")
        if not option_desc:
            return
        options[option] = option_desc

    commands[command] = {
        "description": description,
        "options": options,
        "example": example,
        "additional_info": additional_info
    }
    refresh_commands()

root = tk.Tk()
root.title("Linux Command Practice")
root.geometry("1150x300")

current_font_size = 18

def set_font_size(size):
    global current_font_size
    current_font_size = int(size)
    refresh_ui_font(root)
    refresh_commands()

def refresh_ui_font(widget):
    if isinstance(widget, (tk.Label, tk.Button, tk.Text)):
        widget.configure(font=("Arial", current_font_size))
    for child in widget.winfo_children():
        refresh_ui_font(child)

def refresh_commands():
    for widget in command_frame.winfo_children():
        widget.destroy()
    create_command_buttons()

def create_command_buttons():
    for cmd, info in commands.items():
        label = tk.Button(command_frame, text=cmd, command=lambda c=cmd, i=info: show_command_info(c, i), font=("Arial", current_font_size))
        label.pack(side="left", padx=5, pady=5)

font_size_label = tk.Label(root, text="フォントサイズ", font=("Arial", current_font_size))
font_size_label.pack(pady=5)

font_size_slider = tk.Scale(root, from_=8, to=50, orient="horizontal", command=lambda size: set_font_size(int(size)))
font_size_slider.set(current_font_size)
font_size_slider.pack(pady=5)

add_command_button = tk.Button(root, text="コマンド追加", command=add_command, font=("Arial", current_font_size))
add_command_button.pack(pady=10)

command_frame = tk.Frame(root)
command_frame.pack(fill="both", expand="yes", padx=10, pady=5)

create_command_buttons()

root.mainloop()
