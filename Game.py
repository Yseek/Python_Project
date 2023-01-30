import pygame
import random


pygame.init()

# 화면 크기 설정
screen_width = 1024
screen_height = 768
screen = pygame.display.set_mode((screen_width,screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Aim Practice")

# FPS
clock = pygame.time.Clock()

# 1. 게임 초기화(배경화면, 게임 이미지, 좌표, 폰트 등)

# 배경 만들기
background = pygame.image.load("images/background.png")

info = pygame.image.load("images/info.png")
info_size = info.get_rect().size
info_height = info_size[1]

# 격발 만들기
shot = pygame.image.load("images/shot.png")
shot_size = shot.get_rect().size
shot_width = shot_size[0]
shot_height = shot_size[1]

# 시작시 에임 표시 숨기기
shot_x_pos = -15 
shot_y_pos = -15

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
total_time=10
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


running = True
while running:
  dt = clock.tick(30)

  # 2. 이벤트 처리(키보드, 마우스 등)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

    if bullet <=0:
      pass
    else:
      if event.type == pygame.MOUSEBUTTONDOWN:
        shot_pos=pygame.mouse.get_pos()
        shot_x_pos=shot_pos[0]
        shot_y_pos=shot_pos[1]
        bullet -=1
        bullettxt = game_font.render("Bullet:{}".format(bullet),True,(255,255,255))
        if bullet <=0:
          reloadn=0
    if event.type == pygame.MOUSEBUTTONUP:
      shot_x_pos = -15
      shot_y_pos = -15
    
    if event.type == pygame.KEYDOWN:
      if event.key ==pygame.K_r:
        reloadn = -1
  
  # 충돌 처리
  shot_rect=shot.get_rect()
  shot_rect.left=shot_x_pos-shot_width/2
  shot_rect.top=shot_y_pos-shot_height/2

  target_rect=target.get_rect()
  target_rect.left=target_x_pos
  target_rect.top=target_y_pos

  if shot_rect.colliderect(target_rect):
    target_x_pos=random.randint(0,screen_width-target_width)
    target_y_pos=random.randint(0,screen_height-info_height-target_height)
    score +=1
    scoretxt= game_font.render("Score:{}".format(score), True, (255,255,255))

  # 경과 시간 계산
  elapsed_time = (pygame.time.get_ticks()- start_ticks)/1000
  timer = game_font.render("Time: {}".format(int(total_time-elapsed_time)),True,(255,255,255))
  timer_size=timer.get_rect().size
  timer_width=timer_size[0]

  if total_time-elapsed_time <=0:
    game_result ="END"
    running = False
    
  # 5. 화면에 그리기
  screen.blit(background,(0,0))
  screen.blit(info,(0,screen_height-info_height))
  screen.blit(shot,(shot_x_pos-shot_width/2,shot_y_pos-shot_height/2))
  screen.blit(target,(target_x_pos,target_y_pos))
  screen.blit(timer,(screen_width/2 - timer_width/2,700))
  screen.blit(scoretxt,(screen_width/6,700))
  screen.blit(bullettxt,(screen_width/1.6+bullettxt_width,700))
  if reloadn==0:
    screen.blit(reloadMsg,(screen_width/2-reloadMsg_width/2,reloadMsg_height))
  elif reloadn==-1:
    reload="Reloading.."
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

pygame.time.delay(2000)

pygame.quit()