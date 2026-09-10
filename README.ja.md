# Koi StyleKit

[简体中文](README.md) | [English](README.en.md) | **日本語** | [한국어](README.ko.md)

Koi StyleKit は、手描きイラストのスタイルを探し、再利用できるプロンプトレシピを書き出すオープンソースのローカルツールです。

## できること

- 48 のスタイルファミリー、300 以上のレシピを検索・絞り込み・比較
- サンプル画像と検証状態を確認
- 中国語プロンプトと JSON スタイルパッケージをエクスポート
- Python CLI またはローカル Web ギャラリーで利用

```sh
git clone https://github.com/koi-lee/koi-stylekit.git
cd koi-stylekit
python3 scripts/serve.py
```

ブラウザで `http://127.0.0.1:4317/` を開いてください。画像生成 API は呼び出さず、テーマは外部へ送信しません。

サンプル画像は単一テーマの候補であり、別テーマや別モデルでの再現を保証しません。詳細は [README.md](README.md) と [機械可読概要](wireframes/llms.txt) を参照してください。

