"""
Sound Pool Class

This class provides a convenient way of managing sounds in an environment,  with 1, 2 and 3 dimensions. It uses the functions found in sound_positioning.py to do the actual sound adjustments, so modifying these functions will affect the entire system. The sound_pool_item class holds all the information necessary for one single sound in the game world. Note that you should not make instances of the sound_pool_item class directly but always use the methods and properties provided in the sound_pool class.
"""

from AGK.audio import sound_positioning as sp
from AGK.audio import sound
class sound_pool_item(object):
	def __init__(self):
		self.sound=sound.sound()
		self.filename=""
		self.x=0.0
		self.y=0.0
		self.z=0.0
		self.looping=False
		self.pan_step=0.0
		self.volume_step=0.0
		self.behind_pitch_decrease=0.0
		self.start_pan=0.0
		self.start_volume=0.0
		self.start_pitch=0.0
		self.upper_range=0
		self.lower_range=0
		self.forward_range=0
		self.backward_range=0
		self.left_range=0
		self.right_range=0
		self.is_3d=False
		self.paused=False
		self.stationary=False
		self.persistent=False
	# This method updates the sound, checking if it should be closed do to out of earshot conditions etc. 
	def update(self, listener_x, listener_y, listener_z, rotation, max_distance):
		if self.sound == None:
			return
		if max_distance>0 and self.looping==True:
			total_distance=self.get_total_distance(listener_x, listener_y, listener_z)
			if total_distance > max_distance:
				self.sound.stop()
				return
			if total_distance <= max_distance:
				try:
					self.sound.load(self.filename)
					self.update_listener_position(listener_x, listener_y, listener_z, rotation)
					if paused == False:
						self.sound.play_looped()
				except:
					pass
		self.update_listener_position(listener_x, listener_y, listener_z, rotation)
	# This method recalculates the position parameters including the ranges, if any. It then calls the appropriate sound positioning function on the sound handle. 
	def update_listener_position(self, listener_x, listener_y, listener_z, rotation):
		if self.sound == None:
			return
		if self.stationary:
			return
		delta_left = self.x - self.left_range
		delta_right = self.x + self.right_range
		delta_backward = self.y - self.backward_range
		delta_forward = self.y + self.forward_range
		delta_upper = self.z + self.upper_range
		delta_lower = self.z - self.lower_range
		true_x = listener_x
		true_y = listener_y
		true_z = listener_z
		if self.is_3d == False:
			if listener_x >= delta_left and listener_x <= delta_right:
				sp.position_sound_custom_1d(self.sound.handle, listener_x, listener_x, self.pan_step, self.volume_step, self.start_pan, self.start_volume)
				return
			if listener_x < delta_left:
				sp.position_sound_custom_1d(self.sound.handle, listener_x, delta_left, self.pan_step, self.volume_step, self.start_pan, self.start_volume)
			if listener_x > delta_right:
				sp.position_sound_custom_1d(self.sound.handle, listener_x, delta_right, self.pan_step, self.volume_step, self.start_pan, self.start_volume)
			return
		if listener_x < delta_left:
			true_x = delta_left
		elif listener_x > delta_right:
			true_x = delta_right
		if listener_y < delta_backward:
			true_y = delta_backward
		elif listener_y > delta_forward:
			true_y = delta_forward
		if listener_z < delta_lower:
			true_z = delta_lower
		elif listener_z > delta_upper:
			true_z = delta_forward
		sp.position_sound_custom_3d(self.sound.handle, listener_x, listener_y, listener_z, true_x, true_y, true_z, rotation, self.pan_step, self.volume_step, self.behind_pitch_decrease, 0.0, 0.0, 0.0, self.start_pan, self.start_volume, self.start_pitch)
	# This method returns the total distance between the current sound and the listener in space. This is used to calculate in and out of earshot conditions.
	def get_total_distance(self, listener_x, listener_y, listener_z):
		if self.stationary:
			return 0
		delta_left = self.x - self.left_range
		delta_right = self.x + self.right_range
		delta_backward = self.y - self.backward_range
		delta_forward = self.y + self.forward_range
		delta_upper = self.z + self.upper_range
		delta_lower = self.z - self.lower_range
		true_x = listener_x
		true_y = listener_y
		true_z = listener_z
		distance=0
		if self.is_3d == False:
			if listener_x >= delta_left and listener_x <= delta_right:
				return 0
			if listener_x < delta_left:
				distance = delta_left - listener_x
			if listener_x > delta_right:
				distance = listener_x - delta_right
			return distance
		if listener_x < delta_left:
			true_x = delta_left
		elif listener_x > delta_right:
			true_x = delta_right
		if listener_y < delta_backward:
			true_y = delta_backward
		elif listener_y > delta_forward:
			true_y = delta_forward
		if listener_z < delta_lower:
			true_z = delta_lower
		elif listener_z > delta_upper:
			true_z = delta_forward
		if listener_x < true_x:
			distance = (true_x - listener_x)
		if listener_x > true_x:
			distance = (listener_x - true_x)
		if listener_y < true_y:
			distance += (true_y - listener_y)
		if listener_y > true_y:
			distance += (listener_y - true_y)
		if listener_z < true_z:
			distance += (true_z - listener_z)
		if listener_z > true_z:
			distance += (listener_z - true_z)
		return distance

