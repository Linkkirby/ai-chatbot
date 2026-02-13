import pygame, copy, math

pygame.init()

# ================= CONFIG =================
WIDTH = 512
SQ = WIDTH // 8
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Chess AI")

LIGHT = (235,235,208)
DARK  = (119,148,85)
BLUE  = (0,120,255)
RED   = (220,50,50)
GREEN = (50,200,50)

# ================= BOARD =================
board = [
    list("rnbqkbnr"),
    list("pppppppp"),
    list("........"),
    list("........"),
    list("........"),
    list("........"),
    list("PPPPPPPP"),
    list("RNBQKBNR")
]

castle = {'K':True,'Q':True,'k':True,'q':True}

# ================= PIECES =================
PIECE_VALUES = {
    'P':10,'N':30,'B':30,'R':50,'Q':90,'K':900,
    'p':-10,'n':-30,'b':-30,'r':-50,'q':-90,'k':-900
}

DIRS = {
    'N':[(-2,-1),(-2,1),(2,-1),(2,1),(-1,-2),(-1,2),(1,-2),(1,2)],
    'B':[(-1,-1),(-1,1),(1,-1),(1,1)],
    'R':[(-1,0),(1,0),(0,-1),(0,1)],
    'Q':[(-1,-1),(-1,1),(1,-1),(1,1),(-1,0),(1,0),(0,-1),(0,1)],
    'K':[(-1,-1),(-1,1),(1,-1),(1,1),(-1,0),(1,0),(0,-1),(0,1)]
}

images = {}
for p in "PRNBQKprnbqk":
    images[p] = pygame.transform.scale(
        pygame.image.load(f"pieces/{'w' if p.isupper() else 'b'}{p.lower()}.png"),
        (SQ, SQ)
    )

# ================= HELPERS =================
def in_bounds(r,c): return 0<=r<8 and 0<=c<8
def is_white(p): return p.isupper()
def is_black(p): return p.islower()

# ================= MOVE GEN =================
def generate_moves(b, white, castle_state):
    moves=[]
    for r in range(8):
        for c in range(8):
            p=b[r][c]
            if p=='.': continue
            if white and not is_white(p): continue
            if not white and not is_black(p): continue

            # Pawn
            if p.upper()=='P':
                d=-1 if is_white(p) else 1
                if in_bounds(r+d,c) and b[r+d][c]=='.':
                    moves.append((r,c,r+d,c))
                for dc in(-1,1):
                    if in_bounds(r+d,c+dc) and b[r+d][c+dc]!='.' and is_white(p)!=is_white(b[r+d][c+dc]):
                        moves.append((r,c,r+d,c+dc))
                continue

            # Other pieces
            for dr,dc in DIRS[p.upper()]:
                nr,nc=r+dr,c+dc
                while in_bounds(nr,nc):
                    if b[nr][nc]=='.':
                        moves.append((r,c,nr,nc))
                    else:
                        if is_white(p)!=is_white(b[nr][nc]):
                            moves.append((r,c,nr,nc))
                        break
                    if p.upper() in ('N','K'): break
                    nr+=dr; nc+=dc

            # Castling
            if p=='K' and r==7 and c==4:
                if castle_state['K'] and b[7][5]==b[7][6]=='.':
                    moves.append((7,4,7,6))
                if castle_state['Q'] and b[7][1]==b[7][2]==b[7][3]=='.':
                    moves.append((7,4,7,2))
            if p=='k' and r==0 and c==4:
                if castle_state['k'] and b[0][5]==b[0][6]=='.':
                    moves.append((0,4,0,6))
                if castle_state['q'] and b[0][1]==b[0][2]==b[0][3]=='.':
                    moves.append((0,4,0,2))
    return moves

def make_move(b, m, castle_state):
    b2 = copy.deepcopy(b)
    castle2 = copy.deepcopy(castle_state)

    r1,c1,r2,c2 = m
    piece = b2[r1][c1]
    b2[r1][c1]='.'
    b2[r2][c2]=piece

    # Promotion
    if piece=='P' and r2==0: b2[r2][c2]='Q'
    if piece=='p' and r2==7: b2[r2][c2]='q'

    # Castling rook
    if piece=='K' and abs(c2-c1)==2:
        if c2==6: b2[7][5]='R'; b2[7][7]='.'
        else:      b2[7][3]='R'; b2[7][0]='.'
        castle2['K']=castle2['Q']=False

    if piece=='k' and abs(c2-c1)==2:
        if c2==6: b2[0][5]='r'; b2[0][7]='.'
        else:      b2[0][3]='r'; b2[0][0]='.'
        castle2['k']=castle2['q']=False

    if piece=='K': castle2['K']=castle2['Q']=False
    if piece=='k': castle2['k']=castle2['q']=False

    return b2, castle2

