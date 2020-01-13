import pygame
import text
import math
import time

class Timer:

    # Time States
    NOT_COUNTING = 0    # Ready for pregame to begin.
    SETUP_COUNTING = 1  # Pregame countdown is running.
    MATCH_COUNTING = 2  # Game countdown is running.
    MATCH_OVER = 3      # Game has finished, waiting for reset.

    FULL_SETUP_TIME    = 60
    FULL_MATCH_TIME    = 150
    FULL_ENDMATCH_TIME = 30

    TEST_SETUP_TIME    = 5
    TEST_MATCH_TIME    = 10
    TEST_ENDMATCH_TIME = 3

    MAIN_CLOCK_SIZE    = 0.70 # fraction of screen height
    WALL_CLOCK_SIZE    = 0.15 # fraction of screen height
    ROUND_SIZE         = 0.15 # fraction of screen height

    def __init__( self, width, height ):
        # Define length of game periods
        self.mSetupTime   = Timer.FULL_SETUP_TIME
        self.mMatchTime   = Timer.FULL_MATCH_TIME
        self.mEndGameTime = Timer.FULL_ENDMATCH_TIME

        # display dimensions
        self.mWidth = width
        self.mHeight = height
        
        # Wall-clock
        wall_size = int(self.mHeight * Timer.WALL_CLOCK_SIZE)
        self.mWallClock = text.Text( "0:00 AM", int(0.95*self.mWidth), self.mHeight - wall_size )
        self.mWallClock.setFont( "latinmodernromancaps", wall_size )
        self.mWallClock.alignRight()

        # Round Number
        self.mRoundNumber = 0
        round_size = int(self.mHeight * Timer.ROUND_SIZE)
        self.mRoundNumberText = text.Text( "Round: 0", int(0.05*self.mWidth), self.mHeight - round_size )
        self.mRoundNumberText.setFont( "latinmodernromancaps", round_size )
        self.mRoundNumberText.alignLeft()

        # Font selection and clock placement
        size = int(self.mHeight * Timer.MAIN_CLOCK_SIZE)
        y    = int(0.50*self.mHeight) - int(max(wall_size,round_size))
        self.mText = text.Text( "0:00", int(0.50*self.mWidth), y )
        self.mText.setFont( "latinmodernromancaps", size )

        # Color selection
        self.mSetupBackground = ( 255, 255, 0 )  # yellow
        self.mSetupColor = ( 0, 0, 0 )

        self.mMatchBackground = ( 0, 255, 0 )    # green
        self.mMatchColor = ( 0, 0, 0 )
        
        self.mBackground = self.mSetupBackground

        self.mText.setColor( self.mSetupColor )
        self.mWallClock.setColor( self.mSetupColor )
        self.mRoundNumberText.setColor( self.mSetupColor )
        self.reset( )
        self.setText( )

        # beginning of match
        self.mStartSound = pygame.mixer.Sound( "wav/start.wav" )
        # end of match
        self.mEndSound = pygame.mixer.Sound( "wav/end.wav" )
        # 30 seconds to go sound
        self.mEndGameSound = pygame.mixer.Sound( "wav/end-game.wav" )
        # early termination
        self.mStopSound = pygame.mixer.Sound( "wav/stop.wav" )

        return

    def setText( self ):
        # I've tried to stop 1:00 from going to 0:60, but unsuccessfully.
        
        # minutes = math.floor( self.mTimeRemaining / 60 )
        # seconds = math.ceil( self.mTimeRemaining - minutes * 60 )
        
        minutes = self.mTimeRemaining // 60
        seconds = 0.99 + self.mTimeRemaining - minutes * 60
        
        
        self.mWallClock.setText( time.strftime("%I:%M %p",time.localtime()) )
        if self.mRoundNumber > 0:
            s = "Round: %d" % (self.mRoundNumber,)
        else:
            s = "Round: 0"
        self.mRoundNumberText.setText(s)

        if False:
            # Tried to display 1/10 of seconds, but removed for now.
            deciseconds = int( 10 * ( self.mTimeRemaining - minutes * 60 - seconds ) )
            s = "%01d:%02d.%01d" % ( minutes, seconds, deciseconds )
            self.mText.setText( s )            
        else:
            s = "%01d:%02d" % ( minutes, seconds, )
            self.mText.setText( s )
            if self.mCounting == Timer.NOT_COUNTING:
                self.mText.setColor( self.mSetupColor )
                self.mBackground = self.mSetupBackground
            elif self.mCounting == Timer.SETUP_COUNTING:
                self.mText.setColor( self.mSetupColor )
                self.mBackground = self.mSetupBackground
            elif self.mCounting == Timer.MATCH_COUNTING:
                self.mText.setColor( self.mMatchColor )
                self.mBackground = self.mMatchBackground
            elif self.mCounting == Timer.MATCH_OVER:
                self.mText.setColor( self.mMatchColor )
                self.mBackground = self.mMatchBackground

        return

    # back to the beginning of pregame
    def reset( self ):
        self.mTimeRemaining = self.mSetupTime
        self.mCounting = Timer.NOT_COUNTING
        self.mHavePlayedEndGame = False
        return

    # start pregame countdown
    def actOnPressA( self ):
        if self.mCounting == Timer.NOT_COUNTING:
            self.mCounting = Timer.SETUP_COUNTING
        return

    # back to beginning of pregame, only if countdown has finished
    def actOnPressB( self ):
        if self.mCounting == Timer.MATCH_OVER:
            self.mRoundNumber += 1
            self.reset( )
        return

    # toggle test mode
    def actOnPressT( self ):
        if self.mCounting == Timer.NOT_COUNTING:
            if self.mSetupTime == Timer.TEST_SETUP_TIME:
                self.mSetupTime   = Timer.FULL_SETUP_TIME
                self.mMatchTime   = Timer.FULL_MATCH_TIME
                self.mEndGameTime = Timer.FULL_ENDMATCH_TIME
            else:
                self.mSetupTime   = Timer.TEST_SETUP_TIME
                self.mEndGameTime = Timer.TEST_ENDMATCH_TIME
                self.mMatchTime   = Timer.TEST_MATCH_TIME
            self.reset( )
        return

    # early termination, back to beginning of pregame
    def actOnPressP( self ):
        if self.mCounting == Timer.SETUP_COUNTING or self.mCounting == Timer.MATCH_COUNTING:
            self.mStopSound.play()
            self.reset( )
        return

    # increase round number
    def actOnPressUp( self ):
        if self.mCounting == Timer.NOT_COUNTING:
            self.mRoundNumber += 1
        return

    # decrease round number
    def actOnPressDown( self ):
        if self.mCounting == Timer.NOT_COUNTING:
            self.mRoundNumber -= 1
            if self.mRoundNumber < 0:
                self.mRoundNumber = 0
        return

    # update all status based on time change (dt)
    def evolve( self, dt ):
        if self.mCounting == Timer.NOT_COUNTING:
            pass
        elif self.mCounting == Timer.SETUP_COUNTING:
            self.mTimeRemaining -= dt
            if self.mTimeRemaining <= 0:
                self.mTimeRemaining = self.mMatchTime
                self.mCounting = Timer.MATCH_COUNTING
                self.mStartSound.play()
        elif self.mCounting == Timer.MATCH_COUNTING:
            self.mTimeRemaining -= dt
            if self.mTimeRemaining <= self.mEndGameTime and (not self.mHavePlayedEndGame):
                self.mEndGameSound.play()
                self.mHavePlayedEndGame = True
            if self.mTimeRemaining <= 0:
                self.mTimeRemaining = 0
                self.mCounting = Timer.MATCH_OVER
                self.mEndSound.play()
        elif self.mCounting == Timer.MATCH_OVER:
            pass

        self.setText( )
        return

    # draws the current state of the system
    def draw( self, surface ):
        
        # rectangle to fill the background
        rect = pygame.Rect( int ( 0 ), int ( 0 ), int ( self.mWidth ), int ( self.mHeight ) )
        
        pygame.draw.rect( surface, self.mBackground, rect, 0 )

        self.mText.draw( surface )
        self.mWallClock.draw( surface )
        self.mRoundNumberText.draw( surface )

        return
