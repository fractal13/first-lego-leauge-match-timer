import pygame
import game
import timer

# YOU SHOULD CONFIGURE THESE TO MATCH YOUR GAME
# window title bar text
TITLE = "Match Timer"
# pixels width
WINDOW_WIDTH  = 1920
# pixels high
WINDOW_HEIGHT = 1080
# frames per second
DESIRED_RATE  = 60

class PygameApp( game.Game ):

    def __init__( self, title, width, height, frame_rate ):

        game.Game.__init__( self, title, width, height, frame_rate )
        
        # create a game instance
        # YOU SHOULD CHANGE THIS TO IMPORT YOUR GAME MODULE
        self.mGame = timer.Timer( width, height )
        return
        
        
    def game_logic( self, keys, newkeys, buttons, newbuttons, mouse_position, dt ):
        # keys contains all keys currently held down
        # newkeys contains all keys pressed since the last frame
        # Use pygame.K_? as the keyboard keys.
        # Examples: pygame.K_a, pygame.K_UP, etc.
        # if pygame.K_UP in newkeys:
        #    The user just pressed the UP key
        #
        # buttons contains all mouse buttons currently held down
        # newbuttons contains all buttons pressed since the last frame
        # Use 1, 2, 3 as the mouse buttons
        # if 3 in buttons:
        #    The user is holding down the right mouse button
        #
        # mouse_position contains x and y location of mouse in window
        # dt contains the number of seconds since last frame
        
        x = mouse_position[ 0 ]
        y = mouse_position[ 1 ]

        # Update the state of the game instance
        # YOU SHOULD CHANGE THIS TO IMPORT YOUR GAME MODULE
        if pygame.K_a in newkeys:
            self.mGame.actOnPressA( )
        if pygame.K_b in newkeys:
            self.mGame.actOnPressB( )
        if pygame.K_p in newkeys:
            self.mGame.actOnPressP( )
        if pygame.K_t in newkeys:
            self.mGame.actOnPressT( )
        if pygame.K_UP in newkeys:
            self.mGame.actOnPressUp( )
        if pygame.K_DOWN in newkeys:
            self.mGame.actOnPressDown( )

        self.mGame.evolve( dt )

        return
    
    def paint( self, surface ):
        # Draw the current state of the game instance
        self.mGame.draw( surface )
        return

def main( ):
    pygame.font.init( )
    pygame.mixer.init( )
    game = PygameApp( TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, DESIRED_RATE )
    pygame.display.toggle_fullscreen( )
    game.main_loop( )
    
if __name__ == "__main__":
    main( )
