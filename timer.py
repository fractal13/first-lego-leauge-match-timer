import pygame
import text
import math

class Timer:

    NOT_COUNTING = 0
    SETUP_COUNTING = 1
    MATCH_COUNTING = 2
    MATCH_OVER = 3

    def __init__( self, width, height ):
        #print( pygame.font.get_fonts( ) )
        self.mSetupTime = 60
        self.mEndGameTime = 30
        self.mMatchTime = 150
        self.mWidth = width
        self.mHeight = height
        self.mText = text.Text( "0:00", self.mWidth / 2, self.mHeight / 2 )
        self.mText.setFont( "latinmodernromancaps", 600 )

        self.mSetupBackground = ( 255, 255, 0 )
        self.mSetupColor = ( 0, 0, 0 )

        self.mMatchBackground = ( 0, 255, 0 )
        self.mMatchColor = ( 0, 0, 0 )
        
        self.mBackground = self.mSetupBackground

        self.mText.setColor( self.mSetupColor )
        self.reset( )
        self.setText( )

        # beginning of match
        self.mStartSound = pygame.mixer.Sound( "wav/start.wav" )
        # end of match
        self.mEndSound = pygame.mixer.Sound( "wav/end.wav" )
        # 30 seconds to go sound
        self.mEndGameSound = pygame.mixer.Sound( "wav/end-game.wav" )
        # unused
        self.mStopSound = pygame.mixer.Sound( "wav/stop.wav" )

        return

    def setText( self ):
        # minutes = math.floor( self.mTimeRemaining / 60 )
        # seconds = math.ceil( self.mTimeRemaining - minutes * 60 )
        
        minutes = self.mTimeRemaining // 60
        seconds = 0.99 + self.mTimeRemaining - minutes * 60
        
        if False:
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

    def reset( self ):
        self.mTimeRemaining = self.mSetupTime
        self.mCounting = Timer.NOT_COUNTING
        self.mHavePlayedEndGame = False
        return

    def actOnPressA( self ):
        if self.mCounting == Timer.NOT_COUNTING:
            self.mCounting = Timer.SETUP_COUNTING
        return

    def actOnPressB( self ):
        if self.mCounting == Timer.MATCH_OVER:
            self.reset( )
        return

    def actOnPressT( self ):
        if self.mCounting == Timer.NOT_COUNTING:
            if self.mSetupTime == 5:
                self.mSetupTime = 60
                self.mEndGameTime = 30
                self.mMatchTime = 150
            else:
                self.mSetupTime = 5
                self.mEndGameTime = 3
                self.mMatchTime = 10
            self.reset( )
            
        return

    def actOnPressP( self ):
        if self.mCounting == Timer.SETUP_COUNTING or self.mCounting == Timer.MATCH_COUNTING:
            self.mStopSound.play()
            self.reset( )
        return

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

        return
