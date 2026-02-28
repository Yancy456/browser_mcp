"""Cloud sync event types (moved from agent - Agent has been removed)."""

from datetime import datetime, timezone

from bubus import BaseEvent
from pydantic import Field, field_validator
from uuid_extensions import uuid7str

MAX_STRING_LENGTH = 500000
MAX_URL_LENGTH = 100000
MAX_TASK_LENGTH = 100000
MAX_COMMENT_LENGTH = 2000
MAX_FILE_CONTENT_SIZE = 50 * 1024 * 1024  # 50MB


class UpdateAgentTaskEvent(BaseEvent):
	id: str
	user_id: str = Field(max_length=255)
	device_id: str | None = Field(None, max_length=255)
	stopped: bool | None = None
	paused: bool | None = None
	done_output: str | None = Field(None, max_length=MAX_STRING_LENGTH)
	finished_at: datetime | None = None
	agent_state: dict | None = None
	user_feedback_type: str | None = Field(None, max_length=10)
	user_comment: str | None = Field(None, max_length=MAX_COMMENT_LENGTH)
	gif_url: str | None = Field(None, max_length=MAX_URL_LENGTH)


class CreateAgentOutputFileEvent(BaseEvent):
	id: str = Field(default_factory=uuid7str)
	user_id: str = Field(max_length=255)
	device_id: str | None = Field(None, max_length=255)
	task_id: str
	file_name: str = Field(max_length=255)
	file_content: str | None = None
	content_type: str | None = Field(None, max_length=100)
	created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

	@field_validator('file_content')
	@classmethod
	def validate_file_size(cls, v: str | None) -> str | None:
		if v is None:
			return v
		if ',' in v:
			v = v.split(',')[1]
		estimated_size = len(v) * 3 / 4
		if estimated_size > MAX_FILE_CONTENT_SIZE:
			raise ValueError(f'File content exceeds maximum size of {MAX_FILE_CONTENT_SIZE / 1024 / 1024}MB')
		return v


class CreateAgentStepEvent(BaseEvent):
	id: str = Field(default_factory=uuid7str)
	user_id: str = Field(max_length=255)
	device_id: str | None = Field(None, max_length=255)
	created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
	agent_task_id: str
	step: int
	evaluation_previous_goal: str = Field(max_length=MAX_STRING_LENGTH)
	memory: str = Field(max_length=MAX_STRING_LENGTH)
	next_goal: str = Field(max_length=MAX_STRING_LENGTH)
	actions: list[dict]
	screenshot_url: str | None = Field(None, max_length=MAX_FILE_CONTENT_SIZE)
	url: str = Field(default='', max_length=MAX_URL_LENGTH)

	@field_validator('screenshot_url')
	@classmethod
	def validate_screenshot_size(cls, v: str | None) -> str | None:
		if v is None or not v.startswith('data:'):
			return v
		if ',' in v:
			base64_part = v.split(',')[1]
			estimated_size = len(base64_part) * 3 / 4
			if estimated_size > MAX_FILE_CONTENT_SIZE:
				raise ValueError(f'Screenshot content exceeds maximum size of {MAX_FILE_CONTENT_SIZE / 1024 / 1024}MB')
		return v


class CreateAgentTaskEvent(BaseEvent):
	id: str = Field(default_factory=uuid7str)
	user_id: str = Field(max_length=255)
	device_id: str | None = Field(None, max_length=255)
	agent_session_id: str
	llm_model: str = Field(max_length=200)
	stopped: bool = False
	paused: bool = False
	task: str = Field(max_length=MAX_TASK_LENGTH)
	done_output: str | None = Field(None, max_length=MAX_STRING_LENGTH)
	scheduled_task_id: str | None = None
	started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
	finished_at: datetime | None = None
	agent_state: dict = Field(default_factory=dict)
	user_feedback_type: str | None = Field(None, max_length=10)
	user_comment: str | None = Field(None, max_length=MAX_COMMENT_LENGTH)
	gif_url: str | None = Field(None, max_length=MAX_URL_LENGTH)


class CreateAgentSessionEvent(BaseEvent):
	id: str = Field(default_factory=uuid7str)
	user_id: str = Field(max_length=255)
	device_id: str | None = Field(None, max_length=255)
	browser_session_id: str = Field(max_length=255)
	browser_session_live_url: str = Field(max_length=MAX_URL_LENGTH)
	browser_session_cdp_url: str = Field(max_length=MAX_URL_LENGTH)
	browser_session_stopped: bool = False
	browser_session_stopped_at: datetime | None = None
	is_source_api: bool | None = None
	browser_state: dict = Field(default_factory=dict)
	browser_session_data: dict | None = None


class UpdateAgentSessionEvent(BaseEvent):
	id: str
	user_id: str = Field(max_length=255)
	device_id: str | None = Field(None, max_length=255)
	browser_session_stopped: bool | None = None
	browser_session_stopped_at: datetime | None = None
	end_reason: str | None = Field(None, max_length=100)
