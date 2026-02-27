# Browser Automation Python API Documentation

## Overview
The `browser-use` library is an async Python >= 3.11 library that implements AI browser driver abilities using LLMs + CDP (Chrome DevTools Protocol). The core architecture enables AI agents to autonomously navigate web pages, interact with elements, and complete complex tasks by processing HTML and making LLM-driven decisions.

## Core Classes

### Agent Class
The primary orchestrator that takes tasks, manages browser sessions, and executes LLM-driven action loops.

#### Constructor Parameters:
- `task: str` - The main task for the agent to perform
- `llm: BaseChatModel | None` - The language model to use (defaults to ChatBrowserUse if not provided)
- `browser_profile: BrowserProfile | None` - Configuration for the browser instance
- `browser_session: BrowserSession | None` - Pre-existing browser session to reuse
- `browser: Browser | None` - Alias for browser_session
- `tools: Tools[Context] | None` - Custom tools to extend agent functionality
- `controller: Tools[Context] | None` - Alias for tools
- `output_model_schema: type[AgentStructuredOutput] | None` - Schema for structured output
- `extraction_schema: dict | None` - Schema for data extraction
- `use_vision: bool | Literal['auto'] = True` - Whether to use vision capabilities
- `max_failures: int = 5` - Maximum number of failures before stopping
- `override_system_message: str | None` - Override the default system message
- `extend_system_message: str | None` - Extend the default system message
- `generate_gif: bool | str = False` - Generate a GIF of the agent's actions
- `max_actions_per_step: int = 5` - Maximum number of actions per step
- `use_thinking: bool = True` - Enable/disable thinking process
- `flash_mode: bool = False` - Use faster mode for certain models
- `max_history_items: int | None` - Limit history items
- `fallback_llm: BaseChatModel | None` - Fallback LLM for error recovery
- `use_judge: bool = True` - Enable judge functionality
- `max_clickable_elements_length: int = 40000` - Maximum length for clickable elements in DOM
- `enable_planning: bool = True` - Enable planning capabilities

#### Main Methods:
- `async def run(self, max_steps: int = 500, on_step_start: AgentHookFunc | None = None, on_step_end: AgentHookFunc | None = None) -> AgentHistoryList[AgentStructuredOutput]` - Execute the task asynchronously
- `def run_sync(self, max_steps: int = 500, on_step_start: AgentHookFunc | None = None, on_step_end: AgentHookFunc | None = None) -> AgentHistoryList[AgentStructuredOutput]` - Synchronous wrapper for the async run method
- `def detect_variables(self) -> dict[str, DetectedVariable]` - Detect reusable variables in agent history
- `def save_history(self, file_path: str | Path | None = None) -> None` - Save agent history to a file
- `def pause(self) -> None` - Pause the agent
- `def resume(self) -> None` - Resume the agent
- `def stop(self) -> None` - Stop the agent
- `async def close(self) -> None` - Close the agent and cleanup resources

### BrowserSession Class
Manages browser lifecycle, CDP connections, and coordinates multiple watchdog services through an event bus.

#### Constructor Parameters:
**Cloud browser parameters:**
- `cloud_profile_id: UUID | str | None` - Cloud profile ID
- `cloud_proxy_country_code: ProxyCountryCode | None` - Proxy country for cloud browsers
- `cloud_timeout: int | None` - Timeout for cloud operations
- `use_cloud: bool | None` - Use cloud browser service
- `cloud_browser_params: CloudBrowserParams | None` - Cloud browser configuration

**Local browser parameters:**
- `executable_path: str | Path | None` - Path to browser executable
- `headless: bool | None` - Run in headless mode
- `user_data_dir: str | Path | None` - Browser user data directory
- `args: list[str] | None` - Additional browser launch arguments
- `downloads_path: str | Path | None` - Downloads directory
- `channel: str | None` - Browser channel (stable, beta, dev, canary)

