from bge import logic
from link_scripts.PlayerConstants import PlayerState
from link_scripts.states.Ledge import pasteToLedgeGround

# ---------------------------------------------------------------------
# * Starter state
# ---------------------------------------------------------------------
def start_ladderFromTop(self):
	# set property
	self.suspendDynamics()
	self.grounded = False
	self.onLadder = True
	# reset state time
	self.stateTime = 0.0
	# set pos
	self.worldPosition[0] = self.ladderData[0].worldPosition[0]
	self.worldPosition[1] = self.ladderData[0].worldPosition[1]
	self.worldPosition[2] = self.ladderData[0].worldPosition[2] - 1.2
	self.orientation = self.ladderData[0].orientation
	# Animation
	self.rig.playSetLadderFromTop()
	# state
	self.switchState(PlayerState.START_LADDER_TOP_STATE)

def start_climbUpLadderState(self):
	# reset hud action text
	#self.playerHUD().resetActionText()
	self.rig.playLadderClimbUp()
	self.switchState(PlayerState.CLIMBUPLADDER_STATE)

def start_climbDownLadderState(self):
	# reset hud action text
	# self.playerHUD().resetActionText()
	self.rig.playLadderClimbDown()
	self.switchState(PlayerState.CLIMBDOWNLADDER_STATE)

def start_climbToGroundLadderState(self):
	# reset hud action text
	# self.playerHUD().resetActionText()
	self.rig.playLadderClimbToGround()
	self.switchState(PlayerState.CLIMB_TO_GROUND_LADDER_STATE)

def start_climbToIdleState(self):
	# reset hud action text
	# self.playerHUD().resetActionText()
	self.onLadder = False
	self.onGround = True
	self.physic.onGround()
	self.restoreDynamics()
	self.switchState(PlayerState.FALL_STATE)

def start_climbToFallState(self):
	# reset hud action text
	# self.playerHUD().resetActionText()
	self.onLadder = False
	self.restoreDynamics()
	self.switchState(PlayerState.FALL_STATE)

# End
def end_ladderState(self):
	# reset hud action text
	# self.playerHUD().resetActionText()
	self.onLadder = False
	self.restoreDynamics()

# ---------------------------------------------------------------------
# * Utils
# ---------------------------------------------------------------------
def isAlignToGround(self):
	if (self.worldPosition[2] >= self.ledgeGroundData[0][2] - 0.85):
		return True
	else:
		return False

# ---------------------------------------------------------------------
# * States
# ---------------------------------------------------------------------
def ladderTopState(self):
	frame = self.rig.getActionFrame(2)
	if (frame == 58):
		parent = self.ladderData[0].parent
		self.ladderData[0] = parent
		self.ladderData[1] = parent.orientation
		self.switchState(PlayerState.WAITLADDER_STATE)

def waitLadderState(self):
	# increment state time
	self.playStateTime(1)
	# if put to up key for climb to top
	if ( self.gamepad.isUpPressed() ):
		# go to climb up state
		start_climbUpLadderState(self)
	elif ( self.gamepad.isDownPressed() ):
		# go to climb down state
		start_climbDownLadderState(self)
	elif (self.stateTime == 1.0):
		# set action hud text
		# self.playerHUD().changeActionText('Lacher')
		if ( self.gamepad.isActionPressed()):
			# go to fall state
			start_climbToFallState(self)
	# else wait
	else:
		# play ladder wait animation
		self.rig.playLadderWait()

		ladder = self.ladderData[0]
		#set orientation to ledge

def climbToGroundLadderState(self):
	if ( self.rig.getActionFrame(2) == 39 ):
		# go to idle state
		end_ladderState(self)
		# base pose
		self.rig.playBasePose()
		# paste player to ground (simule the climb pos
		pasteToLedgeGround(self)
		# go to the ground
		self.grounded = True
		# go to idle state
		self.switchState(PlayerState.IDLE_STATE)


def climbDownLadderState(self):
	frame = self.rig.getActionFrame(2)
	if (frame != 0):
		# play step sound
		self.audio.playStepSound(self.rig.getActionFrame(2), [6, 14])
		# if detect the ground from down (the end)
		if ( self.tester.detectGround()):
			# climb
			start_climbToIdleState(self)
		else:
			# realistic movement
			if not (frame >= 6.0 and frame <= 9.0) and not (frame >= 14.0 and frame <= 17.0):
				self.worldPosition[2] -= 0.042
	else:
		# go to ladder state
		self.switchState(PlayerState.WAITLADDER_STATE)

def climbUpLadderState(self):
	frame = self.rig.getActionFrame(2)
	if (frame != 17):
		# play step sound
		self.audio.playStepSound(self.rig.getActionFrame(2), [6, 14])
		# if detect the ground (the end)
		if ( self.tester.detectLedgeGround(0.0) and isAlignToGround(self) ):
			# climb
			start_climbToGroundLadderState(self)
		else:
			# realistic movement
			if not (frame >= 6.0 and frame <= 9.0) and not (frame >= 14.0 and frame <= 17.0):
				self.worldPosition[2] += 0.042
	else:
		# go to ladder state
		self.switchState(PlayerState.WAITLADDER_STATE)
