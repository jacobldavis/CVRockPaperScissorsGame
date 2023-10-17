# Import Modules
import random
import pygame
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

# Initialize PyGame
pygame.init()

# Create Window/Display
width, height = 640, 480
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rock, Paper, Scissors, Shoot!")

# Start Webcam
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# Import/Create Resources
gameFont = pygame.font.Font('../Resources/Font.ttf', 50)
color1 = pygame.color.Color(30, 144, 255)
color2 = pygame.color.Color(255, 143, 31)

# Create Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Initialize Clock for FPS
fps = 30
clock = pygame.time.Clock()

# GameState Variables
gameState = False
shoot = False
start_time = 0
player_score = 0
cpu_score = 0
fingerUp = 0
playerChoice = ""
cpuChoice = ""
cpuInt = 0
gameCount = 0
current = 0
outcome = ""

# Main loop
start = True

while start:
    # Quit & Start
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("Start")
            start_time = pygame.time.get_ticks()
            gameState = True
            current = gameCount
            gameCount += 1

    # OpenCV
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    # Frame Settings
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgRGB = np.rot90(imgRGB)
    frame = pygame.surfarray.make_surface(imgRGB).convert()
    frame = pygame.transform.flip(frame, True, False)
    window.blit(frame, (0, 0))

    # Text Backgrounds and Start Text
    s = pygame.Surface((640, 70))
    s2 = pygame.Surface((640, 40))
    s.set_alpha(170)
    s2.set_alpha(170)
    s.fill((5, 5, 5))
    s2.fill((5, 5, 5))
    window.blit(s, (0, 0))
    window.blit(s2, (0, 440))
    if not gameState:
        start_text = gameFont.render("Click anywhere to start!", False, color1)
        start_rect = start_text.get_rect(center=(width/2, 460))
        window.blit(start_text, start_rect)

    # Game Loop
    if gameState:

        # Countdown
        current_time_int = 5 - int((pygame.time.get_ticks() - start_time) / 1000)
        if current_time_int > 0:
            countdown_text = gameFont.render(f'Shoot!  {current_time_int}', False, color1)
            countdown_rect = countdown_text.get_rect(center=(width/2, 460))
            window.blit(countdown_text, countdown_rect)

        # Detect Hands & Logic
        if hands:
            hand1 = hands[0]
            if current_time_int > 0:
                fingersUp = detector.fingersUp(hand1)
                fingerCount = fingersUp.count(1)
                if fingerCount == 0 or fingerCount == 1:
                    playerChoice = "Rock"
                elif fingerCount == 2 or fingerCount == 3:
                    playerChoice = "Scissors"
                elif fingerCount == 4 or fingerCount == 5:
                    playerChoice = "Paper"

        if current_time_int == 0:
            current += 1
            if gameCount == current:
                cpuInt = random.randint(1, 3)
                if cpuInt == 1:
                    cpuChoice = "Rock"
                elif cpuInt == 2:
                    cpuChoice = "Paper"
                elif cpuInt == 3:
                    cpuChoice = "Scissors"
                if cpuChoice == playerChoice:
                    outcome = "Draw!"
                elif cpuChoice == "Rock" and playerChoice == "Scissors" or cpuChoice == "Paper" and playerChoice == "Rock" or cpuChoice == "Scissors" and playerChoice == "Paper":
                    outcome = "CPU Wins!"
                    cpu_score += 1
                else:
                    outcome = "P1 Wins!"
                    player_score += 1

        if current_time_int < 0:
            outcomeText = gameFont.render(outcome, False, color1)
            outcomeRect = outcomeText.get_rect(center=(width/2, 460))
            window.blit(outcomeText, outcomeRect)

            restartText = gameFont.render("Click to restart!", False, color2)
            restartRect = restartText.get_rect(center=(width/2, 60))
            window.blit(restartText, restartRect)
    # Text
    playerText = gameFont.render(playerChoice, False, color2)
    playerRect = playerText.get_rect(center=(70, 460))
    window.blit(playerText, playerRect)

    cpuText = gameFont.render(cpuChoice, False, color2)
    cpuRect = cpuText.get_rect(center=(570, 460))
    window.blit(cpuText, cpuRect)

    title = gameFont.render('Rock, Paper, Scissors, Shoot!', True, color1)
    window.blit(title, (100, 10))

    playerScoreText = gameFont.render(f'P1: {player_score}', True, color2)
    window.blit(playerScoreText, (10, 40))

    cpuScoreText = gameFont.render(f'CPU: {cpu_score}', True, color2)
    window.blit(cpuScoreText, (540, 40))

    # Update Display
    pygame.display.update()

    # Set FPS
    clock.tick(fps)
