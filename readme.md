# acbDecrypter

このツールはacbファイルをwav変換するツールです。

このツールはID: f70CrkXN さんの
AFS2(.awb)CPK(.cpk)展開ツール v1.40 と
HCAデコーダ v1.21 の機能をラップしたものです。
基幹機能は f70CrkXN さんによるものですので感謝を...


## usage

acbファイルか、awbファイルをD&Dもしくはexe起動後パス入力で自動でwav変換します。
wavファイルは、acbファイルと同階層にacbファイルの名前から拡張子を取った名前のフォルダを作成しその中に保存します。
処理終了後自動で開くのでわかると思います。


exeと同階層のacbToHcaにはAFS2(.awb)CPK(.cpk)展開ツール v1.40
同じくhcaToWavにはHCAデコーダ v1.21が入っています。ただし、hcaToWav内の復号化.batについては都合により一部編集しています。
adxToWavにはADXデコーダ v1.31が入っています。ただし都合により特殊鍵指定デコード.bat、復号鍵指定デコード.batを追加しています。


鍵リストは、exeと同階層のhcaToWavフォルダ内の復号鍵リスト.txtを参照しています。
鍵、空白、コロン、空白、タイトル
の形式で追記すれば後からでも追加可能です。

※このツールによって生じたいかなる損害も作者は負いませんので自己責任でお願いします。

## update

0.2.2
HCAデコーダのアップデート

0.2.1
いくつかの微細なアップデート

0.2.0
ADXデコーダのアップデート、ADX復号の安定性の向上、ADX鍵選択のGUI化、ADXファイルのみ選択したときにHCA鍵選択ダイアログが出ないよう変更。
鍵選択ダイアログは各フォーマットのファイルが初めて見つかったときにでます。
また、上記変更に伴い内部の構造を大幅に変更
ADXの復号には、現状特殊鍵を用いる方法のみ対応。復号鍵を用いる方法は対応予定。

0.1.3b
ADXデコーダの取り込み。ADXファイルの解析に対応（仮）
ADXファイルが見つかると、DOS窓で別途鍵を聞いてくるので入力してください。ADXファイルのみを選択したときもhca用鍵を選択するダイアログが出てきますが利用されません。改善検討中。
ADX復号は不安定のため固まることがあります。
ADXは正常に復号できた例がないので
現状は安定版0.1.2の利用を推奨。
また、上記変更に伴い見にくかったコードを小分けにして関数にしました。
受付、自動検出のファイル名を.acb.txtなどからacb.txtなどへ変更しました。これはららマジの仕様に対応するためです。

0.1.2
はじめに見つかったacbファイルの中のhcaファイルを解析し、鍵が必要なければ鍵選択ダイアログを表示しないように変更

0.1.1
鍵を使わないボタンを追加
acbToHcaとhcaToWavフォルダ内から必須でないファイルを幾つか削除
処理終了後のエクスプローラ表示を再開

0.1.0
手入力だったファイル選択をGUI化
フォルダ選択の選択肢を追加
複数に分かれている音楽ファイルの自動結合機能を追加（バンドリのみ）
ソフトが落ちないようにした0.0.4の修正に関して修正漏れを修正
処理の経過がわかるようにプログレスバーを追加
DOS窓の表示数の軽減

0.0.4
手入力でパスを入力した際、パスに空白が含まれていると正常に動作しない不具合修正
wavファイルの元名取得に失敗した際リネームを取りやめ、ソフトが落ちないように修正

0.0.3
wavファイルの名前を元の名前にリネームできるよう変更（安定して稼働できるかは要検証）

0.0.2
一度に複数のファイルの変換に対応
注意:1ファイル完了ごとにwav保存先フォルダがエクスプローラで開くのであまりたくさん一気にやるとエクスプローラだらけになります。
