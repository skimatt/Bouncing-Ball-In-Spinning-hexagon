        import pygame
        import math
        import sys

        # Initialize Pygame
        pygame.init()

        # Screen dimensions
        WIDTH, HEIGHT = 800, 600
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Bouncing Ball in Spinning Hexagon")

        # Colors
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)

        # Ball properties
        ball_radius = 20
        ball_pos = [WIDTH // 2, HEIGHT // 2]
        ball_vel = [5, -10]  # Initial velocity

        # Gravity and friction
        gravity = 0.5
        friction = 0.99

        # Hexagon properties
        hexagon_radius = 250
        hexagon_angle = 0
        hexagon_rotation_speed = 0.02

        def get_hexagon_points(radius, angle):
            points = []
            for i in range(6):
                x = WIDTH // 2 + radius * math.cos(math.radians(60 * i + angle))
                y = HEIGHT // 2 + radius * math.sin(math.radians(60 * i + angle))
                points.append((x, y))
            return points

        def draw_hexagon(points):
            pygame.draw.polygon(screen, BLACK, points, 2)

        def draw_ball(pos):
            pygame.draw.circle(screen, RED, (int(pos[0]), int(pos[1])), ball_radius)

        def check_collision(ball_pos, ball_vel, points):
            for i in range(len(points)):
                x1, y1 = points[i]
                x2, y2 = points[(i + 1) % len(points)]

                # Line equation: (y2 - y1)x - (x2 - x1)y + (x2 y1 - x1 y2) = 0
                A = y2 - y1
                B = x1 - x2
                C = x2 * y1 - x1 * y2

                distance = abs(A * ball_pos[0] + B * ball_pos[1] + C) / math.sqrt(A**2 + B**2)

                if distance <= ball_radius:
                    # Reflect velocity
                    normal = (A, B)
                    normal_length = math.sqrt(normal[0]**2 + normal[1]**2)
                    normal = (normal[0] / normal_length, normal[1] / normal_length)

                    dot_product = ball_vel[0] * normal[0] + ball_vel[1] * normal[1]
                    ball_vel[0] -= 2 * dot_product * normal[0]
                    ball_vel[1] -= 2 * dot_product * normal[1]

                    # Apply friction
                    ball_vel[0] *= friction
                    ball_vel[1] *= friction

        # Main loop
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Update hexagon rotation
            hexagon_angle += hexagon_rotation_speed
            hexagon_points = get_hexagon_points(hexagon_radius, hexagon_angle)

            # Update ball position
            ball_vel[1] += gravity
            ball_pos[0] += ball_vel[0]
            ball_pos[1] += ball_vel[1]

            # Check for collisions
            check_collision(ball_pos, ball_vel, hexagon_points)

            # Clear screen
            screen.fill(WHITE)

            # Draw hexagon and ball
            draw_hexagon(hexagon_points)
            draw_ball(ball_pos)

            # Update display
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()