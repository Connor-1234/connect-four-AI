import pygame
import sys
import time

import connect4 as ttt

pygame.init()
size = width, height = 800,550

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)

screen = pygame.display.set_mode(size)

mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 55)

user = None
board = ttt.initial_state()
ai_turn = False

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(black)

    # Let user choose a player.
    if user is None:

        # Draw title
        title = largeFont.render("Play Connect Four", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Draw buttons
        playREDButton = pygame.Rect((width / 9), (height / 2), width / 3, 60)
        playRED = mediumFont.render("Play as Red", True, black)
        playREDRect = playRED.get_rect()
        playREDRect.center = playREDButton.center
        pygame.draw.rect(screen, white, playREDButton)
        screen.blit(playRED, playREDRect)

        playBLUEButton = pygame.Rect(5 * (width / 9), (height / 2), width / 3, 60)
        playBLUE = mediumFont.render("Play as Blue", True, black)
        playBLUERect = playBLUE.get_rect()
        playBLUERect.center = playBLUEButton.center
        pygame.draw.rect(screen, white, playBLUEButton)
        screen.blit(playBLUE, playBLUERect)

        # Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playREDButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.red
            elif playBLUEButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.blue

    else:

        # Draw game board
        tile_size = 80
        tile_origin = (width/3 - (1.5 * tile_size),
                       height/2.8 - (1.5 * tile_size))
        tiles = []
        for i in range(5):
            row = []
            for j in range(6):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                piece_rect = pygame.Rect(
                    tile_origin[0] + j * tile_size + 4,
                    tile_origin[1] + i * tile_size + 4,
                    tile_size * 0.9, tile_size * 0.9
                )
                pygame.draw.rect(screen, white, rect, 5)
                # print(board[i][j])
                if board[i][j] != ttt.EMPTY:
                    if board[i][j] == ttt.red:
                        move = pygame.draw.rect(screen, red, piece_rect)
                    else:
                        move = pygame.draw.rect(screen, blue, piece_rect)
                row.append(rect)
            tiles.append(row)

        game_over = ttt.terminal(board)
        player = ttt.player(board)

        # Show title
        if game_over:
            winner = ttt.winner(board)
            if winner is None:
                title = f"Game Over: Tie."
            else:
                if winner == ttt.red:
                    title = "Game Over: Red wins."
                else:
                    title = "Game Over: Blue wins."
        elif user == player:
            if user == ttt.red:
                title = "Play as Red"
            else:
                title = "Play as Blue"
        else:
            title = f"Computer thinking..."
        title = largeFont.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)

        # Check for AI move
        if user != player and not game_over:
            if ai_turn:
                time.sleep(0.2)
                move = ttt.minimax(board)
                board = ttt.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        # Check for a user move
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(5):
                for j in range(6):
                    if board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse):
                        if (i, j) not in ttt.actions(board):
                            counter = 0
                            x = j
                            while counter < 5:
                                action = (counter, x)
                                if action in ttt.actions(board):
                                    board = ttt.result(board, action)
                                counter += 1
                        else:
                            board = ttt.result(board, (i, j))

        if game_over:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = mediumFont.render("Play Again", True, black)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, white, againButton)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board = ttt.initial_state()
                    ai_turn = False

    pygame.display.flip()
