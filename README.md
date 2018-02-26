# これ何？
LightFieldRenderingの基本的な実装をしたサンプルプログラム。

# 使い方
cloneした後に必要なPythonのパッケージをインストールした後に`lightfield.py`を実行すると`./dst/` ディレクトリ以下に出力後の画像が出てきます。`JPEG Images`はブラウザ閲覧用の画質劣化版、`Original Images`はオリジナル画質版です。

# プログラムの中で変更するパラメータ

## lightfield.py
`src_folder_path` ソース画像のパス
`x_amount, y_amount` 横方向、縦方向の画像の枚数