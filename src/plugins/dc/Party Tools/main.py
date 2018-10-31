from nodeforge.PluginUtils import *
import random, difflib

class Main(Plugin):

    def onLoad(self):
        """
        Load the parser.
        """
        self.parse = self.core.findPlugin('NMDC Parser')


    def onData(self, txt):
        context = self.parse.context

        if context.cmd == '/roll':
            self.roll()
        elif context.cmd == '/fortune':
            context.reply(self.fortune())
        elif context.cmd == '/smack':
            self.smack()
            
     # roll a D&D dice
    def roll(self):
        context = self.parse.context
        
        try:
            die = context.args.split()[0].split('d')
            
            t = int(die[0])
            n = int(die[1])
            
            if ( t < 1 or t > 500 ) or ( n < 1 or n > 500 ):
                context.reply('Die must be between 1 and 500, ex. 5d24')
                return
            
        except Exception as e:
            context.reply('Parse Error ex. 5d24')
            return
        

        sum = 0
        for i in xrange(t):
            sum += random.randint(1,n)
        
        max = t*n-t
        
        if sum < (max*0.2+t):
            comment = ' You suck'
        elif sum > (max*0.8+t):
            comment = ' You hit for massive damage!'
        else:
            comment = ''
     
        context.reply( '"'+context.sender+'" rolled: '+str(sum)+comment )
     
     # smack someone
    def smack(self):
        context = self.parse.context
        dif = difflib.SequenceMatcher()    
        
        dif.set_seqs(self.parse.nick, context.args)
        
        try:
            if dif.quick_ratio() > .7:
               target = context.sender
            else:
               target = context.args
        except:
            context.reply('Specify a target')
        
        adj = ("a horrifying","a terrifying","an awesome","a splendid","a wonderful","a killer","a devastating","a spectacular")
        verb = ("rapes", "mutilates", "ravages", "slaps","mauls", "destroys", "bashes", "kills", "tortures","maims","violates")
        finish = ("choking him/her to death","shattering his/her backbone","ripping off his/her wo/manhood","forcing him/her to submission",
                  "knocking him/her out","squeezing the shit out of him/her","causing his nuts to explode","vaporizing him/her")
        
        move1 = (
                "Back Breaker Hold","Inverted Face Lock","Abdominal Stretch","Standing Achilles Tendon Hold","Reverse Ankle Lock",
                "Bridging Double Armbar","Rolling Crucifix","Step Over Armbar","Reverse Armbar with Neck Submission",
                "Crossed Arm Knee Back Breaker Hold","Inverted Shoulder Back Breaker Rack","Double Chickenwing","Back Mounted Chinlock",
                "Front Face Lock Choke Hold","Full Nelson","Entanglement Submission Hold","Spinning Inverted Facelock",
                "Standing Reverse Inverted Full Nelson","Back to Back Elevated Hammerlock","Angled Reverse Figure Four Leg Lock",
                "Arm Trap Standing Leg Lock","Inverted Indian Deathlock","Leg Lock with Bridging Chinlock",
                "Leg Lock with Reverse Inverted Full Nelson","Leg Lock with Underhook Neck Submission","Leg Trap Arm Hook",
                "Nerve Hold with Armbar","Grounded Octupus Hold","Spinning Cobra Clutch Sleeper Hold",
                "Step-Over Toe Hold Face Lock with Double Arm Lock","Belly to Back Wristlock", "3/4 Neckbreaker","Stunner",
                "Diamond Cutter","450 degree splash","Abdominal Stretch","Airplane Spin","Airplane Spin Toss","Majistral Cradle",
                "Amittyville Horror","Ankle Lock","Arm Bar","Arm Breaker","Arm Drag","Arm Lock","Arm Scissors","Arm Stretch","Hip Roll",
                "Hip Toss","Arm Wringer","Asai","Moonsault","Atomic Drop","Avalanche","Back Body Drop","Backbreaker","Back Fist","Back Rake",
                "Back Roll","BackRoll Press","Backslide","Back Suplex","Bear Hug","Bodyslam","Chop","Crossface","DDT","Dropkick","Fist Drop",
                "Flap Jack","Flatliner","Grapevine","Gutwrench","Cradle","Bulldog","Headlock","Facebuster","Knee","Katahajimi","Knee Drop",
                "Bell Clap","Hair Pull","Half Crab","Half Nelson","Hammerbomb","Hammerlock","Headbutt","Leg Sweep","Leg Drop","Leg Lock",
                "Leg Split","Leg Whip","Headlock","Headscissors","Head Vice","Superkick","Pancake","Pedigree","Pilebriver","Plancha","Pole Ram",
                "Punch","Quackensmash","Claw Hold","Rana","Reversal","Tarantula","Uppercut","Vaderbomb","Sunset Flip","Super Chokeslam",
                "Standing Double Grape Vine","Super Front Slam","Super Front Slam","Super Belly-To-Back Suplex","Superplex","Suplex Surfboard",
                "Super Belly-To-Belly Suplex","Surfboard Chinlock","Swan Dive","Swanton Bomb","Super Fisherman Buster","Tackle","Taz-Plex",
                "Texas Cloverleaf Swinging Neck Breaker","Thrust Kick","Tiger Bomb","Tiger Driver","Tazmission Taz-Plex","Tiger Driver '91",
                "Tiger Suplex Rope Walk","Tilt-A-Whirl Backbreaker","Toe Hold","Tombstone Piledriver","Tornado Punch","Tornado DDT","Torso Flip",
                "Torturer Crab","Tree Of Woe","Turnbuckle Bomb","Turnbuckle Smash","Tumbleweed Leg Drop Vertical Suplex","Victory Roll","Walking Crab",
                "Triple-Jump Moonsault","Whiplash","Whipper Snapper","Wrist Lock Abdominal Stretch","Armbar","Double Backbreaker",
                "Gaijin Smash"
                )
        
        rand = random.choice
        
        msg = '%s %s with %s %s, %s!' % (rand(verb), target, rand(adj), rand(move1), rand(finish))
        
        self.parse.emote(msg)
     
     # return a fortune
    def fortune(self):
        fort = ('Godly Luck',
                'Good Luck',
                'Average Luck',
                'Bad Luck',
                'Very Bad Luck',
                'You will meet a dark handsome stranger',
                'Good news will come to you by mail',
                'Better not tell you now',
                'Outlook Good',
                )
        
        return 'Your fortune: '+random.choice(fort)