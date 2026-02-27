# Browser-Use Library Architecture

## Overview
The `browser-use` library implements an event-driven architecture for AI-powered browser automation. The system is composed of several interconnected modules that handle different aspects of browser interaction and automation.

## Core Components

### 1. Actor Module (`browser_use/actor/`)
The actor module provides low-level primitives for browser interactions, simulating human-like behavior through realistic mouse movements, element interactions, and page navigation.

#### Key Functions:
- **Realistic Mouse Movement**: Implements human-like mouse paths using Bezier curves and easing functions to avoid robot detection
- **Element Interactions**: Direct DOM manipulation and interaction with page elements
- **Page Operations**: Low-level page navigation and manipulation capabilities

#### Key Files:
- `mouse.py`: Implements realistic mouse movement algorithms with curved paths, easing functions, and random deviations
- `element.py`: Handles element-specific operations including clicks, input, focus, and dragging
- `page.py`: Manages page-level interactions and operations
- `utils.py`: Utility functions for actor operations

### 2. Browser Module (`browser_use/browser/`)
The browser module manages the actual browser sessions, CDP (Chrome DevTools Protocol) connections, and coordinates various watchdog services through an event bus.

#### Key Functions:
- **Session Management**: Creates and manages browser sessions using Chrome DevTools Protocol
- **CDP Communication**: Handles communication with the browser via CDP commands
- **Event Coordination**: Coordinates multiple watchdog services through an event bus system
- **Security Monitoring**: Implements domain restrictions and security policies

#### Key Files:
- `session.py`: Core session management and CDP client handling
- `profile.py`: Browser configuration profiles and launch settings
- `watchdogs/`: Multiple watchdog services for different browser events:
  - `captcha_watchdog.py`: Handles CAPTCHA detection and solving
  - `downloads_watchdog.py`: Manages file downloads
  - `popups_watchdog.py`: Handles JavaScript dialogs and popups
  - `security_watchdog.py`: Enforces domain restrictions
  - `dom_watchdog.py`: Processes DOM snapshots and element highlighting

### 3. Tools Module (`browser_use/tools/`)
The tools module serves as the bridge between AI decisions and actual browser operations, mapping LLM outputs to concrete browser actions.

#### Key Functions:
- **Action Registration**: Maps AI decisions to browser operations
- **Action Execution**: Translates LLM-generated actions into browser commands
- **Input/Output Processing**: Validates and processes tool parameters

#### Key Files:
- `service.py`: Core tools registry and action mapping
- `views.py`: Pydantic models defining action schemas
- `registry/`: Action registration and validation logic

### 4. DOM Module (`browser_use/dom/`)
The DOM module handles DOM processing, element serialization, and extraction of page content for AI consumption.

#### Key Functions:
- **DOM Serialization**: Converts DOM structures to formats suitable for AI processing
- **Element Selection**: Identifies and extracts interactive elements
- **Content Extraction**: Processes and extracts relevant page content
- **Accessibility Tree Generation**: Creates accessibility trees for element identification

#### Key Files:
- `service.py`: Main DOM processing service
- `serializer/`: Different serializers for DOM content
- `views.py`: Data models for DOM representation

## Component Relationships

### Event Flow
```
[Agent] -> [Tools] -> [Browser Session] -> [CDP Client] -> [Browser]
                      -> [Actor] -> [Mouse/Element Operations]
                      -> [DOM] -> [Element Processing]

Events flow through bubus (event bus):
[BrowserSession] <- [Watchdogs] <- [Security/CAPTCHA/etc]
```

### Interaction Flow
1. **Agent Layer**: Makes high-level decisions based on LLM responses
2. **Tools Layer**: Translates decisions into specific actions (click, input, navigate)
3. **Browser Layer**: Coordinates with CDP and manages browser sessions
4. **Actor Layer**: Executes low-level operations with realistic human-like behavior
5. **DOM Layer**: Provides element information and content extraction
6. **Watchdogs**: Monitor and handle various browser events and conditions

### Data Flow
- DOM information flows from the browser to the AI model through the DOM module
- AI decisions flow through the tools module to trigger specific actions
- Actions are executed via the actor module with realistic behavior
- Browser state is monitored and updated continuously by watchdogs

### Key Dependencies
- **Actor** depends on **Browser** for CDP client access
- **Tools** integrate with both **Browser** and **Actor** to execute actions
- **DOM** provides element information to **Tools** and **Agent**
- **Browser** coordinates with all other components through the event system

## Architecture Benefits

1. **Modularity**: Each component has a clear, separated responsibility
2. **Extensibility**: Easy to add new tools or modify behavior without affecting other components
3. **Reliability**: Event-driven architecture with multiple watchdogs ensures robust operation
4. **Human-like Behavior**: Actor module provides realistic interaction patterns
5. **Security**: Built-in security measures through watchdogs and domain restrictions