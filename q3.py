from q2 import *
import check


PLAYERS = ["North", "East", "South", "West"]
PLAYERS_DICT = {"North":0, "East":1, "South":2, "West":3}
NUM_PLAYERS = len(PLAYERS)

HIGH_CARDS = ['J', 'Q', 'K', 'A']
SUITS = ['C', 'D', 'H', 'S']
VALUES = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 
          'J', 'Q', 'K']


class Game:
  '''
  Fields:
    contract (list Bid (anyof Bid None))
    cur_player (Str)
    declarer (Str)
    declarer_tricks (Nat)
    players (list Player Player Player Player)
    ns_vulnerable (Bool)
    ew_vulnerable (Bool)
  
  Requires:
      contract[0] is a numeric bid
      contract[1] is one of 
         None 
         Bid("double", None)
         Bid("redouble", None) or 
      cur_player is one of "North", "East", "South", "West"
      players.name are in some cyclic permutation of 
         "North", "East", "South", "West"
      declarer is one of the player names above
      0 &lt;=  declarer_tricks &lt;= 13
      players[k].hand have no repetition amongst the cards for all k.
  
  '''

  ##PROVIDED METHODS
  
  def __init__(self, ctract, start_player, declarer, d_tricks, the_players,
               ns_vul, ew_vul):
    '''
    Initialized a valid Bridge Game.
   
    Effects: Mutates self
  
    __init__: Game Str (anyof Str None) -> None
    Requires: Conditions from Fields above are met.
    '''
    self.contract = ctract
    self.cur_player = start_player
    self.players = the_players
    self.declarer = declarer
    self.declarer_tricks = d_tricks
    self.ns_vulnerable = ns_vul
    self.ew_vulnerable = ew_vul
  
  def __eq__(self, other):
    '''
    Returns if self and other are equal.
    All fields must be equal.
    
    __eq__: Game Any -> Bool
    '''
    return isinstance(other, Game) and\
           self.contract == other.contract and\
           self.cur_player == other.cur_player and\
           self.players == other.players and\
           self.declarer == other.declarer and\
           self.declarer_tricks == other.declarer_tricks and\
           self.ns_vulnerable == other.ns_vulnerable and\
           self.ew_vulnerable == other.ew_vulnerable
  
  
  def __repr__(self):
    '''
    Returns a string representation of Game
    
    __repr__: Game -> Str
    '''
    return ("Bridge Game:\n" + \
            "Contract: {0.contract}\n" + \
            "Current Player: {0.cur_player}\n" + \
            "Declarer: {0.declarer}\n" + \
            "Declarer Tricks: {0.declarer_tricks}\n" + \
            "Players: {0.players}\n" + \
            "NS Vulnerable?: {0.ns_vulnerable}\n" + \
            "EW Vulnerable?: {0.ew_vulnerable}\n"
            ).format(self)
  
  
  def trick_winner(self, trick):
    '''
    Returns the player who won the trick in the self Game.
    Also mutates self.cur_player to be the winner and
    possibly mutates self.declarer_tricks if declarer's
    team won the trick.
  
    Effects: 
       Mutates self.declarer_tricks
       Mutates self.cur_player
  
    trick_winner: Game (list Card Card Card Card) -> Str
    Requires: self.cur_player is the player that played the first card
    
    Examples:
       P = [Player("North", [Card("2", "D")]), 
            Player("East", [Card("5", "D")]),  
            Player("South", [Card("A", "D")]), 
            Player("West", [Card("K", "D")])]  
       G = Game([Bid("3", "S"), None], "East", "North", 0, P, False, False)
       G.trick_winner([Card("5", "D"), Card("A", "D"), 
                       Card("K", "D"), Card("2", "D")]) => "South"
       and G is mutated to:
       Game([Bid("3", "S"), None], "South", "North", 1, P, False, False)
                       
       P = [Player("North", [Card("2", "S")]), 
            Player("East", [Card("5", "D")]),  
            Player("South", [Card("A", "D")]), 
            Player("West", [Card("K", "D")])]  
       G = Game([Bid("3", "S"), None], "East", "North", 0, P, False, False)                       
       G.trick_winner([Card("5", "D"), Card("A", "D"), 
                       Card("K", "D"), Card("2", "S")]) => "North"
       and G is mutated to
       Game([Bid("3", "S"), None], "North", "North", 1, P, False, False)  
    '''
    trump = self.contract[0].suit
    trump_played = list(filter(lambda x: x.suit == trump, trick))
    if trump_played != []:
      max_val = max(list(map(lambda x: convert_value(x.value), 
                             trump_played)))
      max_card = list(filter(lambda x: convert_value(x.value) == max_val,
                             trump_played))[0]
    else:
      suit_led = trick[0].suit
      suit_followed = list(filter(lambda x: x.suit == suit_led, trick))
      max_val = max(list(map(lambda x: convert_value(x.value), 
                             suit_followed)))
      max_card = list(filter(lambda x: convert_value(x.value) == max_val,
                             suit_followed))[0]
      
    cur_player_index = PLAYERS_DICT[self.cur_player]
    player_index = ((trick.index(max_card) + cur_player_index)
                    % NUM_PLAYERS)
    winner = PLAYERS[player_index]
    
    dummy_name = who_is_dummy(self.declarer)
    if winner in [self.declarer, dummy_name]:
      self.declarer_tricks += 1
    self.cur_player = winner    
    
    return winner    

  ##FUNCTIONS TO COMPLETE:

  def save(self, file_name):
    '''
    Saves the contents of the Game self to file_name
    
    Effects: Writes to a file
    
    save: Game Str -> None
    
    P = [Player("North", [Card("2", "S")]), 
         Player("East", [Card("5", "D")]),  
         Player("South", [Card("A", "D")]), 
         Player("West", [Card("K", "D")])]     

    G = Game([Bid("3", "NT"), Bid("double", None)], "West", 
              "South", 12, P, False, False)

    G.save("testExample.txt") => None
    and the file "testExample.txt" contains:
    3
    NT
    double
    West
    South
    12
    False
    False
    1
    North
    2S
    East
    5D
    South
    AD
    West
    KD
    '''
    file = open(file_name,"w")
    file.write(self.contract[0].value + '\n')
    file.write(self.contract[0].suit + '\n')
    if self.contract[1] is None:
      file.write('None\n')
    else:
      file.write(self.contract[1].value + '\n')
    file.write(self.cur_player + '\n')
    file.write(self.declarer + '\n')
    file.write(str(self.declarer_tricks) + '\n')
    file.write(str(self.ns_vulnerable) + '\n')
    file.write(str(self.ew_vulnerable) + '\n')
    length = len(self.players[0].hand)
    file.write(str(length) + '\n')
    for player in self.players[0:4]:
      file.write(player.name + '\n')
      for cards in player.hand:
        file.write(cards.value + cards.suit + '\n')
    file.close()
