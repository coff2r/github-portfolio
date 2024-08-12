# クライアントの技術的分析

1. 言語 オプション 辞書
- ユーザーが選択した言語に応じて適切なメッセージを表示できるように、メッセージを言語別に整理します。
<pre>
  <code>
    # 言語オプション辞書
languages = {
    'en': {
        'commands': '>> Commands <<',
        'server_list': '>> Available Servers <<',
        'select_server': 'Select a server by number: ',
        'invalid_choice': 'Invalid choice. Exiting.',
        'enter_id': 'Enter your user ID: ',
        'connection_failed': 'Failed to connect to the server. Please check the host and port.',
        'connected': '>> Connected to Server',
        'now_disconnected': '>>now disconnected',
        'current_time': '>>> {} <<<',
        'help_list': '1. "/hl" or "/helplist" = Show Commands List\n2. "/ul" or "/userlist" = Show Connected User List\n3. "/ct" or "/currenttime" = Show Current Day and Time\n4. "/l" or "/lang" = Change language\n ex) /l(/lang) ko : Korean, /l(lang) en : English, /l(lang) jp : Japanese\n5. "/q" or "/quit" = Quit Client',
        'language_changed': 'Language changed to {}.',
        'unsupported_language': 'It starts with English, which is the default language, because there is no optional language.'
    },
    'jp': {
        'commands': '>> コマンド <<',
        'server_list': '>> 利用可能なサーバー <<',
        'select_server': '番号でサーバーを選択: ',
        'invalid_choice': '無効な選択です。終了します。',
        'enter_id': 'ユーザーIDを入力してください: ',
        'connection_failed': 'サーバーへの接続に失敗しました。ホストとポートを確認してください。',
        'connected': '>> サーバーに接続しました',
        'now_disconnected': '>> 切断しました',
        'current_time': '>>> {} <<<',
        'help_list': '1. "/hl" または "/helplist" = コマンドリストを表示\n2. "/ul" または "/userlist" = 接続ユーザーリストを表示\n3. "/ct" または "/currenttime" = 現在の日付と時間を表示\n4. "/l" または "/lang" = 言語変更\n ex) /l(/lang) ja : 韓国語 , /l(lang) en : 英語 , /l(lang) jp : 日本語\n5. "/q" または "/quit" = クライアントを終了',
        'language_changed': '言語が {} に変更されました。',
        'unsupported_language': '選択言語がないため、デフォルトの言語である英語で開始します。'
    },
    'kr': {
        'commands': '>> 명령어 <<',
        'server_list': '>> 사용 가능한 서버 <<',
        'select_server': '번호로 서버를 선택하세요: ',
        'invalid_choice': '잘못된 선택입니다. 종료합니다.',
        'enter_id': '사용자 ID를 입력하세요: ',
        'connection_failed': '서버에 연결할 수 없습니다. 호스트와 포트를 확인하세요.',
        'connected': '>> 서버에 연결되었습니다',
        'now_disconnected': '>> 연결 종료됨',
        'current_time': '>>> {} <<<',
        'help_list': '1. "/hl" 또는 "/helplist" = 명령어 목록 보기\n2. "/ul" 또는 "/userlist" = 연결된 사용자 목록 보기\n3. "/ct" 또는 "/currenttime" = 현재 날짜와 시간 보기\n4. "/l" 또는 "/lang" = 언어 변경\n    ex) /l(/lang) ko : 한국어 , /l(lang) en : 영어 , /l(lang) jp : 일본어\n5. "/q" 또는 "/quit" = 클라이언트 종료',
        'language_changed': '언어가 {}(으)로 변경되었습니다.',
        'unsupported_language': '선택 언어가 없기 때문에 기본 언어인 영어로 시작합니다.'
    }
}
  </code>
</pre>

2. 言語設定の変更
- インターフェイスは、ユーザーの言語選択に応じて切り替えられ、異なる言語環境でアプリケーションを使用できます。
<pre>
  <code>
    # C現在の言語設定
current_language = 'en'

# 言語を変更する機能
def set_language(language_code):
    global current_language
    if language_code in languages:
        current_language = language_code
        print(get_text('language_changed', language_code))
    else:
        print(get_text('unsupported_language', language_code))
  </code>
</pre>

