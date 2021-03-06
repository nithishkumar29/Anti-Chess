import time
import random
import board
import pieces
import Tkinter as tk
from PIL import Image, ImageTk
#import suicide

#board = chess.variant.SuicideBoard()

class BoardGuiTk(tk.Frame):
    pieces = {}
    selected = None
    selected_piece = None
    hilighted = None
    icons = {}
    play=0
    color1 = "white"
    color2 = "grey"

    rows = 8
    columns = 8
    maxDepth=99;
    @property
    def canvas_size(self):
        return (self.columns * self.square_size,
                self.rows * self.square_size)

    def __init__(self, parent, chessboard, square_size=64):

        self.chessboard = chessboard
        self.square_size = square_size
        self.parent = parent

        canvas_width = self.columns * square_size
        canvas_height = self.rows * square_size

        tk.Frame.__init__(self, parent)

        self.canvas = tk.Canvas(self, width=canvas_width, height=canvas_height, background="grey")
        self.canvas.pack(side="top", fill="both", anchor="c", expand=True)

        self.canvas.bind("<Configure>", self.refresh)
        self.canvas.bind("<Button-1>", self.click)
        self.statusbar = tk.Frame(self, height=64)
        self.button_quit = tk.Button(self.statusbar, text="New", fg="black", command=self.reset)
        self.button_quit.pack(side=tk.LEFT, in_=self.statusbar)

        self.button_save = tk.Button(self.statusbar, text="Save", fg="black", command=self.chessboard.save_to_file)
        self.button_save.pack(side=tk.LEFT, in_=self.statusbar)

        self.label_status = tk.Label(self.statusbar, text="   White's turn  ", fg="black")
        self.label_status.pack(side=tk.LEFT, expand=0, in_=self.statusbar)

        self.button_quit = tk.Button(self.statusbar, text="Quit", fg="black", command=self.parent.destroy)
        self.button_quit.pack(side=tk.RIGHT, in_=self.statusbar)
        self.statusbar.pack(expand=False, fill="x", side='bottom')


    def click(self, event):

        # Figure out which square we've clicked
        col_size = row_size = event.widget.master.square_size

        current_column = event.x / col_size
        current_row = 7 - (event.y / row_size)

        position = self.chessboard.letter_notation((current_row, current_column))
        piece = self.chessboard[position]

        if self.selected_piece:
            self.move(self.selected_piece[1], position)
            self.selected_piece = None
            self.hilighted = None
            self.pieces = {}
            self.refresh()
            self.draw_pieces()
            self.canvas.after(200, self.opponent)
            self.canvas.after(200, self.refresh)
            self.canvas.after(200, self.draw_pieces)
        else:    
            self.hilight(position)
            self.refresh()

    def opponent(self):
        if self.play==0:
            return
        self.play=0
        valid_move=self.check()
        #k=random.randint(0,len(valid_move))-1
        if len(valid_move)==1:
            p3,p4=valid_move[0].split("+")
            piece = self.chessboard[p3]
            try:
                self.chessboard.move(p3,p4)
            except board.ChessError as error:
                self.label_status["text"] = error.__class__.__name__
            else:
                self.label_status["text"] = " " + piece.color.capitalize() +": "+ p3 + p4
        elif len(valid_move)>1:
            overallBestScore, overallBestMove = -self.INFINITY, valid_move[0]
            for depth in range(0,self.maxDepth):
                    sys.stdout.write(".")
                bestScore, bestMove = self.getMoveToDepth(board, maxTime, startTime, valid_move, depth)
                if bestScore>=overallBestScore:
                    overallBestMove = bestMove
                    overallBestScore = bestScore
                if time.time()-startTime > maxTime:
                    break
            p3,p4=bestMove.split("+")
            piece = self.chessboard[p3]
            try:
                self.chessboard.move(p3,p4)
            except board.ChessError as error:
                self.label_status["text"] = error.__class__.__name__
            else:
                self.label_status["text"] = " " + piece.color.capitalize() +": "+ p3 + p4

    '''def getMoveToDepth(self, board, maxTime, startTime, validMoves, depth):
        bestScore, bestMove = -self.INFINITY, validMoves[0]
        counter=0

        for move in validMoves:
            counter += 1
            p3,p4=bestMove.split("+")
            self.board.move(p3,p4)
            if self.color==self.color1
                score = -self.alphabeta(board, depth, -self.INFINITY, self.INFINITY, self.color2, startTime, maxTime)
            else:
                score = -self.alphabeta(board, depth, -self.INFINITY, self.INFINITY, self.color1, startTime, maxTime)
            #board.retractMove()
                        elapsedTime = time.time() - startTime
                        if elapsedTime>maxTime:
                            break
            if score > bestScore:
                bestScore, bestMove = score, move
            if bestScore==self.INFINITY:
                break
        return bestScore, bestMove

    def scoringLast(self, board, color, validMoves):
        n_me = board.getNumPieces(self.color)
        n_him = board.getNumPieces(1-self.color)
        if n_me==0:
            return +self.INFINITY
        if n_him==0:
            return -self.INFINITY
                if len(validMoves)==0:
                    return +self.INFINITY
                material_score = n_him - n_me
                
        return material_score
        
    def alphabeta(self, board, depth, a, b, color, startTime, maxTime):
        validMoves = self.check()
        if len(validMoves)==0 or depth <= 0:
            return self.scoringLast(board, color, validMoves)
        for move in validMoves:
            p3,p4=move.split('+')
            self.board.move(p3,p4)
            if self.color==self.color1
                a=max(a,-self.alphabeta(board, depth, -self.INFINITY, self.INFINITY, self.color2, startTime, maxTime))
            else:
                a=max(a,-self.alphabeta(board, depth, -self.INFINITY, self.INFINITY, self.color1, startTime, maxTime))
            #a = max(a, -self.alphabeta(board, depth-1, -b, -a, 1-color, startTime, maxTime))
            #board.retractMove()
            if b <= a:
                break   
                        elapsedTime = time.time() - startTime
                        if elapsedTime>maxTime:
                            return 0 

        return a
        '''

    def move(self, p1, p2):
        valid_move=self.check()
        piece = self.chessboard[p1]
        dest_piece = self.chessboard[p2]
        flag=1
        val=p1+'+'+p2
        if val in valid_move:
            flag=0
        if flag==1:
            return 
        if dest_piece is None or dest_piece.color != piece.color:
            self.play=1;
            try:
                self.chessboard.move(p1,p2)
            except board.ChessError as error:
                self.label_status["text"] = error.__class__.__name__
            else:
                self.label_status["text"] = " " + piece.color.capitalize() +": "+ p1 + p2

    def check(self):
        valid_moves=[]
        v_m=[]
        for i in range (0,8):
            for j in range (0,8):
                pos = self.chessboard.letter_notation((i,j))
                piece = self.chessboard[pos]
                if piece is not None and (piece.color == self.chessboard.player_turn):
                    for k in range(0,len(piece.possible_moves(pos))):
                        pos1=piece.possible_moves(pos)[k]
                        valid_moves.append(pos+'+'+pos1)
                        piece2=self.chessboard[pos1]
                        if piece2 is not None:
                            v_m.append(pos+'+'+pos1)
        if len(v_m)>0:
            return v_m
        else:
            return valid_moves


    def hilight(self, pos):
        piece = self.chessboard[pos]
        if piece is not None and (piece.color == self.chessboard.player_turn):
            self.selected_piece = (self.chessboard[pos], pos)
            self.hilighted = map(self.chessboard.number_notation, (self.chessboard[pos].possible_moves(pos)))
            

    def addpiece(self, name, image, row=0, column=0):
        '''Add a piece to the playing board'''
        self.canvas.create_image(0,0, image=image, tags=(name, "piece"), anchor="c")
        self.placepiece(name, row, column)

    def placepiece(self, name, row, column):
        '''Place a piece at the given row/column'''
        self.pieces[name] = (row, column)
        x0 = (column * self.square_size) + int(self.square_size/2)
        y0 = ((7-row) * self.square_size) + int(self.square_size/2)
        self.canvas.coords(name, x0, y0)

    def refresh(self, event={}):
        '''Redraw the board'''
        if event:
            xsize = int((event.width-1) / self.columns)
            ysize = int((event.height-1) / self.rows)
            self.square_size = min(xsize, ysize)

        self.canvas.delete("square")
        color = self.color2
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.square_size)
                y1 = ((7-row) * self.square_size)
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                if (self.selected is not None) and (row, col) == self.selected:
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="orange", tags="square")
                elif(self.hilighted is not None and (row, col) in self.hilighted):
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="spring green", tags="square")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
                color = self.color1 if color == self.color2 else self.color2
        for name in self.pieces:
            self.placepiece(name, self.pieces[name][0], self.pieces[name][1])
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")

    def draw_pieces(self):
        self.canvas.delete("piece")
        for coord, piece in self.chessboard.iteritems():
            x,y = self.chessboard.number_notation(coord)
            if piece is not None:
                filename = "img/%s%s.png" % (piece.color, piece.abbriviation.lower())
                piecename = "%s%s%s" % (piece.abbriviation, x, y)

                if(filename not in self.icons):
                    self.icons[filename] = ImageTk.PhotoImage(file=filename, width=32, height=32)

                self.addpiece(piecename, self.icons[filename], x, y)
                self.placepiece(piecename, x, y)

        #time.sleep(2)

    def reset(self):
        self.chessboard.load(board.FEN_STARTING)
        self.refresh()
        self.draw_pieces()
        self.refresh()

def display(chessboard):
    root = tk.Tk()
    root.title("Simple Python Chess")

    gui = BoardGuiTk(root, chessboard)
    gui.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    gui.draw_pieces()

    #root.resizable(0,0)
    root.mainloop()

if __name__ == "__main__":
    display()
