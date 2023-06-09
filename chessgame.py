import threading
from time import sleep
from board import Board, get_pos, pygame
from game import Logic, Color, State, Square, Move
from vars import *
from plyer import Human, Bot, PlayerType





class ChessGame:
    def __init__(self, win, fen,mode):
        self.win = win
        self.logic = Logic(fen=fen)
        self.board = Board(BOARDSIZE)
        self.board.update(self.logic)

        self.current_piece_legal_moves = []
        self.game_on = True
        self.window_on = True
        if mode == "BOT":
            modew=modeb=PlayerType.BOT
        else:
            modew=PlayerType.HUMAN
            modeb=PlayerType.BOT

        self.players = {Color.WHITE: modew,
                        Color.BLACK: modeb}

        self.bot_is_thinking = False
        self.returnlist = [None]
        self.thread = None

        # Buttons
        self.buttons = []
       

    def run(self):
        clock = pygame.time.Clock()
        while self.window_on:
            clock.tick(60)
            self.events()
            self.bot_events()
            self.draw()

    def events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.window_on = False

            if not self.game_on:
                continue
            turn = self.logic.turn
            if self.players[turn] == PlayerType.HUMAN:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if self.board.clicked(pos):
                        if self.logic.turn != self.logic.get_piece(Square(*self.board.clicked_piece_coord)).color:
                            continue
                        self.current_piece_legal_moves = self.logic.get_legal_moves_piece(
                            Square(*self.board.clicked_piece_coord))

                if self.board.dragging:
                    if event.type == pygame.MOUSEMOTION:
                        pos = pygame.mouse.get_pos()
                        self.board.drag(pos)

                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        pos = pygame.mouse.get_pos()
                        dest_coord = self.board.drop(pos)
                        move = Move(Square(*self.board.clicked_piece_coord), Square(*dest_coord))
                        for m in self.current_piece_legal_moves:
                            if m == move:
                                self.play(m)
                                print("Move played : ", m)
                                self.current_piece_legal_moves = []
                                break

    def play(self, move):
        self.logic.real_move(move)
        self.board.update(self.logic)
        self.check_end()

    def bot_events(self):
        if not self.game_on:
            return
        turn = self.logic.turn
        if self.players[turn] == PlayerType.BOT:
            if not self.bot_is_thinking:
                self.bot_is_thinking = True
                # Start the thinking thread
#sleep 3 seconds
                
                sleep(1)
                p = Bot()
                self.thread = threading.Thread(target=p.play, args=(self.logic, self.returnlist))
                self.thread.start()
            else:
                # Check if the move was found
                if self.returnlist[0]:
                    eval_and_move = self.returnlist[0]
                    self.bot_is_thinking = False
                    e, move = eval_and_move
                    print(f"Eval found : {e}")
                    self.play(move)
                    self.returnlist = [None]

 

    def check_end(self):
        if self.logic.state != State.GAMEON:
            print(self.logic.state)
            self.game_on = False

    def draw(self):
        self.win.fill(BLACK)
        self.board.draw(self.win, self.current_piece_legal_moves, *get_pos())
        for button in self.buttons:
            button.draw(self.win)
        pygame.display.flip()

    def select(self, pos):
        self.board.select(pos)



