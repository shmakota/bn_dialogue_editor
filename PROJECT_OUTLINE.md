# Cataclysm: Bright Nights Dialogue Editor - Project Outline

## Overview
A graph-based dialogue editor for Cataclysm: Bright Nights that allows users to visually edit dialogue files by representing talk_topics as nodes in a node graph. Built with Python and Tkinter, this tool enables intuitive creation and modification of dialogue trees while maintaining compatibility with the game's JSON dialogue format.

## Current Status: IMPLEMENTED ✅

This project has reached a functional state with all core features implemented and working.

## Core Features (Implemented)

### 1. File Management ✅
- **Import Dialogue Files**
  - Load JSON files containing talk_topics
  - Parse and validate dialogue structure
  - Handle nested structures and references
  - Support for all standard dialogue formats

- **Export Dialogue Files**
  - Export edited dialogue to JSON format
  - Maintain proper formatting and structure
  - Validate output before saving
  - Preserves all dialogue data

### 2. Node Graph Interface ✅
- **Node Representation**
  - Each talk_topic displayed as a node in the graph
  - Node visualization includes:
    - Topic ID display
    - Preview of dynamic_line content
    - Visual indicator of number of responses
    - Selected node highlighting
    - Conditional line indicators (⚙ emoji)

- **Connection System**
  - Edges represent responses between talk_topics
  - Each response object creates a connection from current node to target node
  - Visual representation of dialogue flow
  - Support for multiple outgoing connections (multiple responses)
  - Support for multiple incoming connections

- **Graph Canvas**
  - Pan and zoom functionality (mouse wheel, middle mouse button, arrow keys)
  - Node selection and manipulation
  - Drag-and-drop node positioning
  - Auto-layout algorithms (force-directed and grid layouts)
  - Manual node positioning with persistence
  - Grid display that moves with view
  - Snap-to-grid functionality

### 3. Node Editing ✅
- **Topic Properties Editor**
  - Edit topic ID (read-only display for selected node)
  - Edit dynamic_line (single entry with full editor)
  - Add/remove/edit responses
  - Edit speaker_effect objects
  - Handle conditional topics and effects

- **Dynamic Line Editor**
  - **Simple Text Tab**: Direct text entry
  - **Conditional Tab**: 
    - Simple condition editor with form-based UI
    - Raw JSON editor for advanced conditions
    - Optional yes/no branches
    - Support for variables, effects, gender, environment, and boolean logic
  - **Advanced Tab**: Raw JSON editor for complex structures
  - Support for strings, arrays, and conditional dicts

- **Response Management** ✅
  - Add new responses to nodes
  - Edit response text
  - Link responses to target topics (dropdown with custom entry)
  - Support for special topics (TALK_NONE, TALK_DONE, TALK_TRAIN)
  - Remove responses
  - **Response Editor Tabs**:
    - **Basic Tab**: Direct topic responses
    - **Trial Tab**: Skill checks (PERSUADE, INTIMIDATE, LIE) with success/failure branches
    - **Advanced Tab**: 
      - Condition editing (simple form + raw JSON)
      - True/False text support
      - Switch option
      - Effect, opinion, and mission_opinion handled in trial success/failure

- **Effects Editor** ✅
  - Visual editor for speaker_effect objects
  - **Simple Tab**: Form-based editor for:
    - npc_add_var (with type, context, value)
    - u_adjust_var
    - npc_add_effect (with duration)
    - u_add_effect (with duration)
    - mapgen_update (complex - use advanced tab)
  - **Advanced Tab**: Raw JSON editor for complex structures
  - Handles flattened structures and effect wrappers

- **Condition Editor** ✅
  - **Simple Tab**: Form-based editor supporting:
    - Variable checks (npc_has_var, u_has_var with type, context, value)
    - Effect checks (npc_has_effect, u_has_effect)
    - Gender checks (npc_female, npc_male, u_female, u_male)
    - Environment checks (days_since_cataclysm, is_season, is_day, is_outside)
    - Boolean logic (AND, OR, NOT) with nested sub-condition editing
  - **Raw JSON Tab**: Direct JSON editing
  - Nested condition support through SubConditionDialog

### 4. Visual Features ✅
- **Node Styling**
  - Selected nodes highlighted in blue
  - Different colors for selected vs unselected nodes
  - Visual indicators for conditional lines (⚙)
  - Response count display
  - Grid background with major/minor lines

- **Graph Navigation**
  - Mouse wheel zoom (inverted delta support for Linux)
  - Middle mouse button panning
  - Arrow key panning (20px per keypress)
  - Zoom in/out/reset buttons in toolbar
  - Auto-layout button for automatic node arrangement