##FUNCTIONS TO COMPLETE:
    
def load(file_name):
  '''
  Loads the contents of the Game self to file_name
  
  Effects: Reads from a file
  
  load: Str -> Game
  
  Example:
    load("testExample.txt") => 
       Game([Bid("3", "NT"), 
            Bid("double", None)], "West", "South", 12, 
            [Player("North", [Card("2", "S")]), 
             Player("East", [Card("5", "D")]),  
             Player("South", [Card("A", "D")]), 
             Player("West", [Card("K", "D")])] , 
            False, False)
       
    assuming the file "testExample.txt" contains:
    3
    NT
    double
    West
    South
    12
    False
    False
    1
    North
    2S
    East
    5D
    South
    AD
    West
    KD
  '''
  fin = open(file_name, 'r')
  all_names = fin.readlines()
  alist = []
  for line in all_names:
    alist.append(line.strip('\n'))
  if alist[2] == 'None':
    contract = [Bid(alist[0], alist[1]), None]
  else:
    contract = [Bid(alist[0], alist[1]), Bid(alist[2], None)]
  cur_player = alist[3]
  declarer = alist[4]
  declarer_tricks = alist[5]
  ns_vulnerable = alist[6]
  ew_vulnerable = alist[7]
  if ns_vulnerable == 'False':
    ns_vulnerable = False 
  else:
    ns_vulnerable = True
  if ew_vulnerable == 'False':
    ew_vulnerable = False 
  else:
    ew_vulnerable = True  
  
  P = []
  name = alist[9]
  pos = 10
  cards = []
  cards_num = int(alist[8])
  while pos < len(alist):
    cards.append(Card(alist[pos][0:(len(alist[pos]) - 1)], alist[pos][-1]))
    if len(cards) == cards_num:
      player = Player(name, cards)
      P.append(player)
      cards = []
      pos += 1
      if pos < len(alist):
        name = alist[pos]
    pos += 1
  
  fin.close()
  return Game(contract, cur_player, declarer, int(declarer_tricks), P,
              ns_vulnerable, ew_vulnerable)

