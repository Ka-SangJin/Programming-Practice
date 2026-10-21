class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
    
    def __str__(self):
        return f'{self.suit} {self.value}'
    
    def get_value(self):
        if self.value in ['J','Q','K']:
            return 10
        elif self.value == 'A':
            return 11
        else:
            return int(self.value)
        
import random

class Deck:
    def __init__(self):
        self.cards = []
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']

        for suit in suits:
            for value in values:
                self.cards.append(Card(suit,value))
        
    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        if len(self.cards)>0:
            return self.cards.pop()
        else:
            return None

class Hand:
    def __init__(self):
        self.cards = [] 
    
    def blackjack(self):
        return len(self.cards) == 2 and self.getscore() == 21

    def getcard(self, card):
        self.cards.append(card) 

    def getscore(self):
        score = 0
        ace = 0 
        for card in self.cards:
            score += card.get_value()
            if card.value == 'A':
                ace += 1
        #21점 이상이면
        while score > 21 and ace > 0:
            score -= 10
            ace -= 1
        return score


    def __str__(self):
        s = ''
        for card in self.cards:
            s += str(card) + '  '
        return s.strip()


class Player:
    def __init__(self, name='Player'):
        self.name = name
        self.hand = Hand()  
        self.chip = 100 

    def bust(self):
        return self.hand.getscore() > 21

    def hit(self, deck):
        card = deck.deal()
        if card is not None:
            self.hand.getcard(card)
        return card
    
    def reset_hand(self):
        self.hand = Hand()

    def __str__(self):
        return self.name + '의 카드: ' + str(self.hand) + '\n점수: ' + str(self.hand.getscore())


class Dealer(Player):
    def __init__(self):
        Player.__init__(self, 'Dealer')

    def play(self, deck):
        print("딜러의 카드:", self.hand)
        print("딜러 점수:", self.hand.getscore())
        while True:
            now = self.hand.getscore()
            if now >= 17:
                break
            print("딜러가 카드를 뽑습니다:", end=' ')
            card = self.hit(deck)
            print(card)
            print("딜러의 카드:", self.hand)
            print("딜러 점수:", self.hand.getscore())

class Game:
    def __init__(self):
        print("블랙잭 게임에 오신 것을 환영합니다!")
        name = input("이름을 입력하세요: ")
        self.player = Player(name)
        self.dealer = Dealer()

    def start(self):
        while True: #칩이 없을때까지
            if self.player.chip <= 0:
                print("칩이 모두 소진되었습니다. 게임을 종료합니다.")
                break

            print("\n현재 칩:", self.player.chip)
            print("배팅할 금액을 입력하세요: ", end='')
            while True:
                try:
                    coin = int(input())
                    if coin > 0 and coin <= self.player.chip:
                        break
                    else:
                        print("잘못된 금액입니다.")
                except:
                    print("숫자를 입력하세요.")

            from random import shuffle
            self.deck = Deck()
            self.deck.shuffle()
            self.player.reset_hand()
            self.dealer.reset_hand()

            self.player.hit(self.deck)
            self.player.hit(self.deck)
            self.dealer.hit(self.deck)
            self.dealer.hit(self.deck)

            print("\n" + str(self.player))
            print("딜러의 카드:", self.dealer.hand.cards[0], ", Hidden\n")

            if self.player.hand.blackjack():
                print("블랙잭! 이겼습니다.\n")
                self.player.chip += coin
                continue
            # 플레이어 턴
            while True:
                try:
                    move = input("히트(h) 또는 스탠드(s)를 선택하세요: ")
                    if move == 'h':
                        self.player.hit(self.deck)
                        print(self.player)
                        if self.player.bust():
                            print("버스트! 졌습니다.\n")
                            self.player.chip -= coin
                            break
                    elif move == 's':
                        break
                    else:
                        raise Exception("h 또는 s만 입력하세요.")
                except Exception as e:
                    print(e)

            # 딜러 턴
            if not self.player.bust():
                self.dealer.play(self.deck)

                playerscore = self.player.hand.getscore()
                dealerscore = self.dealer.hand.getscore()
                print()
                print(self.player.name + " 점수:", playerscore)
                print("딜러 점수:", dealerscore)

                if dealerscore > 21:
                    print("딜러 버스트! 이겼습니다!\n")
                    self.player.chip += coin
                elif playerscore > dealerscore:
                    print("이겼습니다!\n")
                    self.player.chip += coin
                elif playerscore < dealerscore:
                    print("졌습니다.\n")
                    self.player.chip -= coin
                else:
                    print("무승부입니다.\n")

            if self.player.chip <= 0:
                print("칩이 모두 소진되었습니다. 게임을 종료합니다.")
                break

            while True:
                again = input("다시 플레이하시겠습니까? (y/n): ")
                if again == 'y':
                        break  
                elif again == 'n':
                    print("게임 종료! 최종 칩:", self.player.chip)
                    return 
                else:
                    print("잘못된 입력입니다. y 또는 n으로 입력하세요.")

if __name__ == '__main__':
    game = Game()
    game.start()