#This is the actual sound_pool class. For more information on how to use the class, please see the AGK3's sound_pool example in directory examples/sound_pool_test.py
class sound_pool(object):
	# this is the default constructor
	def __init__(self):
		self.items=[]
		for i in range(100):
			x=sound_pool_item()
			self.items.append(x)
		self.max_distance=0
		self.pan_step=1.0
		self.volume_step=1.0
		self.behind_pitch_decrease=0.25
		self.last_listener_x=0
		self.last_listener_y=0
		self.last_listener_z=0
		self.last_listener_rotation=0.0
		self.highest_slot=0
		self.clean_frequency=3
	def __init__(self, number_of_items):
		self.items=[]
		for i in range(number_of_items):
			x=sound_pool_item()
			self.items.append(x)
		self.max_distance=0.0
		self.pan_step=1.3
		self.volume_step=0.5
		self.behind_pitch_decrease=0.25
		self.last_listener_x=0
		self.last_listener_y=0
		self.last_listener_z=0
		self.last_listener_rotation=0.0
		self.highest_slot=0
		self.clean_frequency=3
	
	# play_stationary function. Works the same as bgt
	def play_stationary(self, filename, looping, persistent=False):
		return self.play_stationary_extended(filename, looping, 0.0, 1.0,  persistent)
	
	#play_stationary_extended function, Same as bgt. It doesn't support offset and start_pitch yet. Minimum volume is 0.0, maximum volume is 1.0, minimum pan is -1 and maximum pan is 1.
	def play_stationary_extended(self, filename, looping, start_pan, start_volume, persistent=False):
		slot=self.reserve_slot()
		if slot == -1:
			return -1
		self.items[slot].filename=filename
		self.items[slot].looping=looping
		self.items[slot].stationary=True
		self.items[slot].start_pan=start_pan
		self.items[slot].start_volume=start_volume
		
		self.items[slot].persistent=persistent
		try:
			self.items[slot].sound.load(filename)
		except:
			return -1
		if start_pan != 0.0:
			self.items[slot].sound.handle.pan=start_pan
		if start_volume < 1.0:
			self.items[slot].sound.handle.volume=start_volume
		if looping:
			self.items[slot].sound.play_looped()
		else:
			self.items[slot].sound.play()
		if slot > self.highest_slot:
			self.highest_slot = slot
		return slot
	
	#play_1d function, Same as bgt
	def play_1d(self, filename, listener_x, sound_x, looping, persistent=False):
		return self.play_extended_1d(filename, listener_x, sound_x, 0.0, 0.0, looping, 0.0, 1.0, persistent)
	
	#play_extended_1d function. Same as bgt, But as mentioned before, no offset and start pitch. Minimum pan is -1, maximum pan is 1, minimum volume is 0, maximum volume is 1
	def play_extended_1d(self, filename, listener_x, sound_x, left_range, right_range, looping, start_pan, start_volume, persistent=False):
		slot=self.reserve_slot()
		if slot == -1:
			return -1
		self.items[slot].filename=filename
		self.items[slot].x=sound_x
		self.items[slot].y=0
		self.items[slot].looping=looping
		self.items[slot].pan_step=self.pan_step
		self.items[slot].volume_step=self.volume_step
		self.items[slot].behind_pitch_decrease=0.0
		self.items[slot].start_pan=start_pan
		self.items[slot].start_volume=start_volume
		self.items[slot].left_range=left_range
		self.items[slot].right_range=right_range
		self.items[slot].is_3d=False
		self.items[slot].persistent=persistent
		if self.max_distance > 0 and self.items[slot].get_total_distance(listener_x, 0, 0) > self.max_distance:
			if looping == False:
				self.items[slot].sound.stop()
				return -2
			else:
				self.last_listener_x=listener_x
				self.items[slot].update(listener_x, 0, 0, 0.0, self.max_distance)
				if slot > self.highest_slot:
					self.highest_slot=slot
				return slot
		try:
			self.items[slot].sound.load(filename)
		except:
			print("could not load %s" %(filename))
			return -1
		self.last_listener_x=listener_x
		self.items[slot].update(listener_x, 0, 0, 0.0, self.max_distance)
		if looping:
			self.items[slot].sound.play_looped()
		else:
			self.items[slot].sound.play()
		if slot > self.highest_slot:
			self.highest_slot = slot
		return slot
	
	def play_2d(self, filename, listener_x, listener_y, sound_x, sound_y, rotation, looping, persistent=False):
		return self.play_extended_2d(filename, listener_x, listener_y, sound_x, sound_y, rotation, 0, 0, 0, 0, looping, 0.0, 1.0, persistent)
	
	def play_2d(self, filename, listener_x, listener_y, sound_x, sound_y, looping, persistent=False):
		return self.play_extended_2d(filename, listener_x, listener_y, sound_x, sound_y, 0.0, 0, 0, 0, 0, looping, 0.0, 1.0, persistent)
	
	def play_extended_2d(self, filename, listener_x, listener_y, sound_x, sound_y, rotation, left_range, right_range, backward_range, forward_range, looping, start_pan, start_volume, persistent=False):
		slot=self.reserve_slot()
		if slot == -1:
			return -1
		self.items[slot].filename=filename
		self.items[slot].x=sound_x
		self.items[slot].y=sound_y
		self.items[slot].looping=looping
		self.items[slot].pan_step=self.pan_step
		self.items[slot].volume_step=self.volume_step
		self.items[slot].behind_pitch_decrease=self.behind_pitch_decrease
		self.items[slot].start_pan=start_pan
		self.items[slot].start_volume=start_volume
		self.items[slot].left_range=left_range
		self.items[slot].right_range=right_range
		self.items[slot].backward_range=backward_range
		self.items[slot].forward_range=forward_range
		self.items[slot].is_3d=True
		self.items[slot].persistent=persistent
		if self.max_distance>0 and self.items[slot].get_total_distance(listener_x, listener_y, 0) > self.max_distance:
			if looping == False:
				return -2
			else:
				self.last_listener_x=listener_x
				self.last_listener_y=listener_y
				self.last_listener_rotation=rotation
				self.items[slot].update(listener_x, listener_y, 0, rotation, self.max_distance)
				if slot > self.highest_slot:
					self.highest_slot = slot
				return slot
		try:
			self.items[slot].sound.load(filename)
		except:
			return -1
		self.last_listener_x=listener_x
		self.last_listener_y=listener_y
		self.last_listener_rotation=rotation
		self.items[slot].update(listener_x, listener_y, 0, rotation, self.max_distance)
		if looping:
			self.items[slot].sound.play_looped()
		else:
			self.items[slot].sound.play()
		if slot > self.highest_slot:
			self.highest_slot = slot
		return slot
	
	def play_3d(self, filename, listener_x, listener_y, listener_z, sound_x, sound_y, sound_z, looping, persistent=False):
		return self.play_extended_3d(filename, listener_x, listener_y, listener_z, sound_x, sound_y, sound_z, 0.0, 0, 0, 0, 0, 0, 0, looping, 0.0, 1.0, persistent)
	def play_3d(self, filename, listener_x, listener_y, listener_z, sound_x, sound_y, sound_z, rotation, looping, persistent=False):
		return self.play_extended_3d(filename, listener_x, listener_y, listener_z, sound_x, sound_y, sound_z, rotation, 0, 0, 0, 0, 0, 0, looping, 0.0, 1.0, persistent)
	def play_extended_3d(self, filename, listener_x, listener_y, listener_z, sound_x, sound_y, sound_z, rotation, left_range, right_range, backward_range, forward_range, lower_range, upper_range, looping, start_pan, start_volume, persistent=False):
		slot=self.reserve_slot()
		if slot == -1:
			return -1
		self.items[slot].filename=filename
		self.items[slot].x=sound_x
		self.items[slot].y=sound_y
		self.items[slot].z=sound_z
		self.items[slot].looping=looping
		self.items[slot].pan_step=self.pan_step
		self.items[slot].volume_step=self.volume_step
		self.items[slot].behind_pitch_decrease=self.behind_pitch_decrease
		self.items[slot].start_pan=start_pan
		self.items[slot].start_volume=start_volume
		self.items[slot].left_range=left_range
		self.items[slot].right_range=right_range
		self.items[slot].backward_range=backward_range
		self.items[slot].forward_range=forward_range
		self.items[slot].lower_range=lower_range
		self.items[slot].upper_range=upper_range
		self.items[slot].is_3d=True
		self.items[slot].persistent=persistent
		if self.max_distance>0 and self.items[slot].get_total_distance(listener_x, listener_y, listener_z) > self.max_distance:
			if looping == False:
				return -2
			else:
				self.last_listener_x=listener_x
				self.last_listener_y=listener_y
				self.last_listener_z=listener_z
				self.last_listener_rotation=rotation
				self.items[slot].update(listener_x, listener_y, listener_z, rotation, self.max_distance)
				if slot > self.highest_slot:
					self.highest_slot = slot
				return slot
		try:
			self.items[slot].sound.load(filename)
		except:
			return -1
		self.last_listener_x=listener_x
		self.last_listener_y=listener_y
		self.last_listener_z=listener_z
		self.last_listener_rotation=rotation
		self.items[slot].update(listener_x, listener_y, listener_z, rotation, self.max_distance)
		if looping:
			self.items[slot].sound.play_looped()
		else:
			self.items[slot].sound.play()
		if slot > self.highest_slot:
			self.highest_slot = slot
		return slot
	
	def update_sound_1d(self, slot, x):
		return self.update_sound_3d(slot, x, 0, 0)
	
	def update_sound_2d(self, slot, x, y):
		return self.update_sound_3d(slot, x, y, 0)
	
	def update_sound_3d(self, slot, x, y, z):
		if(self.verify_slot) == False:
			return False
		self.items[slot].x=x
		self.items[slot].y=y
		self.items[slot].z=z
		self.items[slot].update(self.last_listener_x, self.last_listener_y, self.last_listener_z, self.last_listener_rotation, self.max_distance)
		return True
	
	def sound_is_playing(self, slot):
		if self.items[slot].sound.handle == 0:
			return False
		return self.items[slot].sound.handle.is_playing()
	
	
	def verify_slot(self, slot):
		if slot < 0:
			return False
		if slot >= len(self.items):
			return False
		if self.items[slot].persistent==true:
			return True
		if self.items[slot].sound.handle==0:
			return False
		if self.items[slot].sound.handle.is_looping():
			return True
		return False
	def update_listener_1d(self, listener_x):
		self.update_listener_3d(listener_x, 0, 0, 0.0)
	
	def update_listener_2d(self, listener_x, listener_y, rotation):
		self.update_listener_3d(listener_x, listener_y, 0, rotation)
	def update_listener_3d(self, listener_x, listener_y, listener_z, rotation):
		if len(self.items) == 0:
			return
		self.last_listener_x=listener_x
		self.last_listener_y=listener_y
		self.last_listener_z=listener_z
		self.last_listener_rotation=rotation
		for i in range(self.highest_slot+1):
			self.items[i].update(listener_x, listener_y, listener_z, rotation, self.max_distance)
	
	
	def reserve_slot(self):
		self.clean_frequency-=1
		if self.clean_frequency == 0:
			self.clean_frequency=3
			#self.clean_unused()
		slot=-1
		for i in range(len(self.items)):
			if self.items[i].persistent==True or self.items[i].looping==True:
				continue
			if self.items[slot].sound.handle==0:
				slot = i
				break
			if self.items[i].sound.handle.is_playing()==False or self.items[slot].sound.handle.is_active()==False:
				slot = i
				break
		return slot
	
	