# ================= CHECK =================
def find_king(b, white):
    k='K' if white else 'k'
    for r in range(8):
        for c in range(8):
            if b[r][c]==k: return r,c

def in_check(b, white, castle_state):
    kr,kc=find_king(b,white)
    for m in generate_moves(b, not white, castle_state):
        if m[2]==kr and m[3]==kc:
            return True
    return False

def legal_moves(b, white, castle_state):
    legal=[]
    for m in generate_moves(b,white,castle_state):
        b2,c2 = make_move(b,m,castle_state)
        if not in_check(b2,white,c2):
            legal.append(m)
    return legal

def piece_legal_moves(b, r, c, white, castle_state):
    return [m for m in legal_moves(b,white,castle_state) if m[0]==r and m[1]==c]

def checkmate(b, white, castle_state):
    return in_check(b,white,castle_state) and not legal_moves(b,white,castle_state)

# ================= AI =================
def evaluate(b):
    return sum(PIECE_VALUES.get(p,0) for row in b for p in row)

def minimax(b, castle_state, d, a, beta, white):
    if d==0:
        return evaluate(b),None
    moves=legal_moves(b,white,castle_state)
    if not moves:
        return evaluate(b),None

    best=None
    if white:
        val=-math.inf
        for m in moves:
            b2,c2 = make_move(b,m,castle_state)
            e,_=minimax(b2,c2,d-1,a,beta,False)
            if e>val: val,best=e,m
            a=max(a,e)
            if beta<=a: break
        return val,best
    else:
        val=math.inf
        for m in moves:
            b2,c2 = make_move(b,m,castle_state)
            e,_=minimax(b2,c2,d-1,a,beta,True)
            if e<val: val,best=e,m
            beta=min(beta,e)
            if beta<=a: break
        return val,best

# ================= DRAW =================
def draw(selected, legal):
    for r in range(8):
        for c in range(8):
            pygame.draw.rect(WIN, LIGHT if (r+c)%2==0 else DARK, (c*SQ,r*SQ,SQ,SQ))
            if board[r][c]!='.':
                WIN.blit(images[board[r][c]],(c*SQ,r*SQ))

    for m in legal:
        pygame.draw.circle(WIN,GREEN,(m[3]*SQ+SQ//2,m[2]*SQ+SQ//2),8)

    for side in (True,False):
        if in_check(board,side,castle):
            r,c=find_king(board,side)
            pygame.draw.rect(WIN,RED,(c*SQ,r*SQ,SQ,SQ),4)

    if selected:
        pygame.draw.rect(WIN,BLUE,(selected[1]*SQ,selected[0]*SQ,SQ,SQ),3)

    pygame.display.update()

# ================= MAIN =================
selected=None
legal=[]
white_turn=True
clock=pygame.time.Clock()
run=True

while run:
    clock.tick(60)
    draw(selected, legal)

    if checkmate(board,True,castle):
        print("Checkmate! Black wins."); break
    if checkmate(board,False,castle):
        print("Checkmate! White wins."); break

    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            run=False

        if e.type==pygame.MOUSEBUTTONDOWN and white_turn:
            x,y=pygame.mouse.get_pos()
            r,c=y//SQ,x//SQ

            if selected:
                move=(selected[0],selected[1],r,c)
                if move in legal:
                    board,castle = make_move(board,move,castle)
                    white_turn=False
                selected=None
                legal=[]
            else:
                if board[r][c]!='.' and is_white(board[r][c]):
                    selected=(r,c)
                    legal=piece_legal_moves(board,r,c,True,castle)

    if not white_turn:
        _,move=minimax(board,castle,3,-math.inf,math.inf,False)
        board,castle = make_move(board,move,castle)
        white_turn=True

pygame.quit()
