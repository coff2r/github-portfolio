import socket
import datetime
import threading

# 定義された言語メッセージ 言語別メッセージ 
messages = {
    'en': {
        'welcome': "Welcome",
        'connected': "User : {user_id} connected.",
        'disconnected': "User : {user_id} disconnected.",
        'list': "Connected users : ",
        'start': "Server started on IP : {host} / PORT :{port}",
        'listening': "Listening for connections...",
        'select': "Select servers to start (enter numbers separated by commas): ",
        'starting': "Starting server at IP: {host}, PORT: {port}",
        'invalid_choice': "Invalid choice: {index}",
        'enter_valid': "Please enter valid numbers.",
        'exit_cmd': '/q or /quit',
        'list_cmd': '/ul or /userlist',
        'language_prompt': 'Choose your language: "en" for English, "jp" for Japanese, "kr" for Korean \n'
    },
    'jp': {
        'welcome': "ようこそ",
        'connected': "ユーザー : {user_id} が接続しました。",
        'disconnected': "ユーザー : {user_id} が切断しました。",
        'list': "接続中のユーザー : ",
        'start': "サーバーが IP : {host} / ポート :{port} で起動しました。",
        'listening': "接続を待っています...",
        'select': "起動するサーバーを選択してください (番号をカンマで区切って入力): ",
        'starting': "IP: {host}, ポート: {port} でサーバーを起動します。",
        'invalid_choice': "無効な選択: {index}",
        'enter_valid': "有効な番号を入力してください。",
        'exit_cmd': '/q or /quit',
        'list_cmd': '/ul or /userlist',
        'language_prompt': '言語を選択してください: "en" は英語, "jp" は日本語, "kr" は韓国語"\n'
    },
    'kr': {
        'welcome': "환영합니다",
        'connected': "사용자 : {user_id} 가 연결되었습니다.",
        'disconnected': "사용자 : {user_id} 가 연결이 끊어졌습니다.",
        'list': "연결된 사용자 : ",
        'start': "서버가 IP : {host} / 포트 :{port} 에서 시작되었습니다.",
        'listening': "연결을 기다리고 있습니다...",
        'select': "시작할 서버를 선택하세요 (번호를 쉼표로 구분하여 입력): ",
        'starting': "IP: {host}, 포트: {port} 에서 서버를 시작합니다.",
        'invalid_choice': "잘못된 선택: {index}",
        'enter_valid': "유효한 번호를 입력하세요.",
        'exit_cmd': '/q or /quit',
        'list_cmd': '/ul or /userlist',
        'language_prompt': '언어를 선택하세요: "en"은 영어, "jp"는 일본어, "kr"는 한국어\n'
    }
}

clients = []  # すべてのクライアントソケットを保存するリスト 
users_id = {}  # クライアントソケットのユーザーIDの保存

def handle_client(client_socket, user_messages):
    global clients, users_id

    # Debugging information
    print("Client connected:", client_socket)

    # ユーザーIDの受信
    user_id = client_socket.recv(1024).decode()
    user_id = user_id.split(":")[1]
    users_id[client_socket] = user_id

    # 接続時のユーザーIDと接続時間表示
    print(">>>", user_messages['connected'].format(user_id=user_id), now_datetime())

    while True:
        try:
            message = client_socket.recv(1024).decode()

            if not message:
                break
            if message == user_messages['exit_cmd']:
                break
            if message == user_messages['list_cmd']:
                update_userlist(requesting_client=client_socket, user_messages=user_messages)
            else:
                for client in clients:
                    if client != client_socket:
                        client.send(f"{user_id}: {message}".encode())
        except ConnectionResetError:
            break

    # クライアント接続終了処理
    client_socket.close()
    clients.remove(client_socket)
    del users_id[client_socket]
    print(">>>", now_datetime(), user_messages['disconnected'].format(user_id=user_id))
    update_userlist(user_messages=user_messages)  # 言語別のメッセージ配信



# 接続クライアントの数を管理
def update_userlist(requesting_client=None, user_messages=None):
    global clients, users_id
    userlist_message = user_messages['list']
    if users_id:
        userlist_message += ' '.join(users_id.values())
    else:
        userlist_message += 'No users connected.'

    if requesting_client:
        # Send the user list to the requesting client
        requesting_client.send(userlist_message.encode())
    else:
        # Broadcast the user list to all clients
        for client in clients:
            client.send(userlist_message.encode())


def now_datetime():
    now = datetime.datetime.now()
    datetime_str = now.strftime('[%Y-%m-%d %H:%M] ')
    return datetime_str

def server(host, port, user_messages):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f'>> {user_messages["start"].format(host=host, port=port)}', now_datetime())
    print(user_messages["listening"])

    while True:
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket, user_messages)).start()

def start_servers():
    # サーバー設定
    servers = [
        ('127.0.0.1', 5000),  # サーバーで使用するホストの IP アドレス、PORT 番号
        ('127.0.0.1', 5001),
        ('127.0.0.1', 5002),
        # 他のサーバーアドレスとポートを追加できます。
    ]

    print(messages['en']['select'])
    for index, (host, port) in enumerate(servers):
        print(f"{index + 1}: IP: {host}, PORT: {port}")

    try:
        choices = input(messages['en']['select'])
        selected_indices = [int(choice.strip()) - 1 for choice in choices.split(',') if choice.strip().isdigit()]

        # 言語を選択
        language = input(messages['en']['language_prompt']).strip()
        if language not in messages:
            language = 'en'
        user_messages = messages[language]

        for index in selected_indices:
            if 0 <= index < len(servers):
                host, port = servers[index]
                print(user_messages['starting'].format(host=host, port=port))
                threading.Thread(target=server, args=(host, port, user_messages)).start()
            else:
                print(user_messages['invalid_choice'].format(index=index + 1))
    except ValueError:
        print(messages['en']['enter_valid'])

if __name__ == "__main__":
    start_servers()
