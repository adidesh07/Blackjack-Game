import pygame
from random import *
from PIL import Image
import time
pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack")

# Background
BG = pygame.transform.scale(pygame.image.load("C:\\Users\\Admin\\Desktop\\Deck\\Poker_table.png"), (WIDTH, HEIGHT))

# Deck images
Ace = Image.open("C:\\Users\\Admin\\Desktop\\Deck\\Ace.png").resize((70, 90))
Two = Image.open("C:\\Users\\Admin\\Desktop\\Deck\\2.png").resize((70, 90))
Three = Image.open("C:\\Users\\Admin\\Desktop\\Deck\\3.png").resize((70, 90))
Four = Image.open("C:\\Users\\Admin\\Desktop\\Deck\\4.png").resize((70, 90))
Five = Image.open("C:\\Users\\Admin\\Desktop\\Deck\\5.png").resize((70, 90))
Six = Image.open("C:\\Users\\Admin\\Desktop\\Deck\\6.png").resize((70, 90))
Seven = Image.open("C:\\Users\\Admin\\Desktop\\Deck\\7.png").resize((70, 90))
Eight = Image.open("C:\\Users\\Admin\\Desktop\\Deck\\8.png").resize((70, 90))
Nine = Image.open("C:\\Users\\Admin\\Desktop\\Deck\\9.png").resize((70, 90))
Ten = Image.open("C:\\Users\\Admin\\Desktop\\Deck\\10.png").resize((70, 90))
Jack = Image.open("C:\\Users\\Admin\\Desktop\\Deck\\Jack.jpg").resize((70, 90))
Queen = Image.open("C:\\Users\\Admin\\Desktop\\Deck\\Queen1.jpg").resize((70, 90))
King = Image.open("C:\\Users\\Admin\\Desktop\\Deck\\King.png").resize((70, 90))
Card = Image.open("C:\\Users\\Admin\\Desktop\\Deck\\Card.jpg").resize((70, 90))
Chips = Image.open("C:\\Users\\Admin\\Desktop\\Deck\\Chips.png").resize((80, 80))

Ace_img = pygame.image.fromstring(Ace.tobytes(), Ace.size, Ace.mode)
Two_img = pygame.image.fromstring(Two.tobytes(), Two.size, Two.mode)
Three_img = pygame.image.fromstring(Three.tobytes(), Three.size, Three.mode)
Four_img = pygame.image.fromstring(Four.tobytes(), Four.size, Four.mode)
Five_img = pygame.image.fromstring(Five.tobytes(), Five.size, Five.mode)
Six_img = pygame.image.fromstring(Six.tobytes(), Six.size, Six.mode)
Seven_img = pygame.image.fromstring(Seven.tobytes(), Seven.size, Seven.mode)
Eight_img = pygame.image.fromstring(Eight.tobytes(), Eight.size, Eight.mode)
Nine_img = pygame.image.fromstring(Nine.tobytes(), Nine.size, Nine.mode)
Ten_img = pygame.image.fromstring(Ten.tobytes(), Ten.size, Ten.mode)
Jack_img = pygame.image.fromstring(Jack.tobytes(), Jack.size, Jack.mode)
Queen_img = pygame.image.fromstring(Queen.tobytes(), Queen.size, Queen.mode)
King_img = pygame.image.fromstring(King.tobytes(), King.size, King.mode)
Card_img = pygame.image.fromstring(Card.tobytes(), Card.size, Card.mode)
Chips_img = pygame.image.fromstring(Chips.tobytes(), Chips.size, Chips.mode)