def followed_suit(hand, card, suit_lead):
  '''
  Returns True if card follows suit, or if the player
  cannot follow the suit. False otherwise.
  
  followed_suit: (listof Card) Card (anyof Str None) -> Bool
  Requires:
     suit_lead is one of 'C', 'D', 'H', 'S'
     card in hand evaluates to True
     
  Examples:
     hand = [Card("A", "D"), Card("4", "C")]
     card = hand[1]
     followed_suit(hand, card, "C") => True

     hand = [Card("A", "D"), Card("4", "C")]
     card = hand[0]
     followed_suit(hand, card, "C") => False
     
     hand = [Card("A", "D"), Card("4", "C")]
     card = hand[0]
     followed_suit(hand, card, None) => True
  '''
  if suit_lead is None:
    return True
  else:
    if card.suit == suit_lead:
      return True
    else:
      for card in hand:
        if card.suit == suit_lead:
          return False
      return True
    
    
## PROVIDED FUNCTIONS

def load_game():
  '''
  Returns the loaded Game if a user wants to restore a game.
  Returns None otherwise.
  
  Effects:
     Reads from a file
     Prints to Screen
     Request input from user
  
  load_game: None -> (anyof None Game)
  '''
  load_game_prompt = "Do you want to load a game? (Y)es (N)o: "
  load_game_invalid = "Invalid Response"
  load_game_name_prompt = \
    "Name of game to load (Must be valid or program crashes!): "

  ans = input(load_game_prompt)
  while ans not in ['Y', 'N']:
    print(load_game_invalid)
    ans = input(load_game_prompt)
  if ans == "Y":
    file_name = input(load_game_name_prompt)
    return load(file_name)
  else:
    return None
    
def who_is_dummy(decl):
  '''
  Returns who the dummy is given the declarer decl
  
  who_is_dummy: Str -> Str
  Requires: dcl in PLAYERS
  '''
  ## dummy is opposite declarer
  dummy = PLAYERS[3] * int(PLAYERS[1] == decl) + \
          PLAYERS[1] * int(PLAYERS[3] == decl)  
  if decl in PLAYERS[::2]:
    dummy = PLAYERS[2] * int(PLAYERS[0] == decl) + \
            PLAYERS[0] * int(PLAYERS[2] == decl)
  return dummy


def valid_card(s):
  '''
  Returns True if s is in the format v + s
  where v is from VALUES and s is from SUITS
  
  valid_card: Str -> Bool
  '''
  val = s[:-1]
  suit = s[-1:]
  return val in VALUES and suit in SUITS

    
