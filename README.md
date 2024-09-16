# Coreserver IP Setter

## What

このスクリプトを実行したサーバを踏み台にしてSSHできるようにするため、
Coreserverのサーバ(m39.coreserver.jp)に対して当サーバーのIPアドレスを
SSH接続元として許可するためのAPIを実行します。

## 前提

このスクリプトはCoreserver V1でのみ動作します。

## How to run
`.env` ファイルを作成する必要があります。

```console
$ cp .env.example .env
$ $EDITOR .env
```

コピーした`.env`を次のように設定します。
```env
# もし使っているエディタが環境変数マスキングをサポートしている場合は
# コメントが読めなくなるため、一旦外してください。
CS_USER= # Coreserverでのユーザー名
SERVER= # Coreserverで自分に割り当てられたサーバーの FQDN 例えば、mNN.coreserver.jp NNは数値、mはプランによって変化します
API_KEY= # コントロールパネルから取得したAPI Key
```

> [!CAUTION]
> `.env` ファイルの管理には十分注意を払ってください。

Pyenv (Python) およびPoetryを準備します。

Pyenvについては[公式インストーラ](https://github.com/pyenv/pyenv-installer)を利用することができます。
ここではpyenvコマンドが利用できるところまでセットアップできた前提で説明します。

Pythonのバージョンは3.12以降を指定します。
```console
$ pyenv install --list | grep 3.12
  3.12.0
  3.12-dev
  3.12.1
  3.12.2
  ...
# リストされた 3.12系のPythonの中で最新を覚えておく
$ pyenv install 3.12.2
$ git clone https://github.com/clpsplug/coreserver-ip-setter
$ cd coreserver-ip-setter
$ pyenv local 3.12.2
$ pip install poetry
$ poetry install
```

この状態で、次を実行し:
```console
$ poetry run python main.py
```

`run.log` に以下の文が出力されていれば成功です。
```log
[2024/09/02 00:00:15] Successfully sent API request for SSH permission
```

もし `err.log` に何らかの出力があった場合は `.env` ファイルや、
当サーバから対象Coreserverへの可用性を確認してください。

## NOTE

このスクリプトは、自サーバのIPを取得するために
`https://api.ipify.org` へリクエストを行います。

## 定期実行のために

crontabに登録する際は次のような記述が良いでしょう。 `/path/to/` の部分は環境により変えてください。

> [!IMPORTANT]
> `/path/to` は２箇所あります。1つめはこのコードに辿り着くための `cd` のパスに、
> もう一つは `.pyenv` フォルダに辿り着くためのパスに存在します。

```cron
# m h  dom mon dow   command
0 0 * * 1 cd /path/to/coreserver-ip-setter && /path/to/.pyenv/shims/poetry run python main.py
```

> [!WARNING]
> あまり頻繁にこのスクリプトを実行しないでください。
> 上記のCrontabでは一週間ごと(月曜)に実行されます。
> また、30日ごとにIP許可はリセットされるため、
> それ以上の間隔で実行されないようにご注意ください。