"""Mouse class for mouse operations with realistic human-like movement."""

import math
import random
import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from cdp_use.cdp.input.commands import DispatchMouseEventParameters, SynthesizeScrollGestureParameters
	from cdp_use.cdp.input.types import MouseButton

	from browser_use.browser.session import BrowserSession


def _ease_in_out_quad(t: float) -> float:
	"""Easing function for smooth movement."""
	if t < 0.5:
		return 2 * t * t
	return -1 + (4 - 2 * t) * t


def _human_mouse_move(start_x: int, start_y: int, end_x: int, end_y: int):
	"""Generate realistic human-like mouse movement path."""
	# Total distance
	total_dist = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)

	if total_dist < 10:  # Short distances - simpler path
		return [(end_x, end_y)]

	# Number of steps based on distance
	n_steps = max(5, int(total_dist / 20) + random.randint(0, 5))

	# Generate a curved path using easing function concept
	points = []
	points.append((start_x, start_y))

	for i in range(1, n_steps):
		t = i / n_steps
		ease_t = _ease_in_out_quad(t)

		# Target position with some deviation
		target_x = start_x + (end_x - start_x) * ease_t
		target_y = start_y + (end_y - start_y) * ease_t

		# Add realistic deviation based on distance traveled
		max_deviation = min(total_dist * 0.2, 50)
		deviation = max_deviation * random.uniform(-0.3, 0.3)

		# Perpendicular deviation to create a curved path
		angle = math.atan2(end_y - start_y, end_x - start_x) + math.pi/2
		dev_x = deviation * math.cos(angle)
		dev_y = deviation * math.sin(angle)

		# Apply the deviation and add small random noise
		x = int(target_x + dev_x + random.uniform(-3, 3))
		y = int(target_y + dev_y + random.uniform(-3, 3))

		points.append((x, y))

	points.append((end_x, end_y))
	return points


