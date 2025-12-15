import os
import cv2
import pathlib
import requests
from datetime import datetime, timedelta

class ChangeDetection:
    result_prev = []
    HOST = 'https://gamincha.pythonanywhere.com' #'http://10.0.2.2:8000'
    username = 'admin'
    password = 'finalterm'
    token = ''
    title = ''
    text = ''
    last_post_time = None  # 마지막 게시 시간
    POST_INTERVAL = timedelta(minutes=3)  # 게시 간격: 3분

    def __init__(self, names):
        self.result_prev = [0 for i in range(len(names))]

        res = requests.post(self.HOST + '/api-token-auth/', {
            'username': self.username,
            'password': self.password,
        })
        res.raise_for_status()
        self.token = res.json()['token']
        print(self.token)

    def add(self, names, detected_current, save_dir, image):
        # names가 딕셔너리일 수 있으므로 리스트로 변환
        names_list = list(names.values()) if isinstance(names, dict) else names
        
        self.title = ''
        self.text = ''
        change_flag = 0
        newly_detected_names = []

        i = 0
        while i < len(self.result_prev):
            if self.result_prev[i]==0 and detected_current[i]==1 :
                change_flag = 1
                newly_detected_names.append(names_list[i])
            i += 1

        self.result_prev = detected_current[:]

        # book이 현재 감지되어 있으면 서버에 게시
        if 'book' in names_list:
            book_idx = names_list.index('book')
            print(f"[DEBUG] book index: {book_idx}, detected: {detected_current[book_idx]}")
            if detected_current[book_idx] == 1:
                print("[DEBUG] book 감지됨! send 호출")
                self.title = "book!"
                self.text = "반납대에 책이 있습니다. 빨리 책을 제자리에 꽂아주세요."
                self.send(save_dir, image)

    def send(self, save_dir, image):
        now = datetime.now()
        # 3분이 안 지났으면 게시 안 함
        if self.last_post_time and (now - self.last_post_time) < self.POST_INTERVAL:
            print(f"[DEBUG] 3분 제한: 마지막 게시 {self.last_post_time}, 현재 {now}")
            return
        print(f"[DEBUG] 서버에 게시 시작!")
        self.last_post_time = now
        
        today = datetime.now()
        save_path = os.getcwd() / save_dir / 'detected' / str(today.year) / str(today.month) / str(today.day) 
        pathlib.Path(save_path).mkdir(parents=True, exist_ok=True)

        full_path = save_path / '{0}-{1}-{2}-{3}.jpg'.format(today.hour,today.minute,today.second,today.microsecond)

        dst = cv2.resize(image, dsize=(320, 240), interpolation=cv2.INTER_AREA)
        cv2.imwrite(full_path, dst)

        # 인증이 필요한 요청에 아래의 headers를 붙임
        headers = {'Authorization' : 'JWT ' + self.token, 'Accept' : 'application/json'}

        # Post Create
        data = {
        'author' : 1,
        'title' : self.title, 
        'text' : self.text, 
        'created_date' : now, 
        'published_date' : now
        }
        file = {'image' : open(full_path, 'rb')}
        res = requests.post(self.HOST + '/api_root/Post/', data=data, files=file, headers=headers)
        print(res)