def select_card(bridge_game, trick, first, dummy_player, 
                declarer_player):
  '''
  Returns either the name of the saved game file or
  None based on a play of a card.
  bridge_game is the Bridge Game object
  trick is the current list of cards played in the trick
  first is True if this is the very first card played in the hand.
  dummy_player is the Player object corresponding to the dummy
  declarer_player is the Player object corresponding to the declarer
  
  Effects: 
     Mutates bridge_game (specifically players and hands)
     Possibly writes to a file if saves
     Prints to Screen
     Request input from user
  
  select_card: Game (listof Card) Bool Player Player -> (anyof Str None)
  Requires:
     dummy_player is the dummy Player object in bridge_game
     declarer_player is the declarer Player object in bridge_game
  '''
  play_card = "Player {0} please play a card from {1} hand."
  enter_card = \
    "Enter a valid card (eg. AS for ace of spades); follow suit if possible: "
  invalid_card = "Invalid Card"
  card_not_in_hand = "Error: Card not in hand"
  not_follow_suit = "Error: You must follow suit"
  dummy_hand = "{0}'s (Dummy's) hand:"
  your_hand = "{0}'s hand:"
  save_prompt = "Enter the name of your game to save: "

  which_hand = "your"
  if bridge_game.cur_player == dummy_player.name:
    which_hand = "dummy's"
    
  str_to_card  = lambda s: Card(s[:-1],s[-1])
  
  card = ""
  if trick == []:
    suit_lead = None
  else:
    suit_lead = trick[0].suit
    
  active_player = list(filter(
    lambda x: x.name == bridge_game.cur_player, bridge_game.players))[0]  
  
  while not valid_card(card) or \
        not followed_suit(active_player.hand, str_to_card(card), suit_lead):
    if active_player == dummy_player:
      print(play_card.format(declarer_player.name, which_hand))
    else:
      print(play_card.format(active_player.name, which_hand))
      
    if not first:
      print(dummy_hand.format(dummy_player.name))
      display_hand(dummy_player.hand)

    if active_player == dummy_player:
      ## Display declarer hand when dummy's turn
      print(your_hand.format(declarer_player.name))
      display_hand(declarer_player.hand)
    else:
      print(your_hand.format(active_player.name))
      display_hand(active_player.hand)
      
    card = input(enter_card)  
    if card == 'S' and trick == []:
      fin = input(save_prompt)
      bridge_game.save(fin)
      return fin
    if not valid_card(card):
      print(invalid_card)   
    else: 
      card_actual = str_to_card(card)
      if card_actual not in active_player.hand:
        print(card_not_in_hand)
        card = "not_in_hand"
      elif not followed_suit(active_player.hand, card_actual, suit_lead):
        print(not_follow_suit)    
      else: 
        active_player.play_card(card_actual)
  trick.append(card_actual)
  