Image_Deck = {"Ace": Ace_img, 2: Two_img, 3: Three_img, 4: Four_img, 5: Five_img, 6:Six_img, 7:Seven_img, 8:Eight_img, 9:Nine_img, 10:Ten_img, 11:Jack_img, 12:Queen_img, 13:King_img, 'Back':Card_img}
Deck = ["Ace", 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

def shuffle_deck():
    shuffle(Deck)

def draw_card():
    shuffle_deck()
    card = Deck[0]
    return card

def card_value(card):
    if card == 'Ace':
        return 1
    elif card > 10:
        return 10
    else:
        return card


class Draw_cards:
    def __init__(self, window):
        self.window = window

    def player(self, images, y_pos=390):
        tot_width = 0
        for items in images:
            tot_width += 70
        tot_width += (len(images) - 1) * 4

        starting_pt = (WIDTH / 2) - (tot_width / 2)
        for item in images:
            self.window.blit(Image_Deck[item], (starting_pt, y_pos))
            starting_pt += 74

    def dealer(self, images, y_pos=120):
        if len(images) == 1:
            self.window.blit(Image_Deck[images[0]], (328, 120))
            self.window.blit(Image_Deck['Back'], (402, 120))
        else:
            self.player(images, y_pos)


# Initial cards:
def player_cards():
    cards = [draw_card()]
    cards.append(draw_card())
    cardsum = 0
    for items in cards:
        cardsum += card_value(items)
    return [cards, cardsum]

def dealer_cards():
    cards = draw_card()
    cardsum = 0
    cardsum = card_value(cards)
    return [[cards], cardsum]


# Get card from deck and return that card and new sum
def hit_func(current_sum):
    new_card = draw_card()
    new_sum = current_sum + card_value(new_card)
    return [new_card, new_sum]

def is_over_limit(sum):
    if sum > 21:
        return True


class Button:
    def __init__(self, color, x, y, width, height):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, window, text, fontsize, outline = None):
        if outline:
            pygame.draw.rect(window, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)

        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height), 0)

        font = pygame.font.SysFont('comicsans', fontsize)
        text_label = font.render(text, 1, (250,250,250))
        window.blit(text_label, (self.x + (self.width/2 - text_label.get_width()/2), self.y + (self.height/2 - text_label.get_height()/2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x+ self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False



class Chips:
    def __init__(self, Total):
        self.Total = Total

    def win_bet(self):
        self.Total += 20

    def loose_bet(self):
        self.Total -= 20


def main():
    run = True #False
    FPS = 60
    clock = pygame.time.Clock()
    end = 0
    Player_Sum = 0
    Dealer_Sum = 0
    player_card_imgs = []
    dealer_card_imgs = []
    sum_font = pygame.font.SysFont("comicsans", 30)
    cards_font = pygame.font.SysFont("comicsans", 40)
    title_font = pygame.font.SysFont("comicsans", 47)
    chips_font = pygame.font.SysFont("comicsans", 23)
    lost_font = pygame.font.SysFont('comicsans', 50)
    hit_button = Button((0,0,255), 620, 250, 110, 40)
    stand_button = Button((0,0,255), 620, 300, 110, 40)
    main_menu_button = Button((0,0,0), 30, 30, 200, 40)
    DrawCards = Draw_cards(WIN)
    lost = False
    won = False
    lost_hand = False
    won_hand = False
    count = 0

    def redraw_window():
        WIN.blit(BG, (0, 0))
        WIN.blit(Chips_img, (80, 240))

        # Draw Text
        player_cards_label = cards_font.render("Player Cards", 1, (255, 255, 255))
        dealer_cards_label = cards_font.render("Dealer Cards", 1, (255, 255, 255))
        player_sum_label = sum_font.render(f"Player sum: {Player_Sum}", 1, (255, 255, 255))
        dealer_sum_label = sum_font.render(f"Dealer sum: {Dealer_Sum}", 1, (255, 255, 255))
        title_font_label = title_font.render("Lets play Blackjack!", 1, (255, 255, 255))
        chips_label = chips_font.render(f"Available chips: {chips.Total}", 1, (255, 255, 255))

        WIN.blit(player_sum_label, ((WIDTH/2) - (player_sum_label.get_width()/2), 355))
        WIN.blit(dealer_sum_label, ((WIDTH/2) - (dealer_sum_label.get_width()/2), 230))
        WIN.blit(dealer_cards_label, ((WIDTH / 2) - (dealer_cards_label.get_width() / 2), 80))
        WIN.blit(player_cards_label, ((WIDTH / 2) - (player_cards_label.get_width() / 2), 495))
        WIN.blit(title_font_label, (((WIDTH / 2) - (title_font_label.get_width() / 2) + 5), ((HEIGHT/2) - (title_font_label.get_height()/2))))
        WIN.blit(chips_label, (55, 325))

        hit_button.draw(WIN, "Hit!", 40, (0,0,0))
        stand_button.draw(WIN, "Stand", 40, (0,0,0))
        main_menu_button.draw(WIN, "Back to Main Menu", 25)

        DrawCards.player(player_card_imgs)
        DrawCards.dealer(dealer_card_imgs)

        if lost:
            lost_label = lost_font.render("You lost the hand!", 1, (255,255,255))
            pygame.draw.rect(WIN, (0,0,0), (200, 250, 400, 100), 0)
            WIN.blit(lost_label, ((400 - (lost_label.get_width()/2)), (300 - (lost_label.get_height()/2))))

        if won:
            won_label = lost_font.render("You won the hand!", 1, (255, 255, 255))
            pygame.draw.rect(WIN, (0, 0, 0), (200, 250, 400, 100), 0)
            WIN.blit(won_label, ((400 - (won_label.get_width() / 2)), (300 - (won_label.get_height() / 2))))

        pygame.display.update()

    [player_card_imgs, Player_Sum] = player_cards()
    [dealer_card_imgs, Dealer_Sum] = dealer_cards()
    #chips = Chips()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lost_hand:
             lost = True
             count += 1
        if won_hand:
            won = True
            count += 1
        if lost or won:
            if count <= FPS*2:
                continue
            else:
                lost = False
                won = False
                return "continue"

        lost_hand = False
        won_hand = False

        if chips.Total == 0:
            return "menu"

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if main_menu_button.isOver(pos):
                    return "menu"

                if hit_button.isOver(pos):
                    new_card, new_sum = hit_func(Player_Sum)
                    Player_Sum = new_sum
                    player_card_imgs += [new_card]
                    if is_over_limit(Player_Sum):
                        chips.loose_bet()
                        lost_hand = True

                if stand_button.isOver(pos):
                    while True:
                        new_card, new_sum = hit_func(Dealer_Sum)
                        Dealer_Sum = new_sum
                        dealer_card_imgs += [new_card]
                        time.sleep(0.5)
                        redraw_window()
                        if Dealer_Sum > Player_Sum or Dealer_Sum == 21:
                            if is_over_limit(Dealer_Sum) or (Dealer_Sum == Player_Sum):
                                chips.win_bet()
                                won_hand = True
                            else:
                                chips.loose_bet()
                                lost_hand = True
                            break

            if event.type == pygame.MOUSEMOTION:
                if hit_button.isOver(pos):
                    hit_button.color = (204,204,0)
                else:
                    hit_button.color = (0,0,255)

                if stand_button.isOver(pos):
                    stand_button.color = (204,204,0)
                else:
                    stand_button.color = (0,0,255)

                if main_menu_button.isOver(pos):
                    main_menu_button.color = (128,128,128)
                else:
                    main_menu_button.color = (0,0,0)


def instructions():
    title_font = pygame.font.SysFont('comicsans', 40)
    content_font = pygame.font.SysFont('comicsans', 22)
    main_menu_button = Button((0, 0, 0), 30, 30, 200, 40)
    run = True
    while run:
        WIN.blit(BG, (0,0))
        main_menu_button.draw(WIN, "Back to Main Menu", 25)
        title_label = title_font.render("Instructions:", 1, (255,255,255))
        content_label1 = content_font.render("1. Player has 100 chips at the start of the game.", 1, (255,255,255))
        content_label2 = content_font.render("2. Each bet is of 20 chips.", 1, (255, 255, 255))
        content_label3 = content_font.render("3. Sum of cards should be less than or equal to 21.", 1, (255, 255, 255))
        content_label4 = content_font.render("4. Player can either draw a card using Hit or give turn to dealer using Stand.", 1, (255, 255, 255))
        content_label5 = content_font.render("5. After player hits Stand, dealer draws cards till a hand is won/lost.", 1, (255, 255, 255))
        content_label6 = content_font.render("6. If dealer sum is less than 21 and more than player sum, player looses the hand.", 1, (255, 255, 255))
        content_label7 = content_font.render("7. If dealer sum exceeds 21, player wins the hand.", 1, (255, 255, 255))

        WIN.blit(title_label, ((400-(title_label.get_width()/2)), 120))
        WIN.blit(content_label1, (105, 190))
        WIN.blit(content_label2, (105, 210))
        WIN.blit(content_label3, (105, 230))
        WIN.blit(content_label4, (105, 250))
        WIN.blit(content_label5, (105, 270))
        WIN.blit(content_label6, (105, 290))
        WIN.blit(content_label7, (105, 310))

        pygame.display.update()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if main_menu_button.isOver(pos):
                    return "menu"

            if event.type == pygame.MOUSEMOTION:
                if main_menu_button.isOver(pos):
                    main_menu_button.color = (128, 128, 128)
                else:
                    main_menu_button.color = (0, 0, 0)



def main_menu():
    MainMenu = True
    while MainMenu:
        welcome_font = pygame.font.SysFont('comicsans', 70)
        start_button = Button((0, 0, 0), 280, 300, 250, 70)
        instructions_button = Button((0,0,0), 280, 380, 250, 70)
        run = True
        playing = False

        while run:
            WIN.blit(BG, (0, 0))
            welcome_label = welcome_font.render("Welcome to Blackjack!", 1, (255,255,255))
            WIN.blit(welcome_label, (145, 230))
            start_button.draw(WIN, "Begin Game", 40)
            instructions_button.draw(WIN, "Instructions", 40)

            pygame.display.update()

            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:
                    MainMenu = False
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.isOver(pos):
                        playing = True
                        run = False
                    if instructions_button.isOver(pos):
                        a = instructions()
                        if a == "quit":
                            MainMenu = False
                            run = False
                        elif a == "menu":
                            run = False

                if event.type == pygame.MOUSEMOTION:
                    if start_button.isOver(pos):
                        start_button.color = (128, 128, 128)
                    else:
                        start_button.color = (0, 0, 0)

                    if instructions_button.isOver(pos):
                        instructions_button.color = (128, 128, 128)
                    else:
                        instructions_button.color = (0, 0, 0)

        global chips
        chips = Chips(100)
        while playing:
            a = main()
            if a == "quit":
                playing = False
                MainMenu = False
            elif a == "menu":
                playing = False
            else:
                continue

    pygame.quit()


if __name__ == '__main__':
    main_menu()