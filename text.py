import pygame

class Text:
    CENTER = 1
    LEFT   = 2
    RIGHT  = 3
    def __init__( self, string, x, y ):
        self.mX = x
        self.mY = y
        self.mString = string
        self.mColor = ( 0, 0, 0 )
        font_height = 24
        self.mFont = pygame.font.SysFont( "Courier New", font_height )
        self.mAlign = Text.CENTER
        return

    def alignCenter(self):
        self.mAlign = Text.CENTER
        return

    def alignLeft(self):
        self.mAlign = Text.LEFT
        return

    def alignRight(self):
        self.mAlign = Text.RIGHT
        return

    def setText( self, string ):
        self.mString = string
        return

    def setColor( self, color ):
        self.mColor = color
        return

    def setSize( self, size ):
        self.mFont = pygame.font.SysFont( "Courier New", size )
        return

    def setFont( self, name, size ):
        self.mFont = pygame.font.SysFont( name, size )
        return

    def draw( self, surface ):
        text_object = self.mFont.render( self.mString, False, self.mColor )
        text_rect = text_object.get_rect( )
        if self.mAlign == Text.CENTER:
            text_rect.center = ( int( self.mX ), int( self.mY ) )
        elif self.mAlign == Text.RIGHT:
            text_rect.right = int( self.mX )
            text_rect.centery = int( self.mY )
        elif self.mAlign == Text.LEFT:
            text_rect.left = int( self.mX )
            text_rect.centery = int( self.mY )
        else:
            raise Exception("Text align misconfigured")
        surface.blit( text_object, text_rect )
        return