3. テキスト受信
- テキストを受信する他の言語に関する他のメッセージを簡単に検索して、再利用することができます。
<pre>
  <code>
    # 現在の言語に基づいてテキストを取得する
def get_text(key, *args):
    text = languages[current_language].get(key, key)
    if args:
        text = text.format(*args)
    return text
  </code>
</pre>

4. 現在の時刻、日付、日付、および時刻の取得
- 現在の時刻、日付、または両方を、形式が指定された文字列で返します。
<pre>
  <code>
    # 時間の機能
def now_time():
    now = datetime.datetime.now()
    return now.strftime('[%H:%M] ')
# 日付の機能 
def now_date():
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d')
# 時間と日付の機能 
def now_datetime():
    now = datetime.datetime.now()
    return now.strftime(' [%Y-%m-%d %H:%M] ')
  </code>
</pre>

5. 命令リスト
<pre>
  <code>
    # コマンド管理
# languages言語オプション辞書のhelp_listを呼び出して表示する
def helplist():
    print(get_text('commands'))
    print(get_text('help_list'))
  </code>
</pre>

6. サーバーリスト('show_serverlist)の確認と選択
- 連結できるサーバーリストを表示して使用者がサーバを選択できるようにします。
<pre>
  <code>
    # サーバーのリスト
servers = [
    # サーバーで定義されたサーバーHOSTとPORTをリスト化
    {'host': '127.0.0.1', 'port': 3000},
    {'host': '127.0.0.1', 'port': 3001},
    {'host': '127.0.0.1', 'port': 3002},
    {'host': '127.0.0.1', 'port': 3003},
    {'host': '127.0.0.1', 'port': 3004},
]

# サーバーリストを表示
def show_serverlist():
    print(get_text('server_list'))
    for i, server in enumerate(servers):
        print(f"{i + 1}. Host: {server['host']}, Port: {server['port']}")

# サーバーを選択
def selectserver():
    show_serverlist()
    choice = int(input(get_text('select_server'))) - 1
    if 0 <= choice < len(servers):
        return servers[choice]
    else:
        print(get_text('invalid_choice'))
        exit()
  </code>
</pre>

7. 言語選択
- アプリケーションの起動時に使用する言語をユーザーが選択できます。
<pre>
  <code>
    # 初期言語の選択
def select_language():
    print("Available languages: en (English), jp (Japanese), kr (Korean)")
    language_code = input('Select your language by entering the language code: (basic language is english)')
    set_language(language_code)

# 開始時の言語選択
select_language()
  </code>
</pre>

8. サーバー接続
- サーバー接続時にIPとポート番号を選択、ユーザーIDを入力
<pre>
  <code>
    # サーバーとユーザーIDの選択
server = selectserver()
HOST = server['host']
PORT = server['port']

# ユーザーidを入力
user_id = input(get_text('enter_id'))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect((HOST, PORT))
except ConnectionRefusedError:
    print(get_text('connection_failed'))
    exit()

client_socket.send(f"ID:[{user_id}]".encode())

def receive_message(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            # Display the received data
            print(data)
        except ConnectionResetError:
            print(get_text('connection_failed'))
            break
    client_socket.close()
  </code>
</pre>

9. メイン·ルート
- ユーザーの入力を受け入れ、サーバーへのメッセージの送信または特定のコマンドの実行に応答します。
- クライアントのソケットを閉じ、サーバーとの接続を閉じます。
<pre>
  <code>
    # 受信メッセージスレッドを開始します
start_new_thread(receive_message, (client_socket,))

print(get_text('connected'), now_datetime())
helplist()

while True:
    message = input('')
    if message == '/q' or message == '/quit':
        print(get_text('now_disconnected'))
        client_socket.send(message.encode())
        break
    elif message == '/ul' or message == '/userlist':
        print("Sending user list request.")
        client_socket.send(message.encode())
    elif message == '/hl' or message == '/helplist':
        helplist()
    elif message == '/ct' or message == '/currenttime':
        print(get_text('current_time', now_datetime()))
    elif message.startswith('/l') or message.startswith('/lang'):
        parts = message.split()
        if len(parts) > 1:
            set_language(parts[1])
        else:
            print(get_text('invalid_choice'))
    else:
        client_socket.send(message.encode())

client_socket.close()

  </code>
</pre>
