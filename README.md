# first-lego-leauge-match-timer
This is a match timer for use in FIRST Lego League matches.

# Program flow

A match has at least 1:00 of pregame setup time.  A match has 2:30 
game time, with the last 0:30 being "end game".  Once the operator
starts the pregame countdown, the program will count the pregame
time to 0, and automatically start the game counter.  The start
game sound is played at that time.  When the end game is reached,
the end game sound will play.  Finally, when the game has finished,
the match end sound will play.

The operator must manually reset the timer back to the beginning of
pregame setup.  If the countdown needs to be terminated for any reason,
the operator may do so.

# Controls

* `a` - Start the pregame 1:00 countdown
* `b` - Reset the clock to pregame status
* `p` - Early terminate the countdown, reset the clock to pregame status
* `t` - Toggle test mode.  In test mode, pregame is 5 seconds, game
  is 10 seconds, and end game starts with 3 seconds left.

# Source

The source code is written in python, with python 3 assumed.
It uses [pygame](pygame.org) for user interface.  `pip` is recommended
for installation of pygame.

# Sound files

The sound files were taken from some other FLL project.  I hope
I'm not violating copyright. If so, please contact me.

The [mp3 folder](mp3/) contains original mp3 format files, but
is not actually used by the program.  The [wav folder][wav/] files
are the ones actually used.

* [start.wav](wav/start.wav) is used for the beginning of the 2:30 match.
* [end.wav](wav/end.wav) is used for the end of the 2:30 match.
* [end-game.wav](wav/end-game.wav) is used to mark the "end game"
  period with 0:30 left in the match.
* [stop.wav](wav/stop.wav) is used to denote early termination of a
  match, such as in the case of a false start.


  

