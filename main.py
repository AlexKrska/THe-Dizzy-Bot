from util.objects import *
from util.routines import *
from util.tools import find_hits  # Added a missing colon in the import statement

class Bot(GoslingAgent):
    def run(self):
        # If the bot already has an intent, do nothing and return
        if self.intent is not None:
            return

        # Check if the bot is in the kickoff phase
        if self.kickoff_flag:
            self.set_intent(kickoff())
            return

        # Checking distances from goals to balls and players
        Dbf_g = abs(self.ball.location.y - self.foe_goal.location.y)
        Dsf_g = abs(self.me.location.y - self.foe_goal.location.y)
        Dbm_g = abs(self.ball.location.y - self.friend_goal.location.y)
        Dsm_g = abs(self.me.location.y - self.friend_goal.location.y)

        # Distance from goal to goal
        Dm_g_f_g = abs(self.friend_goal.location.y - self.foe_goal.location.y)

####################################################################################################
        
        # Hitting Strategy (add it to an if statement for certain scenarios)
        targets = {
            'at_opponent_goal': (self.foe_goal.left_post, self.foe_goal.right_post),
            'away_from_our_net': (self.friend_goal.right_post, self.friend_goal.left_post)
        }
        hits = find_hits(self, targets)

        if len(hits['at_opponent_goal']) > 0:
            self.set_intent(hits['at_opponent_goal'][0])  
            return

        if len(hits['away_from_our_net']) > 0:
            self.set_intent(hits['away_from_our_net'][0])  
            return
        
###################################################################################################

        
        available_boosts = [boost for boost in self.boost if boost.large and boost.active]
    
        closest_boost = None
        closest_distance = 10000

        large_boosts = [boost for boost in available_boosts if (self.me.location - boost.location).magnitude() < 300]
        if len(large_boosts) > 0 and self.me.boost < 15:
            self.set_intent(goto(large_boosts[0]))
            return

        if self.me.boost < 1 and agent.time % 10 == 0:

            for boost in available_boosts:
                distance = (self.me.location - boost.location).magnitude()
                if closest_boost is None or distance < closest_distance:
                    closest_boost = boost
                    closest_distance = distance

            if closest_boost is not None:
                self.set_intent(goto(closest_boost.location)) 
                return
