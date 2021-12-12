# -*- coding: utf-8 -*-
import cv2
import numpy as np
from scipy import *
import pyaudio
import pygame
import wave
import sys
import time

#########################################################
def yellow_detect(img):
    # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # 黄色のHSVの値域1
    hsv_min = np.array([20, 80, 10])
    hsv_max = np.array([50,255,255])
    mask = cv2.inRange(hsv, hsv_min, hsv_max)
    return mask

#赤色
def red_detect(img):
    # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
   # 赤色のHSVの値域1
    hsv_min = np.array([0,100,100])
    hsv_max = np.array([20,255,255])
    mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

    # 赤色のHSVの値域2
    hsv_min = np.array([160,100,100])
    hsv_max = np.array([179,255,255])
    mask2 = cv2.inRange(hsv, hsv_min, hsv_max)
    mask = mask1 + mask2
    return mask

#緑色検出
def green_detect(img):
    # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # 緑色のHSVの値域1
    hsv_min = np.array([40, 75, 75])
    hsv_max = np.array([80,255,255])
    mask = cv2.inRange(hsv, hsv_min, hsv_max)
    return mask

# ブロブ解析
def analysis_blob(binary_img):
    # 2値画像のラベリング処理
    label = cv2.connectedComponentsWithStats(binary_img)

    # ブロブ情報を項目別に抽出
    data = np.delete(label[2], 0, 0)
    center = np.delete(label[3], 0, 0)

    # ブロブ面積最大のインデックス
    max_index = np.argmax(data[:, 4])

    # 面積最大ブロブの情報格納用
    maxblob = {}

    if data[:, 4][max_index] > 1000:
        # 面積最大ブロブの各種情報を取得
        maxblob["upper_left"] = (data[:, 0][max_index], data[:, 1][max_index]) # 左上座標
        maxblob["width"] = data[:, 2][max_index]  # 幅
        maxblob["height"] = data[:, 3][max_index]  # 高さ
        maxblob["area"] = data[:, 4][max_index]   # 面積
        maxblob["center"] = center[max_index]  # 中心座標

    return maxblob
#################################################################

def changePlaySpeed(data,rate):
    data = np.frombuffer(data, dtype="int16")
    res = []
    for i in range(int(len(data) / rate)):
        res.append(data[int(i * float(rate))])
    return np.int16(np.array(res)).tobytes()


# def audio(): 
#     ##################################################
#     chunk = 1024
#     wf = wave.open("audio.wav", 'rb')
#     p = pyaudio.PyAudio()
#     # open stream
#     stream = p.open(format =
#                     p.get_format_from_width(wf.getsampwidth()),
#                     channels = wf.getnchannels(),
#                     rate = wf.getframerate(),
#                     output = True)
#     # read data
#     data = wf.readframes(chunk)

#     # # prev_rate : 直前のchunkの音量, speed : 速さ
#     prev_rate = 0; speed = 1; prev_data = None; z = 0
#     # last_speed_updated : 直前に速さを変更した時刻, speed_update_tol : 速さの変更は何単位時間以内なら許すか
#     last_speed_updated = -1; speed_update_tol = 20
#     # reverbについても同様
#     last_reverb_updated = -1; reverb_update_tol = 20; isReverb = False

#     # scratch音を読んでおく
#     wf_scratch = wave.open("./effects/scratch.wav", "r")
#     scratch = np.frombuffer(wf_scratch.readframes(-1), dtype="int16")
#     is_scratch = False; scratch_time = 0; scratch_len = len(scratch)


#     j = 0
#     #再生
#     history_data = []# すでに再生したデータ
#     while data != b'':
#         ###################################################################
#         result = data      
#         result = changePlaySpeed(result, speed)

#         stream.write(result)

#         history_data.append(data)
#         prev_data = data
#         data = wf.readframes(chunk)
#     stream.close()
#     p.terminate()
#     print("done")

# def video():
#     camera = cv2.VideoCapture(0)                # カメラCh.(ここでは0)を指定
#     # 撮影＝ループ中にフレームを1枚ずつ取得（qキーで撮影終了）
#     while True:
#         ret, frame = camera.read()              # フレームを取得

#         #フレームが取得できない場合はループを抜ける
#         if not ret:
#             break

#         # キー操作があればwhileループを抜ける
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
        
#         # 赤色検出
#         try:
#             mask = color_detect(frame)
#             # マスク画像をブロブ解析（面積最大のブロブ情報を取得）
#             target = analysis_blob(mask)
#             # 面積最大ブロブの中心座標を取得
#             center_x = int(target["center"][0])
#             center_y = int(target["center"][1])
#             # フレームに面積最大ブロブの中心周囲を円で描く
#             cv2.circle(frame, (center_x, center_y), 30, (0, 200, 0),
#                     thickness=3, lineType=cv2.LINE_AA)
#         except:
#             pass
        
