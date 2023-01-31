import pygame
import random

pygame.init()

def game():
  # 화면 크기 설정
  screen_width = 1024
  screen_height = 768
  screen = pygame.display.set_mode((screen_width,screen_height)) # 테스트용 
  #screen = pygame.display.set_mode((screen_width,screen_height),pygame.FULLSCREEN)

  # 화면 타이틀 설정
  pygame.display.set_caption("Aim Practice")

  # FPS
  clock = pygame.time.Clock()

  # 1. 게임 초기화(배경화면, 게임 이미지, 좌표, 폰트 등)

  # 배경 만들기
  background = pygame.image.load("images/background.png")
  backfever = pygame.image.load("images/fever.png")
  info = pygame.image.load("images/info.png")
  info_size = info.get_rect().size
  info_height = info_size[1]
  backfever.set_alpha(128) # 배경 투명도 설정
  help = pygame.image.load("images/help.png")

  # 격발 만들기
  shot = pygame.image.load("images/shot.png")
  shot_size = shot.get_rect().size
  shot_width = shot_size[0]
  shot_height = shot_size[1]

  # 탄흔 만들기
  bulletMark = pygame.image.load("images/bulletMark.png")
  bulletMark_size = bulletMark.get_rect().size
  bulletMark_width=bulletMark_size[0]
  bulletMark_height = bulletMark_size[1]


  # 시작시 에임 표시 숨기기
  shot_x_pos = -40
  shot_y_pos = -40

  # 표적 만들기
  target = pygame.image.load("images/target.png")
  target_size = target.get_rect().size
  target_width = target_size[0]
  target_height = target_size[1]

  #표적 시작 위치
  target_x_pos = screen_width/2 - target_width/2
  target_y_pos = (screen_height- info_height)/2 - target_height/2


  # Font 정의
  game_font = pygame.font.Font(None,40)

  # 스코어 , 시간 , 종료 메세지, 총알 표시
  score=0
  scoretxt= game_font.render("Score:{}".format(score), True, (255,255,255))
  scoretxt_size=scoretxt.get_rect().size
  scoretxt_width = scoretxt_size[0]
  scoretxt_height = scoretxt_size[1]
  total_time=30
  start_ticks = pygame.time.get_ticks() # 시작 시간 정의
  game_result=""
  reload = "Reload"
  reloadMsg = game_font.render(reload,True,(255,255,255))
  reloadMsg_size = reloadMsg.get_rect().size
  reloadMsg_width = reloadMsg_size[0]
  reloadMsg_height = reloadMsg_size[1]
  reloadn=-2
  bullet = 8
  bullettxt = game_font.render("Bullet:{}".format(bullet),True,(255,255,255))
  bullettxt_size=bullettxt.get_rect().size
  bullettxt_width = bullettxt_size[0]

  #탄흔 유지
  bulletMarks=[]

  # 피버 카운트
  hits=[]
  hit=0
  
  # 피버 fever 가 0이면 일반, 1이면 fever 상태
  fever=0
  fever_time_start=0
  fever_time=0
  feverM="FEVER TIME"
  feverMsg=game_font.render(feverM,True,(255,255,0))
  feverMsg_size = feverMsg.get_rect().size
  feverMsg_width = feverMsg_size[0]
  #feverMsg_height = feverMsg_size[1]

  # 커서 변경
  pygame.mouse.set_visible(False)
  cursor_Img = pygame.image.load("images/cursor.png")
  cursor_Img_size = cursor_Img.get_rect().size
  cursor_img_width = cursor_Img_size[0]
  cursor_img_height = cursor_Img_size[1]
  cursor_x_pos=-100
  cursor_y_pos=-100

  # 일시정지
  pause =True
  pause_time = 0
  pause_time_sum = 0

  running = True
  while running:
    dt = clock.tick(60) # 프레임 

    # 2. 이벤트 처리(키보드, 마우스 등)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False

      if bullet <=0:
        pass
      else:
        if event.type == pygame.MOUSEBUTTONDOWN:
          hit=-1 # 격발 함
          shot_pos=pygame.mouse.get_pos()
          shot_x_pos=shot_pos[0]
          shot_y_pos=shot_pos[1]
          if shot_y_pos > screen_height-info_height:
            shot_y_pos = screen_height-info_height
          if fever==0:
            bullet -=1
          else:
            bullet=8
          bullettxt = game_font.render("Bullet:{}".format(bullet),True,(255,255,255))
          bulletMarks.append([shot_x_pos-bulletMark_width/2,shot_y_pos-bulletMark_height/2]) # 탄흔 좌표를 리스트에 저장
          if bullet <=0:
            reloadn=0
      if event.type == pygame.MOUSEBUTTONUP:
        shot_x_pos = -40
        shot_y_pos = -40
      
      if event.type == pygame.KEYDOWN:
        if event.key ==pygame.K_r:
          reloadn = -1
        if event.key == pygame.K_F1:   # F1 누르고 있을시 일시정지
          pause_start=pygame.time.get_ticks()
          screen.blit(help,(0,0))  # F1 도움말 화면
          pygame.display.update()
          while pause:   
            for event in pygame.event.get():
              if event.type == pygame.KEYUP:   # F1 누르고 있지 않을시 일시정지 해제
                if event.key == pygame.K_F1:
                  pause_time = (pygame.time.get_ticks()-pause_start)/1000  # 개별 일시정지한 시간 
                  pause_time_sum += pause_time  # 총 일시정지한 시간,  모든 타이머에 빼줘야할 값 (일시정지 한 만큼 현재 시간은 계속 흘렀기 때문)
                  pause =False  
          pause=True


      if event.type == pygame.MOUSEMOTION:  # 조준점이 정보창 위로 올라가지 못하게 함
        cursor_pos=pygame.mouse.get_pos()
        cursor_x_pos = cursor_pos[0]
        cursor_y_pos = cursor_pos[1]
        if cursor_y_pos > screen_height-info_height:
          cursor_y_pos = screen_height-info_height


    # 충돌 처리
    '''
    shot_rect=shot.get_rect()
    shot_rect.left=shot_x_pos-shot_width/2
    shot_rect.top=shot_y_pos-shot_height/2
    target_rect=target.get_rect()
    target_rect.left=target_x_pos
    target_rect.top=target_y_pos
    '''
    # 그림 이미지보다 충돌범위를 적게 함
    shot_rect = pygame.Rect(shot_x_pos-1,shot_y_pos-1,2,2)
    target_rect = pygame.Rect(target_x_pos+15, target_y_pos+15,20,20)

    # 연속으로 5번 맞추면 피버타임
    if hit==-1:
      if shot_rect.colliderect(target_rect):
        target_x_pos=random.randint(0,screen_width-target_width)
        target_y_pos=random.randint(0,screen_height-info_height-target_height)
        score +=1
        scoretxt= game_font.render("Score:{}".format(score), True, (255,255,255))
        hit=1 # 격발이 끝났음을 알림
        hits.append([1])
        if len(hits)>=5:
          fever=1
          reloadn=-2
          bullet=8
          fever_time_start=pygame.time.get_ticks()  # 피버가 시작된 시간 
          hits.clear()
      else:
        hit=1 
        hits.clear()
    if fever==1:
      fever_time= (pygame.time.get_ticks() -fever_time_start) / 1000 - pause_time_sum  # 피버 시간 재기
      hits.clear() # 10초 동안은 연속 적중 카운트 안 함
      if fever_time> 5: # 5초동안만 지속  
        fever=0
    
    # 경과 시간 계산
    elapsed_time = (pygame.time.get_ticks()- start_ticks)/1000-pause_time_sum
    timer = game_font.render("Time: {}".format(int(total_time-elapsed_time)),True,(255,255,255))
    timer_size=timer.get_rect().size
    timer_width=timer_size[0]

    if total_time-elapsed_time <=0:
      game_result ="END"
      running = False
      global end
      end=True
      
    # 5. 화면에 그리기
    screen.blit(background,(0,0))
    if fever ==1:
      screen.blit(backfever,(0,0))
      screen.blit(feverMsg,(screen_width/2-feverMsg_width/2,scoretxt_height))
    for bulletMark_x_pos, bulletMark_y_pos in bulletMarks:  # 리스트에 저장된 탄흔 좌표를 출력
      screen.blit(bulletMark,(bulletMark_x_pos, bulletMark_y_pos))
    screen.blit(info,(0,screen_height-info_height))
    screen.blit(shot,(shot_x_pos-shot_width/2,shot_y_pos-shot_height/2))
    screen.blit(target,(target_x_pos,target_y_pos))
    screen.blit(timer,(screen_width/2 - timer_width/2,700))
    screen.blit(scoretxt,(screen_width/6,700))
    screen.blit(bullettxt,(screen_width/1.6+bullettxt_width,700))
    screen.blit(cursor_Img,(cursor_x_pos-cursor_img_width/2,cursor_y_pos-cursor_img_height/2))
    if reloadn==0:
      screen.blit(reloadMsg,(screen_width/2-reloadMsg_width/2,reloadMsg_height))
    elif reloadn==-1:
      reload="Reloading..."
      reloadMsg = game_font.render(reload,True,(255,255,255))
      screen.blit(reloadMsg,(screen_width/2-reloadMsg_width/2,reloadMsg_height))
      pygame.display.update()
      pygame.time.delay(1000)
      bullet =8
      bullettxt = game_font.render("Bullet:{}".format(bullet),True,(255,255,255))
      reload="Reload"
      reloadMsg = game_font.render(reload,True,(255,255,255))
      screen.blit(reloadMsg,(-100,-100))
      reloadn=-2

    pygame.display.update()

  msg = game_font.render(game_result,True,(255,255,255))
  msg_rect = msg.get_rect(center=(int(screen_width/2),int(screen_height/2-100)))
  screen.blit(msg,(msg_rect))
  screen.blit(scoretxt,(screen_width/2-scoretxt_width/2,screen_height/2-scoretxt_height/2))
  pygame.display.update()

  # 종료 부분 
  endmsg = "Press Enter to Exit" 
  endmsgtxt = game_font.render(endmsg,True,(255,255,255))
  endmsgtxt_size=endmsgtxt.get_rect().size
  endmsgtxt_width=endmsgtxt_size[0]
  restart = "Press Space to Restart"
  restarttxt = game_font.render(restart,True,(255,255,255))
  restarttxt_size = restarttxt.get_rect().size
  restarttxt_width = restarttxt_size[0]
  screen.blit(endmsgtxt,(screen_width/2-endmsgtxt_width/2,screen_height/4))
  screen.blit(restarttxt,(screen_width/2-restarttxt_width/2,screen_height/4+40))
  pygame.display.update()