class Mouse:
	"""Mouse operations for a target with realistic human-like movement."""

	def __init__(self, browser_session: 'BrowserSession', session_id: str | None = None, target_id: str | None = None):
		self._browser_session = browser_session
		self._client = browser_session.cdp_client
		self._session_id = session_id
		self._target_id = target_id

	async def click(self, x: int, y: int, button: 'MouseButton' = 'left', click_count: int = 1) -> None:
		"""Click at the specified coordinates with realistic human-like movement."""
		# Move mouse to target with realistic movement
		await self.move_to(x, y)

		# Add human-like delay before clicking (time to "look" at what we're clicking)
		await asyncio.sleep(random.uniform(0.08, 0.25))

		# Mouse press with slight randomness in timing
		press_params: 'DispatchMouseEventParameters' = {
			'type': 'mousePressed',
			'x': x,
			'y': y,
			'button': button,
			'clickCount': click_count,
		}
		await self._client.send.Input.dispatchMouseEvent(
			press_params,
			session_id=self._session_id,
		)

		# Human-like pause between press and release - mimics finger pressure variation
		hold_duration = random.uniform(0.06, 0.20)
		await asyncio.sleep(hold_duration)

		# Mouse release
		release_params: 'DispatchMouseEventParameters' = {
			'type': 'mouseReleased',
			'x': x,
			'y': y,
			'button': button,
			'clickCount': click_count,
		}
		await self._client.send.Input.dispatchMouseEvent(
			release_params,
			session_id=self._session_id,
		)

		# Small pause after click to simulate human reaction time
		await asyncio.sleep(random.uniform(0.1, 0.35))

	async def move_to(self, x: int, y: int) -> None:
		"""Move mouse to coordinates with realistic human-like movement."""
		# For simulation purposes, estimate a starting point near the destination
		# In a real implementation with access to current mouse position, we'd use the actual position
		current_x = x - random.randint(20, 300)  # Simulate starting from nearby
		current_y = y - random.randint(20, 300)

		# Generate human-like path
		path_points = _human_mouse_move(current_x, current_y, x, y)

		for idx, (point_x, point_y) in enumerate(path_points):
			# Adjust coordinates to be within valid bounds
			clamped_x = max(0, min(point_x, 9999))  # Assuming reasonable screen bounds
			clamped_y = max(0, min(point_y, 9999))

			params: 'DispatchMouseEventParameters' = {
				'type': 'mouseMoved',
				'x': clamped_x,
				'y': clamped_y
			}
			await self._client.send.Input.dispatchMouseEvent(params, session_id=self._session_id)

			# Variable speed for more human-like movement
			# Humans move faster in the middle of the path, slower at ends
			if idx == 0 or idx == len(path_points) - 1:  # Beginning and end, move slower
				await asyncio.sleep(random.uniform(0.015, 0.035))
			else:
				# Middle of movement, can be faster
				await asyncio.sleep(random.uniform(0.005, 0.025))

	async def down(self, button: 'MouseButton' = 'left', click_count: int = 1) -> None:
		"""Press mouse button down."""
		params: 'DispatchMouseEventParameters' = {
			'type': 'mousePressed',
			'x': 0,  # Will use last mouse position
			'y': 0,
			'button': button,
			'clickCount': click_count,
		}
		await self._client.send.Input.dispatchMouseEvent(
			params,
			session_id=self._session_id,
		)

	async def up(self, button: 'MouseButton' = 'left', click_count: int = 1) -> None:
		"""Release mouse button."""
		params: 'DispatchMouseEventParameters' = {
			'type': 'mouseReleased',
			'x': 0,  # Will use last mouse position
			'y': 0,
			'button': button,
			'clickCount': click_count,
		}
		await self._client.send.Input.dispatchMouseEvent(
			params,
			session_id=self._session_id,
		)

	async def move(self, x: int, y: int) -> None:
		"""Move mouse to the specified coordinates with human-like behavior."""
		await self.move_to(x, y)

	async def scroll(self, x: int = 0, y: int = 0, delta_x: int | None = None, delta_y: int | None = None) -> None:
		"""Scroll the page using robust CDP methods."""
		if not self._session_id:
			raise RuntimeError('Session ID is required for scroll operations')

		# Method 1: Try mouse wheel event (most reliable)
		try:
			# Get viewport dimensions
			layout_metrics = await self._client.send.Page.getLayoutMetrics(session_id=self._session_id)
			viewport_width = layout_metrics['layoutViewport']['clientWidth']
			viewport_height = layout_metrics['layoutViewport']['clientHeight']

			# Use provided coordinates or center of viewport
			scroll_x = x if x > 0 else viewport_width / 2
			scroll_y = y if y > 0 else viewport_height / 2

			# Calculate scroll deltas (positive = down/right)
			scroll_delta_x = delta_x or 0
			scroll_delta_y = delta_y or 0

			# Dispatch mouse wheel event
			await self._client.send.Input.dispatchMouseEvent(
				params={
					'type': 'mouseWheel',
					'x': scroll_x,
					'y': scroll_y,
					'deltaX': scroll_delta_x,
					'deltaY': scroll_delta_y,
				},
				session_id=self._session_id,
			)
			return

		except Exception:
			pass

		# Method 2: Fallback to synthesizeScrollGesture
		try:
			params: 'SynthesizeScrollGestureParameters' = {'x': x, 'y': y, 'xDistance': delta_x or 0, 'yDistance': delta_y or 0}
			await self._client.send.Input.synthesizeScrollGesture(
				params,
				session_id=self._session_id,
			)
		except Exception:
			# Method 3: JavaScript fallback
			scroll_js = f'window.scrollBy({delta_x or 0}, {delta_y or 0})'
			await self._client.send.Runtime.evaluate(
				params={'expression': scroll_js, 'returnByValue': True},
				session_id=self._session_id,
			)