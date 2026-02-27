# Actor vs DOM Modules Comparison

## Actor Module (`browser_use/actor/`)
The Actor module focuses on **performing actions** on the browser. It handles the execution of interactions with web elements and page operations.

### Purpose
- **Action Execution**: Actually performs browser interactions (clicks, typing, navigation)
- **Low-level Control**: Provides granular control over browser operations
- **Human-like Behavior**: Implements realistic movement patterns and interaction delays

### Key Responsibilities
- **Mouse Operations**: Realistic mouse movement with curved paths and human-like timing
- **Element Interactions**: Actually clicking, typing, scrolling, and manipulating elements
- **Page Operations**: Direct manipulation of page content and navigation
- **Behavior Simulation**: Adds randomness and delays to mimic human behavior

### Implementation Details
- Direct CDP (Chrome DevTools Protocol) commands for executing actions
- Timing delays, easing functions, and movement algorithms
- Focus on "doing" - performing the actual interactions

### Example Use Cases
- Clicking a button with realistic mouse movement
- Typing text with human-like key press timing
- Scrolling with variable speed

## DOM Module (`browser_use/dom/`)
The DOM module focuses on **reading and analyzing** the browser's DOM structure. It handles extracting information from the web page for the AI to process.

### Purpose
- **Information Extraction**: Extracts DOM content and structure for AI consumption
- **Element Discovery**: Finds and identifies interactive elements on the page
- **Content Processing**: Converts DOM information into AI-friendly formats

### Key Responsibilities
- **DOM Serialization**: Converts DOM structure to accessible formats
- **Element Detection**: Identifies clickable, input, and other interactive elements
- **Content Analysis**: Extracts text, links, and other page content
- **Structure Representation**: Creates structured representations of the page

### Implementation Details
- Parses and analyzes the DOM structure
- Creates element indexes and mapping systems
- Focus on "observing" - providing information about the page state

### Example Use Cases
- Finding all clickable elements on a page
- Extracting text content for AI analysis
- Creating element indexes for identification

## Key Differences

| Aspect | Actor Module | DOM Module |
|--------|-------------|------------|
| **Primary Function** | Execute actions on the browser | Extract and analyze DOM information |
| **Direction** | Sends commands TO the browser | Gets information FROM the browser |
| **Focus** | Interaction and manipulation | Observation and extraction |
| **Timing** | Action-oriented (immediate execution) | State-oriented (snapshot analysis) |
| **Human-like Behavior** | Yes (randomness, delays, movement paths) | No (pure data extraction) |
| **CDP Usage** | Commands for interaction (click, type, etc.) | Commands for inspection (get DOM, content) |

## Relationship Between Modules

### Complementary Functions
- **DOM** provides the information needed to decide *what* to interact with
- **Actor** performs the actual *how* of interacting with elements

### Typical Workflow
1. **DOM** module analyzes page and identifies elements with indices
2. **AI** decides which element to interact with based on DOM information
3. **Actor** module executes the interaction on the chosen element
4. **DOM** module captures the new state after the action
5. Cycle repeats with updated information

### Data Flow
```
[DOM Analysis] -> [AI Decision] -> [Actor Action] -> [DOM Re-analysis]
(Page State)                    (Interaction)     (New State)
```

## Example Scenario

When clicking a search button:
- **DOM Module**: Discovers the search button and assigns it an index (e.g., #42)
- **AI Model**: Decides to click element #42 based on DOM information
- **Actor Module**: Performs realistic mouse movement to the button and clicks it
- **DOM Module**: Captures the new page state after the click

The two modules work together to enable AI agents to both *understand* the page (DOM) and *interact* with it (Actor) in a realistic manner.