def start():
  # 시작 화면 크기 , 타이틀 설정
  screen_width = 800
  screen_height = 600
  screen = pygame.display.set_mode((screen_width,screen_height))
  pygame.display.set_caption("입장")

  #시작 화면 배경 이미지
  startBackground = pygame.image.load("images/startBackground.jpg")

  #스타트 버튼 이미지
  startbtn = pygame.image.load("images\\start.png")
  startbtnhover= pygame.image.load("images\\starthover.png")
  startbtn_size = startbtn.get_rect().size
  startbtn_width= startbtn_size[0]
  startbtn_hegith = startbtn_size[1]

  # 스타트 버튼 범위 확인
  startbtn_x_pos= screen_width/2-startbtn_width/2
  startbtn_y_pos = screen_height/2-startbtn_hegith/2
  startbtn_rect=pygame.Rect(startbtn_x_pos,startbtn_y_pos+30,150,60)

  # 배경 이미지 그리기
  screen.blit(startBackground,(0,0))
  screen.blit(startbtn,(screen_width/2-startbtn_width/2,screen_height/2-startbtn_hegith/2))
  pygame.display.update()


  running= True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.MOUSEMOTION:  # 마우스가 움직일 때마다 좌표 계산
        mouse_pos=pygame.mouse.get_pos()
        mouse_rect=pygame.Rect(mouse_pos[0],mouse_pos[1],1,1)
        if mouse_rect.colliderect(startbtn_rect):      # 마우스가 버튼 위에 호버링 되면 버튼 색상 변경
          screen.blit(startbtnhover,(screen_width/2-startbtn_width/2,screen_height/2-startbtn_hegith/2))
          pygame.display.update()
        else:                                          # 마우스가 버튼 위에 없을 때 원래 버튼으로 색상 변경
          screen.blit(startbtn,(screen_width/2-startbtn_width/2,screen_height/2-startbtn_hegith/2))
          pygame.display.update()
      if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos=pygame.mouse.get_pos()
        mouse_rect=pygame.Rect(mouse_pos[0],mouse_pos[1],1,1)
        if mouse_rect.colliderect(startbtn_rect):  
          game()
          running=False
      if event.type==pygame.QUIT:
        running= False
        global end
        end=False

start()

while end:
  for event in pygame.event.get():
    if event.type==pygame.KEYDOWN:
      if event.key==pygame.K_RETURN:
        end=False
      if event.key==pygame.K_SPACE:
        game()
pygame.quit()


