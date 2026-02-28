"""
Pytest configuration for browser-use CI tests.

Sets up environment variables to ensure tests never connect to production services.
"""

import os
import socketserver
import tempfile
from unittest.mock import AsyncMock

import pytest
from dotenv import load_dotenv
from pytest_httpserver import HTTPServer

# Fix for httpserver hanging on shutdown - prevent blocking on socket close
# This prevents tests from hanging when shutting down HTTP servers
socketserver.ThreadingMixIn.block_on_close = False
# Also set daemon threads to prevent hanging
socketserver.ThreadingMixIn.daemon_threads = True

from browser_use.tools.service import Tools

# Load environment variables before any imports
load_dotenv()


# Skip LLM API key verification for tests
os.environ['SKIP_LLM_API_KEY_VERIFICATION'] = 'true'

from bubus import BaseEvent

from browser_use.browser import BrowserProfile, BrowserSession


@pytest.fixture(autouse=True)
def setup_test_environment():
	"""
	Automatically set up test environment for all tests.
	"""

	# Create a temporary directory for test config (but not for extensions)
	config_dir = tempfile.mkdtemp(prefix='browseruse_tests_')

	original_env = {}
	test_env_vars = {
		'SKIP_LLM_API_KEY_VERIFICATION': 'true',
		'ANONYMIZED_TELEMETRY': 'false',
		'BROWSER_USE_CLOUD_SYNC': 'true',
		'BROWSER_USE_CLOUD_API_URL': 'http://placeholder-will-be-replaced-by-specific-test-fixtures',
		'BROWSER_USE_CLOUD_UI_URL': 'http://placeholder-will-be-replaced-by-specific-test-fixtures',
		# Don't set BROWSER_USE_CONFIG_DIR anymore - let it use the default ~/.config/browseruse
		# This way extensions will be cached in ~/.config/browseruse/extensions
	}

	for key, value in test_env_vars.items():
		original_env[key] = os.environ.get(key)
		os.environ[key] = value

	yield

	# Restore original environment
	for key, value in original_env.items():
		if value is None:
			os.environ.pop(key, None)
		else:
			os.environ[key] = value


# not a fixture, mock_llm() provides this in a fixture below, this is a helper so that it can accept args
def create_mock_llm(actions: list[str] | None = None):
	"""Create a mock LLM. Agent/LLM have been removed - skips (tests using this need Agent)."""
	pytest.skip('Agent and LLM have been removed from browser-use')


@pytest.fixture(scope='module')
async def browser_session():
	"""Create a real browser session for testing"""
	session = BrowserSession(
		browser_profile=BrowserProfile(
			headless=True,
			user_data_dir=None,  # Use temporary directory
			keep_alive=True,
			enable_default_extensions=True,  # Enable extensions during tests
		)
	)
	await session.start()
	yield session
	await session.kill()
	# Ensure event bus is properly stopped
	await session.event_bus.stop(clear=True, timeout=5)


@pytest.fixture(scope='function')
def mock_llm():
	"""Create a mock LLM that just returns the done action if queried"""
	return create_mock_llm(actions=None)


@pytest.fixture(scope='function')
def agent_with_cloud(browser_session, mock_llm):
	"""Create agent. Agent has been removed - skips."""
	pytest.skip('Agent has been removed')


@pytest.fixture(scope='function')
def event_collector():
	"""Helper to collect all events emitted during tests"""
	events = []
	event_order = []

	class EventCollector:
		def __init__(self):
			self.events = events
			self.event_order = event_order

		async def collect_event(self, event: BaseEvent):
			self.events.append(event)
			self.event_order.append(event.event_type)
			return 'collected'

		def get_events_by_type(self, event_type: str) -> list[BaseEvent]:
			return [e for e in self.events if e.event_type == event_type]

		def clear(self):
			self.events.clear()
			self.event_order.clear()

	return EventCollector()
