import math
import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Starting position and target position
x, y = 100.0, 100.0
target_x, target_y = 600, 400
speed = 5  # Pixels per frame


running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  # 1. Compute direction vector from current position to target
  dx = target_x - x
  dy = target_y - y

  # 2. Calculate the distance (Euclidean distance)
  distance = math.hypot(dx, dy)

  # 3. If we are close enough, snap to the target and stop
  if distance > speed:
    # Normalize the vector (divide by distance) and scale by speed
    x += (dx / distance) * speed
    y += (dy / distance) * speed
  else:
    x, y = target_x, target_y  # Reached destination

  screen.fill((30, 30, 30))
  pygame.draw.rect(screen, (0, 255, 127), (int(x), int(y), 40, 40))
  pygame.display.flip()
  clock.tick(60)

pygame.quit()