#         cv2.imshow('camera', cv2.resize(frame, (int(640), int(360))))             # フレームを画面に表示

    
#     # 撮影用オブジェクトとウィンドウの解放
#     camera.release()
#     cv2.destroyAllWindows()

def judge_stop(x1,x2,y1,y2):
    dx = abs(x2-x1)
    dy = abs(y2-y1)
    if dx < 10 and dy < 10:
        return True
    else:
        return False

def judge_horizontal(x1,x2,y1,y2):
    dx = x2-x1
    dy = abs(y2-y1)
    if dx > 60:
        #print(dx,dy)
        return "right"
    elif dx < -60 :
        #print(dx,dy)
        return "left" 
    else:
        return False

def judge_vertical(x1,x2,y1,y2):
    dx = abs(x2-x1)
    dy = abs(y2-y1)
    if dy > 130 and dx < 10:
        #print(dx,dy)
        return True
    else:
        return False

def judge_height(y):
    if y < 50:
        return True
    else:
        return False

def changePlaySpeedFile(path,k):
    spf = wave.open(path,"rb")
    RATE=spf.getframerate()
    data = spf.readframes(-1)
    wf = wave.open("./music/changed.wav", 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(44100*k)
    wf.writeframes(data)
    wf.close()

def main():
    effect_t = 0.4#scratch用
    previous_x = 0
    previous_y = 0
    speed = "normal"
    pause = False
    
    camera = cv2.VideoCapture(1)                # カメラCh.(ここでは0)を指定
    pygame.mixer.init()
    path = "./music/audio.wav"
    changed_path = "./music/changed.wav"
    pygame.mixer.music.load(path)
    pygame.mixer.music.play(0)
    while True:
        ret, frame = camera.read()              # フレームを取得
       
        #フレームが取得できない場合はループを抜ける
        if not ret:
            break

        # キー操作があればwhileループを抜ける # 撮影＝ループ中にフレームを1枚ずつ取得（qキーで撮影終了）
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        # 黄色検出
        try:
            mask = yellow_detect(frame)
            # マスク画像をブロブ解析（面積最大のブロブ情報を取得）
            target = analysis_blob(mask)    
                
            # 面積最大ブロブの中心座標を取得
            center_x = int(target["center"][0])
            center_y = int(target["center"][1])
            
            # フレームに面積最大ブロブの中心周囲を円で描く
            cv2.circle(frame, (center_x, center_y), 30, (0, 200, 0),
                    thickness=3, lineType=cv2.LINE_AA)
        except:
            target = {}
            center_x = None
            center_y = None
        
        cv2.imshow('camera', cv2.resize(frame, (int(1280), int(720))))           # フレームを画面に表示
        
        #scratchを鳴らす
        if effect_t == 0.4:
            try:
                # if judge_stop(center_x,previous_x,center_y,previous_y):
                #     pygame.mixer.music.pause()
                # else:
                #     pygame.mixer.music.unpause()
                
                if center_y < 120 and judge_horizontal(center_x,previous_x,center_y,previous_y) == "right":
                    if speed == "normal":
                        changePlaySpeedFile(path,3)
                        pygame.mixer.music.load(changed_path)
                        pygame.mixer.music.play(0)
                        speed = "fast"
                        print(center_y, "current speed is ", speed)
                    elif speed == "slow":
                        pygame.mixer.music.load(path)
                        pygame.mixer.music.play(0)
                        speed = "normal"
                        print(center_y, "current speed is ", speed)
                    else:
                        pass
                    effect_t = 0

                if center_y < 120 and judge_horizontal(center_x,previous_x,center_y,previous_y) == "left":
                    if speed == "normal":
                        changePlaySpeedFile(path,1)
                        pygame.mixer.music.load(changed_path)
                        pygame.mixer.music.play(0)
                        speed = "slow"
                        print(center_y, "current speed is ", speed)
                    elif speed == "fast":
                        pygame.mixer.music.load(path)
                        pygame.mixer.music.play(0)
                        speed = "normal"
                        print(center_y, "current speed is ", speed)
                    else:
                        pass
                    effect_t = 0


                if judge_vertical(center_x,previous_x,center_y,previous_y):
                    scratch_sound = pygame.mixer.Sound("./effects/scratch.wav")
                    scratch_sound.set_volume(1.0)
                    scratch_sound.play(0)
                    print("scratch")
                    effect_t = 0
                
            except:
                pass    
        effect_t = min(0.4,effect_t + 0.02)


        previous_x = center_x
        previous_y = center_y

    pygame.mixer.music.stop()
    
    # 撮影用オブジェクトとウィンドウの解放
    camera.release()
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
    main()