### 5. Validation & Error Handling ✅
- **Real-time Validation**
  - Check for broken references (topics that don't exist)
  - Validate JSON structure
  - Check for duplicate topic IDs
  - Validate effect syntax

- **Error Display**
  - Validation button in toolbar
  - Error messages displayed in dialog
  - Export validation with warning before saving

## Technical Architecture

### 1. Project Structure
```
bn_dialogue_editor/
├── dialogue/
│   └── example/              # Example dialogue files
├── src/
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── models/
│   │   ├── __init__.py
│   │   └── dialogue.py     # DialogueTopic, DialogueGraph models
│   ├── parsers/
│   │   ├── __init__.py
│   │   ├── json_parser.py  # JSON import/export
│   │   └── validator.py    # Validation logic
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── main_window.py  # Main application window
│   │   ├── graph_canvas.py # Node graph canvas
│   │   ├── property_editor.py # Property editing panel with dialogs
│   │   ├── toolbar.py      # Toolbar and menus
│   │   └── help_dialog.py  # Information atlas / help dialog
│   ├── graph/
│   │   ├── __init__.py
│   │   ├── graph_manager.py # Graph state management
│   │   └── layout.py        # Node positioning algorithms
│   └── utils/
│       ├── __init__.py
│       └── helpers.py      # Utility functions
├── main.py                  # Application entry point
├── requirements.txt
├── README.md
└── PROJECT_OUTLINE.md
```

### 2. Core Components

#### Data Models
- **DialogueTopic**: Represents a single talk_topic
  - Properties: id, type, dynamic_line (string/dict/list), speaker_effect (dict), responses (list)
  - Methods: to_json(), from_json(), validate()
  - Handles all dialogue formats (simple strings, arrays, conditional dicts)

- **DialogueGraph**: Manages collection of topics and connections
  - Properties: topics (dict), connections (derived)
  - Methods: add_topic(), remove_topic(), get_connections(), find_paths()
  - Builds connection graph from responses

#### UI Components
- **MainWindow**: Primary application window
  - Toolbar with Import, Export, New Topic, Validate, Auto Layout, Zoom, Help
  - Split pane layout (graph canvas + property editor)
  - Status bar

- **GraphCanvas**: Tkinter Canvas for node graph
  - Mouse event handling (select, drag, pan, zoom)
  - Node rendering with zoom scaling
  - Connection rendering between nodes
  - Grid rendering (moves with view)
  - Arrow key panning support
  - Scrollbars (horizontal and vertical)
  - Performance optimizations (grid culling, redraw throttling)

- **PropertyEditor**: Panel for editing selected node properties
  - Dynamic line editor (single entry display)
  - Response list editor
  - Speaker effect editor
  - Update Node button
  - Dialogs: DynamicLineDialog, ResponseDialog, SpeakerEffectDialog, SubConditionDialog

- **Dialogs**:
  - **DynamicLineDialog**: Simple Text / Conditional / Advanced tabs
  - **ResponseDialog**: Basic (Direct) / Trial / Advanced tabs
  - **SpeakerEffectDialog**: Simple / Advanced tabs
  - **SubConditionDialog**: For editing nested conditions in boolean logic

#### Parsers
- **JSONParser**: Handles import/export
  - parse_file(): Load JSON into DialogueGraph
  - export_file(): Save DialogueGraph to JSON
  - Handles all dialogue formats correctly

- **Validator**: Validation logic
  - validate_graph(): Check all topic references exist
  - validate_ids(): Check for duplicates
  - validate_structure(): Check required fields

### 3. Key Algorithms

#### Node Layout ✅
- **Force-directed layout**: Automatic positioning using physics simulation
- **Grid layout**: Structured positioning option
- **Manual positioning**: User-defined positions saved and persisted

#### Graph Analysis ✅
- **Reference resolution**: Build connection graph from responses
- **Connection tracking**: Visual representation of dialogue flow

### 4. Technology Stack
- **Python 3.x**: Core language
- **Tkinter**: GUI framework (included with Python)
- **json**: Standard library for JSON parsing
- **dataclasses**: For data models
- **typing**: Type hints throughout

## User Workflow

### Importing Dialogue ✅
1. File → Import or click "Import" button
2. Select JSON file
3. System parses and validates
4. Graph automatically generates with all topics as nodes
5. Initial layout applied automatically

### Editing a Topic ✅
1. Click on a node in the graph
2. Node highlights and property editor populates
3. Click "Edit" buttons to open dialogs
4. Make changes in dialog (Simple or Advanced tabs)
5. Click "Update Node" to save changes
6. Changes reflect immediately on node

### Adding a New Topic ✅
1. Click "New Topic" in the toolbar
2. Dialog prompts for topic ID
3. New node appears in graph
4. Edit properties in property editor
5. Add responses to connect to other topics

### Creating Connections ✅
1. Select source node
2. In property editor, click "Add" under Responses
3. In response dialog, specify target topic (dropdown or type custom)
4. Connection line appears in graph automatically
5. Multiple responses create multiple connections

### Exporting Dialogue ✅
1. Click "Validate" to check for errors (optional)
2. Click "Export" button
3. Validation runs automatically
4. Any errors/warnings displayed
5. Choose save location
6. JSON file generated with all data

## Data Format Handling

### Talk Topic Structure ✅
- **id**: String identifier (required)
- **type**: Always "talk_topic" (required)
- **dynamic_line**: Can be:
  - String (simple text)
  - Dict (conditional with yes/no branches)
  - List (array of strings for random selection)
  - None (optional)
- **speaker_effect**: Object or dict (optional)
- **responses**: Array of response objects (optional)

### Response Object Structure ✅
- **text**: String (response text shown to player)
- **topic**: String (target talk_topic ID or special value) - for direct responses
- **trial**: Object with type, difficulty, mod (optional) - for skill checks
- **success**: Object with topic, effect, opinion, mission_opinion - for trial success
- **failure**: Object with topic, effect, opinion, mission_opinion - for trial failure
- **condition**: Dict or object - condition check for response availability
- **truefalsetext**: Dict with true/false text and condition - for conditional text
- **switch**: Boolean - switch flag

### Special Topic Values ✅
- **TALK_NONE**: Return to previous topic
- **TALK_DONE**: End conversation
- **TALK_TRAIN**: Training topic
- Custom topic IDs (can type any value)

### Speaker Effect Structure ✅
- **npc_add_var**: String or dict with type, context, value
- **u_adjust_var**: String
- **npc_add_effect**: String or dict with duration
- **u_add_effect**: String or dict with duration
- **mapgen_update**: Complex object (use Advanced tab)
- Can be wrapped in **effect** key: `{ "effect": { ... } }`

## Features Summary

### Implemented Features ✅
1. **File Operations**: Import/Export JSON dialogue files
2. **Graph Visualization**: Nodes and connections with pan/zoom
3. **Node Editing**: Full editor for all topic properties
4. **Dynamic Lines**: Simple text, conditional, and advanced editing
5. **Responses**: Direct topics, trials (skill checks), conditions
6. **Speaker Effects**: Form-based and raw JSON editing
7. **Conditions**: Simple form editor and raw JSON
8. **Boolean Logic**: AND/OR/NOT with nested sub-conditions
9. **Layout**: Auto-layout and manual positioning
10. **Validation**: Reference checking and structure validation
11. **Navigation**: Mouse wheel zoom, middle button pan, arrow keys
12. **Grid**: Visual grid that moves with view
13. **Help**: Information atlas with examples and documentation

### UI Features
- Tabbed dialogs (Simple/Advanced) for complex editing
- Form-based editors for common patterns
- Raw JSON editors for advanced users
- Horizontal scrollbars for long text
- Visual indicators (emojis) for different content types
- Clickable documentation links

## Known Limitations

- No undo/redo system (future enhancement)
- No multi-file project management (single file at a time)
- No copy/paste of nodes
- No search/filter functionality for nodes
- No minimap or overview window

## Future Enhancements (Potential)

### Advanced Features
- Multi-file project management
- Undo/redo system
- Copy/paste nodes
- Batch operations
- Dialogue preview/simulation
- Template system for common dialogue patterns
- Search and replace across all topics
- Statistics view (node count, connection count, etc.)

### UI Improvements
- Customizable themes
- Zoom presets
- More keyboard shortcuts
- Node grouping/folding
- Export graph as image
- Print-friendly view

### Integration Features
- Direct integration with game files
- Auto-reload on file change
- Git integration
- Backup system

## Design Decisions

### Scalability
- Efficient rendering for large graphs
- Grid culling (skips drawing if too many lines)
- Redraw throttling (prevents performance issues)
- Optimized canvas updates

### Usability
- Intuitive interface following common graph editor conventions
- Clear visual feedback (highlighting, emojis)
- Form-based editors for common patterns
- Raw JSON access for power users
- Information atlas with examples

### Maintainability
- Clean separation of concerns (models, UI, parsers)
- Well-documented code structure
- Extensible architecture (easy to add new editors)
- Dialog-based editing (modular)

### Compatibility
- Strict adherence to CBN dialogue format
- Validation to prevent format-breaking changes
- Preserves existing dialogue metadata
- Supports all dialogue structure variations

## Implementation Status

### ✅ Phase 1: Core Structure - COMPLETE
- Basic project setup
- Data models (DialogueTopic, DialogueGraph)
- JSON parser (import/export)
- Basic validation

### ✅ Phase 2: Basic UI - COMPLETE
- Main window structure
- Graph canvas
- Property editor panel
- Toolbar

### ✅ Phase 3: Node Visualization - COMPLETE
- Node rendering on canvas
- Node selection
- Node positioning
- Connection line rendering

### ✅ Phase 4: Editing Functionality - COMPLETE
- Node property editing
- Add/remove nodes
- Add/remove/edit responses
- Dynamic line editing
- Speaker effect editing

### ✅ Phase 5: Graph Interactions - COMPLETE
- Node dragging
- Pan and zoom
- Connection visualization
- Layout algorithms

### ✅ Phase 6: Polish & Validation - COMPLETE
- Advanced validation
- Error display
- Help documentation (Information Atlas)
- UI refinements

## Notes
- This is a desktop application (not web-based)
- Focus on functionality over advanced graphics
- Prioritize correctness of output format
- All dialogue relationships are visually clear
- Supports both simple and complex dialogue trees
- Fully functional for editing Cataclysm: Bright Nights dialogue files