def play_game_bootstrap():
  '''
  Plays a game of bridge and returns the final Game state 
  or the name of a saved file if the game is incomplete
  
  Effects:
     Reads/Writes to file
     Prints to Screen
     Request input from user
  
  play_game_bootstrap: None -> (anyof Game Str)
  '''
  invalid_response = "Invalid response."
  invalid_bid_response = "Invalid bid." 
  welcome = "Welcome to Bridge!"
  is_vulnerable_prompt = "Is the {0} team vulnerable? (Y)es or (N)o: "
  is_vulnerable = ['', '']
  start_game = "Begin playing!"
  dummy_msg = "Declarer is {0} and dummy is {1}"
  save_msg = "Type S to save at the beginning of a trick"
  end_hand = "End of hand"
  saved_msg = "Game Saved in {0}"

  
  print(welcome)
  bridge_game = load_game()
  
  if bridge_game == None:
    for i in range(NUM_PLAYERS//2):
      is_vulnerable[i] = input(is_vulnerable_prompt.format(
        PLAYERS[i] + '-' + PLAYERS[i+2]))
      while is_vulnerable[i] not in ['Y', 'N']:
        print(invalid_response)
        is_vulnerable[i] = input(is_vulnerable_prompt.format(
        PLAYERS[i] + '-' + PLAYERS[i+2]))
        
    ##Swap to boolean
    for i in range(NUM_PLAYERS//2): 
      if is_vulnerable[i] == 'Y':
        is_vulnerable[i] = True
      else:
        is_vulnerable[i] = False
        
    players_and_bids = bidding_bootstrap()
    players = players_and_bids[0]
    bids = players_and_bids[1]
    ctract = contract(bids)
    dealer = players[-1].name
    decl = declarer(dealer, bids)
    start_player = PLAYERS[(PLAYERS.index(decl) + 1 ) % NUM_PLAYERS]
    
    bridge_game = Game(ctract, start_player, decl, 0, players,
                       is_vulnerable[0], is_vulnerable[1]) 
    
  if bridge_game.contract == [Bid('pass', None), None]:
    print("All passed!")
    return bridge_game        
    
    
  print(start_game)
  dummy = who_is_dummy(bridge_game.declarer)
  print(dummy_msg.format(bridge_game.declarer, dummy))
  
  ## First card of round; can determine if no cards have been played!
  first = (len(bridge_game.players[0].hand) == 13)
  
  ##First round; no dummy initially

  dummy_player = list(filter(
    lambda x: x.name == dummy, bridge_game.players))[0] 
  declarer_player = list(filter(
    lambda x: x.name == bridge_game.declarer, bridge_game.players))[0] 
  
  while len(bridge_game.players[0].hand) != 0:
    trick = []
    print(save_msg)
    while len(trick) != 4:
      print("Current Trick: {0}".format(trick))
      saved = select_card(bridge_game, 
                          trick, first, dummy_player, declarer_player)
      if saved != None:
        print(saved_msg.format(saved))
        return saved
      bridge_game.cur_player = PLAYERS[
        (PLAYERS.index(bridge_game.cur_player) + 1 ) % NUM_PLAYERS]
      first = False
    first_player = bridge_game.cur_player
    winner = bridge_game.trick_winner(trick)
    print("First player: {0}".format(first_player))
    print("Trick: {0}".format(trick))
    print("Winner: {0}".format(winner))
    
  print(end_hand)
  return bridge_game
  
  
##Examples trick_winner

P = [Player("North", [Card("2", "D")]), 
     Player("East", [Card("5", "D")]),  
     Player("South", [Card("A", "D")]), 
     Player("West", [Card("K", "D")])]  
G = Game([Bid("3", "S"), None], "East", "North", 0, P, False, False)
##check.expect("Example 1", G.trick_winner([Card("5", "D"), Card("A", "D"), 
                ##Card("K", "D"), Card("2", "D")]), "South")
##check.expect("Example 1 mutation", G, 
             ##Game([Bid("3", "S"), None], "South", "North", 1, P, False, False))
             
                
P = [Player("North", [Card("2", "S")]), 
     Player("East", [Card("5", "D")]),  
     Player("South", [Card("A", "D")]), 
     Player("West", [Card("K", "D")])]  
G = Game([Bid("3", "S"), None], "East", "North", 0, P, False, False)   
##check.expect("Example 1",G.trick_winner([Card("5", "D"), Card("A", "D"), 
                ##Card("K", "D"), Card("2", "S")]), "North")
##check.expect("Example 1 mutation", G, 
             ##Game([Bid("3", "S"), None], "North", "North", 1, P, False, False))
             
             
##Example Save

##NOTE: Make sure you create the file "testExampleExpected.txt" with
##the following except for the quotes
'''
3
NT
double
West
South
12
False
False
1
North
2S
East
5D
South
AD
West
KD
'''

P = [Player("North", [Card("2", "S")]), 
     Player("East", [Card("5", "D")]),  
     Player("South", [Card("A", "D")]), 
     Player("West", [Card("K", "D")])]     

G = Game([Bid("3", "NT"), Bid("double", None)], "West", 
         "South", 12, P, False, False)

##Uncomment to test!
check.set_file_exact("testExample.txt", 
                     "testExampleExpected.txt")
check.expect("Testing Given Example", G.save("testExample.txt"), None)

P = [Player("North", [Card("2", "S"), Card("A", "C")]), 
     Player("East", [Card("5", "D"), Card("Q", "D")]),  
     Player("South", [Card("A", "D"), Card("J", "S")]), 
     Player("West", [Card("K", "D"), Card("10", "H")])]     

G = Game([Bid("3", "NT"), Bid("double", None)], "West", 
         "South", 5, P, False, False)

##Uncomment to test!
check.set_file_exact("testExample1.txt", 
                     "testExampleExpected1.txt")
check.expect("Testing Given Example", G.save("testExample1.txt"), None)
check.expect("Testing Given Example Load", load("testExampleExpected1.txt"), G)


##Example load
##Make sure you have the testExampleExpected file as above.

P = [Player("North", [Card("2", "S")]), 
     Player("East", [Card("5", "D")]),  
     Player("South", [Card("A", "D")]), 
     Player("West", [Card("K", "D")])]     

G = Game([Bid("3", "NT"), Bid("double", None)], "West", 
         "South", 12, P, False, False)

check.expect("Testing Given Example Load", load("testExampleExpected.txt"), G)

##Examples followed_suit

hand = [Card("A", "D"), Card("4", "C")]
card = hand[1]
check.expect("Basic Example", followed_suit(hand, card, "C"), True)

hand = [Card("A", "D"), Card("4", "C")]
card = hand[0]
check.expect("Basic Example", followed_suit(hand, card, "C"), False)

hand = [Card("A", "D"), Card("4", "C")]
card = hand[0]
check.expect("Basic Example", followed_suit(hand, card, None), True)

P = [Player("North", [Card("A", "C"), Card("2", "C"),
                      Card("3", "C"), Card("4", "C"), Card("5", "C"),
                      Card("6", "C"), Card("7", "C"), Card("8", "C"),
                      Card("9", "C"), Card("10", "C"), Card("J", "C"),
                      Card("Q", "C"), Card("K", "C")]),
     Player("East", [Card("A", "D"), Card("2", "D"),
                      Card("3", "D"), Card("4", "D"), Card("5", "D"),
                      Card("6", "D"), Card("7", "D"), Card("8", "D"),
                      Card("9", "D"), Card("10", "D"), Card("J", "D"),
                      Card("Q", "D"), Card("K", "D")]),  
     Player("South", [Card("A", "H"), Card("2", "H"),
                      Card("3", "H"), Card("4", "H"), Card("5", "H"),
                      Card("6", "H"), Card("7", "H"), Card("8", "H"),
                      Card("9", "H"), Card("10", "H"), Card("J", "H"),
                      Card("Q", "H"), Card("K", "H")]), 
     Player("West", [Card("A", "S"),  Card("2", "S"),
                      Card("3", "S"), Card("4", "S"), Card("5", "S"),
                      Card("6", "S"), Card("7", "S"), Card("8", "S"),
                      Card("9", "S"), Card("10", "S"), Card("J", "S"),
                      Card("Q", "S"), Card("K", "S")])]   

G = Game([Bid("3", "NT"), Bid("double", None)], "West", 
         "South", 0, P, False, False)

##Uncomment to test!
check.set_file_exact("testExample3.txt", 
                     "testExampleExpected3.txt")
check.expect("All", G.save("testExample3.txt"), None)
check.expect("All", load("testExampleExpected3.txt"), G)




P = [Player("North", [Card("2", "S")]), 
     Player("East", [Card("5", "D")]),  
     Player("South", [Card("A", "D")]), 
     Player("West", [Card("K", "D")])]     

G = Game([Bid("3", "NT"), None], "West", 
         "South", 12, P, False, False)
check.set_file_exact("testExample5.txt", 
                     "testExampleExpected5.txt")
check.expect("Testing Given Example", G.save("testExample5.txt"), None)
check.expect("Testing Given Example Load", load("testExampleExpected5.txt"), G)
