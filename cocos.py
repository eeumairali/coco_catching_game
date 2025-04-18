import random
import pygame
import math
import time

class Coco:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Coco({self.x}, {self.y})"

class Game:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.target_coco = None
        self.player_scores = [0, 0]  # Player 1 and Player 2 scores
        self.player_clicks = [None, None]  # Store Player 1 and Player 2 clicks
        self.current_turn = 0  # 0 for Player 1, 1 for Player 2
        pygame.init()
        self.screen = pygame.display.set_mode((width * cell_size, height * cell_size))
        pygame.display.set_caption("Coco Catching Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

    def spawn_coco(self):
        x = random.randint(0, self.width - 1)
        y = random.randint(0, self.height - 1)
        self.target_coco = Coco(x, y)
        print(f"Target Coco: {self.target_coco}")

    def draw_grid(self):
        for x in range(0, self.width * self.cell_size, self.cell_size):
            for y in range(0, self.height * self.cell_size, self.cell_size):
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)

    def draw_coco(self):
        if self.target_coco and self.player_clicks[0] and self.player_clicks[1]:  # Show only after both clicks
            rect = pygame.Rect(
                self.target_coco.x * self.cell_size,
                self.target_coco.y * self.cell_size,
                self.cell_size,
                self.cell_size,
            )
            pygame.draw.rect(self.screen, (255, 255, 0), rect)  # Yellow for Coco

    def draw_clicks(self):
        if self.player_clicks[0]:  # Player 1's click
            rect = pygame.Rect(
                self.player_clicks[0][0] * self.cell_size,
                self.player_clicks[0][1] * self.cell_size,
                self.cell_size,
                self.cell_size,
            )
            pygame.draw.rect(self.screen, (255, 0, 0), rect)  # Red for Player 1
        if self.player_clicks[1]:  # Player 2's click
            rect = pygame.Rect(
                self.player_clicks[1][0] * self.cell_size,
                self.player_clicks[1][1] * self.cell_size,
                self.cell_size,
                self.cell_size,
            )
            pygame.draw.rect(self.screen, (0, 0, 255), rect)  # Blue for Player 2

    def draw_scores(self):
        score_text = f"Player 1: {self.player_scores[0]}  Player 2: {self.player_scores[1]}"
        text_surface = self.font.render(score_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (10, 10))

    def calculate_distance(self, click_x, click_y, coco_x, coco_y):
        return math.sqrt((click_x - coco_x) ** 2 + (click_y - coco_y) ** 2)

    def handle_click(self, player, mouse_pos):
        click_x = mouse_pos[0] // self.cell_size
        click_y = mouse_pos[1] // self.cell_size
        self.player_clicks[player] = (click_x, click_y)
        print(f"Player {player + 1} clicked at ({click_x}, {click_y})")

        # Switch turn to the next player
        self.current_turn = (self.current_turn + 1) % 2

    def show_results(self):
        # Calculate distances
        coco_x, coco_y = self.target_coco.x, self.target_coco.y
        player1_distance = self.calculate_distance(
            self.player_clicks[0][0], self.player_clicks[0][1], coco_x, coco_y
        )
        player2_distance = self.calculate_distance(
            self.player_clicks[1][0], self.player_clicks[1][1], coco_x, coco_y
        )

        # Print distances
        print(f"Player 1 distance: {player1_distance:.2f}")
        print(f"Player 2 distance: {player2_distance:.2f}")

        # Determine winner
        if player1_distance < player2_distance:
            print("Player 1 wins this round!")
            self.player_scores[0] += 1
        elif player2_distance < player1_distance:
            print("Player 2 wins this round!")
            self.player_scores[1] += 1
        else:
            print("It's a tie!")

        # Show results for 1 second
        self.screen.fill((0, 0, 0))  # Clear the screen
        self.draw_grid()
        self.draw_coco()
        self.draw_clicks()
        self.draw_scores()
        pygame.display.flip()
        time.sleep(1)

    def run(self):
        running = True
        self.spawn_coco()  # Spawn the first target

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.current_turn == 0 and event.button == 1:  # Player 1's turn (left click)
                        self.handle_click(0, event.pos)
                    elif self.current_turn == 1 and event.button == 1:  # Player 2's turn (left click)
                        self.handle_click(1, event.pos)

            # If both players have clicked, show results and start the next round
            if self.player_clicks[0] and self.player_clicks[1]:
                self.show_results()
                self.player_clicks = [None, None]  # Reset clicks
                self.spawn_coco()  # Spawn a new Coco

            self.screen.fill((0, 0, 0))  # Clear the screen
            self.draw_grid()
            self.draw_coco()
            self.draw_scores()
            pygame.display.flip()
            self.clock.tick(30)  # Limit to 30 frames per second

        pygame.quit()

if __name__ == "__main__":
    game = Game(10, 10, 50)  # Game grid of size 10x10 with each cell 50x50 pixels
    game.run()