from q3 import *
import check

def double_judge(bridge_game):
  '''
  Returns 0 if there is no double, and 2 for doulbe and 4 for redouble
  
  double_judge: Game -> (Anyof 0 or 2 or 4)
  '''
  if bridge_game.contract[1] is None:
    return 0
  elif bridge_game.contract[1].value == 'double':
    return 2
  else:
    return 4
def vulnerable_help(bridge_game):
  '''
  Returns True if bridge_game is vulnerable, otherwise, False
  
  vulnerable_help: Game -> Bool
  '''
  if bridge_game.declarer == 'North' or\
     bridge_game.declarer == 'South':
    if bridge_game.ns_vulnerable == True:
      return True
    else:
      return False
  else:
    if bridge_game.ew_vulnerable == True:
      return True
    else:
      return False
def penalty(bridge_game):
  '''
  Returns the scores once the contract is not made
  
  bridge_game: Game -> Int
  '''
  diff = 6 + int(bridge_game.contract[0].value) - bridge_game.declarer_tricks
  if vulnerable_help(bridge_game) == True:
    if double_judge(bridge_game) == 0:
      return diff * 100
    elif double_judge(bridge_game) == 2:
      if diff == 1:
        return 200
      else:
        return 200 + (diff - 1) * 300
    else:
      if diff == 1:
        return 400
      else:
        return 400 + (diff - 1) * 600
  else:
    if double_judge(bridge_game) == 0:
      return diff * 50
    elif double_judge(bridge_game) == 2:
      if diff == 1:
        return 100
      elif diff <= 3:
        return 100 + (diff - 1) * 200
      else:
        return 100 + 400 + (diff - 3) * 300
    else:
      if diff == 1:
        return 200
      elif diff <= 3:
        return 200 + (diff - 1) * 400  
      else:
        return 200 + 800 + (diff - 3) * 600
      
def score(bridge_game):
  '''
  Returns the score of a bridge game.
  
  score: Game -> Int
  
  Examples:
     P = [Player("North", []), Player("East", []),  
          Player("South", []), Player("West", [])]  
     G = Game([Bid("3", "NT"), None], "South", 
         "North", 9, P, False, False)
     score(G) => 400
     
     G = Game([Bid("4", "S"), None], "South", 
         "North", 11, P, False, True)
     score(G) => 450
  
     G = Game([Bid("4", "S"), Bid("double", None)], 
              "South", "North", 9, P, True, False)
     score(G) => -200
  '''
  
  ## made or exceeded their contract
  scores = 0
  number = bridge_game.declarer_tricks
  value = int(bridge_game.contract[0].value)
  
  if number < value + 6:
    scores = -1 * penalty(bridge_game)
  else:
    ## made or exceeded their contract
    if bridge_game.contract[0].suit == 'NT':
      contract_value = 40 + (value - 1) * 30
    elif bridge_game.contract[0].suit == 'C' or\
         bridge_game.contract[0].suit == 'D':
      contract_value = value * 20
    else:
      contract_value = value * 30
    
    if double_judge(bridge_game) == 2:
      contract_value = contract_value * 2
    elif double_judge(bridge_game) == 4:
      contract_value = contract_value * 4
    else:
      contract_value += 0
        
    scores += contract_value
  
    ## game bonus:
    if contract_value < 100:
      scores += 50
    else:
      if vulnerable_help(bridge_game) == True:
        scores += 500
      else:
        scores += 300
        
    ## Overtrick Points
    if number > value + 6:
      if double_judge(bridge_game) == 0:
        if bridge_game.contract[0].suit == 'C' or\
           bridge_game.contract[0].suit == 'D':
          scores += 20 * (number - value - 6)
        else:
          scores += 30 * (number - value - 6)
      elif double_judge(bridge_game) == 2:
        if vulnerable_help(bridge_game) == True:
          scores += 200 * (number - value - 6)
        else:
          scores += 100 * (number - value - 6)
      else:
        if vulnerable_help(bridge_game) == True:
          scores += 400 * (number - value - 6)
        else:
          scores += 200 * (number - value - 6)  
        
        
    ## Double/Redouble Contract Made Bunus
    if double_judge(bridge_game) == 2:
      scores += 50
    elif double_judge(bridge_game) == 4:
      scores += 100
    else:
      scores += 0
    
    ## Slam Bonus
    if value == 6:
      if vulnerable_help(bridge_game) == True:
        scores += 750
      else:
        scores += 500
    if value == 7:
      if vulnerable_help(bridge_game) == True:
        scores += 1500
      else:
        scores += 1000
  return scores

##Examples for score
P = [Player("North", []), Player("East", []),  Player("South", []),
     Player("West", [])]  
G = Game([Bid("3", "NT"), None], "South", 
    "North", 9, P, False, False)
check.expect("Example 1", score(G), 400)

G = Game([Bid("4", "S"), None], "South", 
    "North", 11, P, False, True)
check.expect("Example 2", score(G), 450)

G = Game([Bid("4", "S"), Bid("double", None)], "South", 
    "North", 9, P, True, False)
check.expect("Example 3", score(G), -200)

G = Game([Bid("4", "S"), Bid("double", None)], "South", 
    "North", 10, P, False, True)
check.expect("Example 4", score(G), 590)

G = Game([Bid("4", "S"), Bid("double", None)], "South", 
    "North", 10, P, True, True)
check.expect("Example 5", score(G), 790)

G = Game([Bid("4", "S"), Bid("double", None)], "South", 
    "North", 11, P, False, True)
check.expect("Example 6", score(G), 690)

G = Game([Bid("4", "S"), Bid("double", None)], "South", 
    "North", 9, P, False, True)
check.expect("Example 7", score(G), -100)

G = Game([Bid("4", "S"), Bid("redouble", None)], "South", 
    "North", 10, P, False, True)
check.expect("Example 8", score(G), 880)

G = Game([Bid("4", "S"), Bid("redouble", None)], "South", 
    "North", 11, P, False, True)
check.expect("Example 9", score(G), 1080)

G = Game([Bid("4", "S"), Bid("redouble", None)], "South", 
    "North", 5, P, False, True)
check.expect("Example 10", score(G), -2200)

G = Game([Bid("5", "NT"), Bid("redouble", None)], "South", 
    "North", 12, P, True, True)
check.expect("Example 11", score(G), 1640)


##To see the whole game in action, uncomment this to play!
##print(score(play_game_bootstrap()))