**Common browser parameters:**
- `headers: dict[str, str] | None` - Default HTTP headers
- `allowed_domains: list[str] | None` - Allowed domains for security
- `prohibited_domains: list[str] | None` - Prohibited domains
- `keep_alive: bool | None` - Keep browser alive between tasks
- `proxy: ProxySettings | None` - Proxy configuration
- `captcha_solver: bool | None` - Enable captcha solving
- `auto_download_pdfs: bool | None` - Auto-download PDF files
- `highlight_elements: bool | None` - Highlight clicked elements
- `dom_highlight_elements: bool | None` - Highlight DOM elements
- `max_iframes: int | None` - Maximum iframes to process
- `max_iframe_depth: int | None` - Maximum iframe nesting depth
- `minimum_wait_page_load_time: float | None` - Minimum time to wait for page load
- `wait_for_network_idle_page_load_time: float | None` - Time to wait for network idle
- `wait_between_actions: float | None` - Wait time between actions

#### Main Methods:
- `async def start(self) -> None` - Start the browser session
- `async def stop(self) -> None` - Stop the browser session
- `async def kill(self) -> None` - Kill the browser session forcefully
- `async def reset(self) -> None` - Reset the browser session
- `async def connect(self, cdp_url: str | None = None) -> Self` - Connect to an existing browser via CDP
- `async def new_page(self, url: str | None = None) -> Page` - Create a new browser page
- `async def get_current_page(self) -> Page | None` - Get the current page
- `async def get_pages(self) -> list[Page]` - Get all open pages
- `async def close_page(self, page: Union[Page, str]) -> None` - Close a specific page
- `async def cookies(self) -> list[Cookie]` - Get all cookies
- `async def clear_cookies(self) -> None` - Clear all cookies
- `async def export_storage_state(self, output_path: str | Path | None = None) -> dict[str, Any]` - Export storage state
- `async def navigate_to(self, url: str, new_tab: bool = False) -> None` - Navigate to URL
- `async def get_current_page_url(self) -> str` - Get current page URL
- `async def get_current_page_title(self) -> str` - Get current page title
- `async def get_browser_state_summary(self) -> BrowserStateSummary` - Get browser state summary
- `async def get_state_as_text(self) -> str` - Get browser state as text
- `async def take_screenshot(self, path: str | Path | None = None, full_page: bool = False) -> bytes` - Take a screenshot
- `async def screenshot_element(self, element_selector: str) -> bytes` - Take screenshot of an element
- `async def get_selector_map(self) -> dict[int, EnhancedDOMTreeNode]` - Get the DOM selector map
- `async def get_element_by_index(self, index: int) -> EnhancedDOMTreeNode | None` - Get element by index
- `async def get_element_coordinates(self, backend_node_id: int, cdp_session: CDPSession) -> DOMRect | None` - Get element coordinates
- `async def get_tabs(self) -> list[TabInfo]` - Get list of open tabs
- `async def remove_highlights(self) -> None` - Remove element highlights
- `async def reconnect(self) -> None` - Reconnect to the browser
- `@classmethod def from_system_chrome(cls, profile_directory: str | None = None, **kwargs: Any) -> Self` - Create session using system Chrome

### Tools Class
Action registry that maps LLM decisions to browser operations (click, type, scroll, etc.).

#### Constructor Parameters:
- `exclude_actions: list[str] | None` - List of action names to exclude
- `output_model: type[T] | None` - Output model for structured output
- `display_files_in_done_text: bool = True` - Display files in done action text

#### Methods:
- `def register(self, description: str, param_model: type[BaseModel], terminates_sequence: bool = False)` - Decorator to register custom actions
- `def get_output_model(self) -> type[BaseModel] | None` - Get the output model
- `def use_structured_output_action(self, schema: type[BaseModel])` - Register structured output action
- `def set_coordinate_clicking(self, enabled: bool)` - Enable coordinate-based clicking
- `def exclude_action(self, action_name: str)` - Exclude an action from being registered

