import cv2
import numpy as np
import datetime

# Webカメラからの入力を開始
cap = cv2.VideoCapture(0)

# 現在の日時を取得
now = datetime.datetime.now()
# ファイル名に使用する日時文字列を作成
filename = 'rec/' + now.strftime('%Y%m%d_%H%M%S') + '.mp4'
# 動画保存の設定
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
fps = int(cap.get(cv2.CAP_PROP_FPS))                    # カメラのFPSを取得
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))              # カメラの横幅を取得
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter(filename, fourcc, fps, (width, height))

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        # フレームの表示
        cv2.imshow('frame',frame)

        # フレームの書き込み
        out.write(frame)

        # 'q'キーが押されたらループを抜ける
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# 入力を解放
cap.release()

# 出力を解放
out.release()

# ウィンドウを閉じる
cv2.destroyAllWindows()
