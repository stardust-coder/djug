# DJUG 〜ジャグリング × DJ〜

## 概要
ボールジャグリング（玉を複数投げて操る大道芸）をしながら、BGMをアレンジ操作できるようになることを目的とした、画像認識プログラムです。

## 使用方法
### 環境
- MacbookPro Catalina10.15.7
- Python 3.8.2
で動作確認済。

### 使用ライブラリ
- opencv
- pyaudio
- pygame
- wav

### 事前準備
1. musicフォルダに任意の音源ファイルをaudio.wavという名称で保存してください。

### 使用手順
1. 実行すると、Webカメラを検出（デフォルトではMacの内蔵カメラ）し起動します。
2. 同時に音楽が流れ始めます。
3. カメラが黄色い物体の特定の動きに反応して音源を操作します。
    - 高い位置で真左に動かす → テンポが遅くなる 
    - 高い位置で真右に動かす → テンポが速くなる
    - 縦に振る ➡️ スクラッチ音が鳴る

### 想定ユースケース
３色のボールでお手玉をしながら、黄色いボールを振って音源操作をし曲調を変えたり効果音を鳴らしたりしましょう。