## Available Built-in Actions

### Navigation Actions
- **search** - Search engines (DuckDuckGo, Google, Bing)
  - Parameters: `query: str`, `engine: str` (default: 'duckduckgo')
- **navigate** - Go to specific URLs
  - Parameters: `url: str`, `new_tab: bool` (default: False)
- **go_back** - Navigate back in browser history
  - Parameters: none
- **wait** - Pause execution for specified time
  - Parameters: `seconds: int` (default: 5)

### Element Interaction
- **click** - Click by element index or coordinates
  - Parameters: `index: int | None`, `coordinate_x: int | None`, `coordinate_y: int | None`
- **input** - Input text into elements
  - Parameters: `index: int`, `text: str`, `clear: bool` (default: True)
- **scroll** - Scroll up/down the page
  - Parameters: `down: bool` (default: True), `pages: float` (default: 1.0), `index: int | None`
- **upload_file** - Upload files to input elements
  - Parameters: `index: int`, `path: str`
- **send_keys** - Send keyboard shortcuts
  - Parameters: `keys: str` (e.g., 'Enter', 'Control+o')

### Tab Management
- **switch** - Switch between browser tabs
  - Parameters: `tab_id: str` (4-character ID)
- **close** - Close browser tabs
  - Parameters: `tab_id: str` (4-character ID)

### Data Extraction
- **extract** - Extract structured data from pages
  - Parameters: `query: str`, `extract_links: bool` (default: False), `start_from_char: int` (default: 0), `output_schema: dict | None`
- **find_elements** - Find elements matching CSS selectors
  - Parameters: `selector: str`, `attributes: list[str] | None`, `max_results: int` (default: 50), `include_text: bool` (default: True)
- **search_page** - Search for text patterns on page
  - Parameters: `pattern: str`, `regex: bool` (default: False), `case_sensitive: bool` (default: False), `context_chars: int` (default: 150), `css_scope: str | None`, `max_results: int` (default: 25)
- **read_content** - Read long-form content intelligently
  - Parameters: `goal: str`, `source: str` (default: 'page'), `context: str` (default: '')

### Utilities
- **screenshot** - Take screenshots of page or elements
  - Parameters: `file_name: str | None` (default: None)
- **save_as_pdf** - Save page as PDF
  - Parameters: `file_name: str | None`, `print_background: bool` (default: True), `landscape: bool` (default: False), `scale: float` (default: 1.0), `paper_format: str` (default: 'Letter')
- **done** - Complete the task and return result
  - Parameters: `text: str`, `success: bool` (default: True), `files_to_display: list[str] | None` (default: [])
- **structured_output** - Return structured data according to schema
  - Parameters: `data: T` (matches provided schema), `success: bool` (default: True), `files_to_display: list[str] | None` (default: [])

## Chat Models

### Base Classes
- `BaseChatModel` - Abstract base class for all chat models

### Available Chat Models
- `ChatOpenAI` - OpenAI GPT models
- `ChatGoogle` - Google Gemini models
- `ChatAnthropic` - Anthropic Claude models
- `ChatAzureOpenAI` - Azure OpenAI models
- `ChatBrowserUse` - Browser-use specific fine-tuned models
- `ChatGroq` - Groq models
- `ChatMistral` - Mistral models
- `ChatOllama` - Ollama local models
- `ChatDeepSeek` - DeepSeek models
- `ChatOCIRaw` - Oracle Cloud Infrastructure models
- `ChatOpenRouter` - OpenRouter models
- `ChatVercel` - Vercel models
- `ChatCerebras` - Cerebras models
- `ChatAWSBedrock` - AWS Bedrock models
- `ChatAnthropicBedrock` - Anthropic models on AWS Bedrock

## Usage Patterns

### Basic Usage
```python
from browser_use import Agent, ChatBrowserUse

# Initialize the model
llm = ChatBrowserUse(model='bu-2-0')

# Define a task
task = "Search Google for 'what is browser automation' and tell me the top 3 results"

# Create and run the agent
agent = Agent(task=task, llm=llm)
await agent.run()
```

### With Custom Browser Configuration
```python
from browser_use import Agent, ChatBrowserUse, BrowserSession

# Create a browser session with custom configuration
browser = BrowserSession(headless=False, user_data_dir='./profile')

# Create agent with custom browser
llm = ChatBrowserUse(model='bu-2-0')
agent = Agent(task="Perform web automation task", llm=llm, browser=browser)
await agent.run()
```

### With Structured Output
```python
from pydantic import BaseModel
from browser_use import Agent, ChatBrowserUse

# Define your output schema
class SearchResult(BaseModel):
    title: str
    url: str
    description: str

class SearchResults(BaseModel):
    results: list[SearchResult]

# Create agent with structured output schema
llm = ChatOpenAI(model='gpt-4o')
agent = Agent(
    task="Search for Python tutorials and return top 3 results",
    llm=llm,
    output_model_schema=SearchResults
)
result = await agent.run()
# Result will be of type SearchResults
```

### Synchronous Usage
```python
from browser_use import Agent, ChatBrowserUse

llm = ChatBrowserUse(model='bu-2-0')
agent = Agent(task="Search for weather forecast", llm=llm)
history = agent.run_sync(max_steps=100)  # Synchronous execution
```

### With Custom Tools
```python
from browser_use import Agent, ChatBrowserUse, Tools

# Create custom tools
tools = Tools()

@tools.register(
    'Custom function that does something',
    param_model=MyCustomAction
)
async def my_custom_action(params: MyCustomAction, browser_session):
    # Your custom logic here
    return ActionResult(extracted_content="result", success=True)

# Create agent with custom tools
llm = ChatBrowserUse(model='bu-2-0')
agent = Agent(task="Use my custom tool", llm=llm, tools=tools)
await agent.run()
```

## Advanced Features

### Vision Capabilities
Enable vision to allow the LLM to see screenshots of the browser:
```python
agent = Agent(
    task="Describe the content of this webpage",
    llm=llm,
    use_vision=True  # Enabled by default
)
```

### Planning
Enable automatic planning to help the agent break complex tasks into steps:
```python
agent = Agent(
    task="Complex multi-step task...",
    llm=llm,
    enable_planning=True  # Enabled by default
)
```

### Security Controls
Configure domain restrictions for security:
```python
from browser_use import BrowserSession

browser = BrowserSession(
    allowed_domains=['example.com', 'trusted-site.com'],
    prohibited_domains=['malicious-site.com']
)
```

### Cloud Browsers
Use remote browsers instead of local ones:
```python
from browser_use import Agent, ChatBrowserUse, BrowserSession

# Create cloud browser session
browser = BrowserSession(
    cloud_profile_id="your-profile-id",  # Your cloud profile ID
    cloud_proxy_country_code="US"        # Optional proxy location
)

agent = Agent(
    task="Automate using cloud browser",
    llm=ChatBrowserUse(model='bu-2-0'),
    browser=browser
)
await agent.run()
```

### Error Handling and Retry Logic
The agent has built-in error handling and can use fallback LLMs:
```python
agent = Agent(
    task="Perform robust automation",
    llm=primary_llm,
    fallback_llm=secondary_llm,  # Will be used if primary fails
    max_failures=10,             # Increase max failures
    calculate_cost=True          # Track token usage costs
)
```

## Events and Observability

The library uses an event-driven architecture with various events:
- `BrowserStartEvent` - Browser startup
- `NavigateToUrlEvent` - Navigation events
- `SwitchTabEvent` - Tab switching
- `CloseTabEvent` - Tab closing
- `ClickElementEvent` - Element clicks
- `FileDownloadedEvent` - File downloads
- And many more for different browser operations

These events can be subscribed to for advanced monitoring and control of the browser automation process.