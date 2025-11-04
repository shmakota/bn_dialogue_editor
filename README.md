# Cataclysm: Bright Nights Dialogue Editor

A graph-based dialogue editor for Cataclysm: Bright Nights that allows you to visually edit dialogue files by representing talk_topics as nodes in a node graph.

## Features

- **Visual Node Graph**: Each talk_topic is displayed as a node with connections representing dialogue flow
- **Import/Export**: Import existing dialogue JSON files and export your edited work
- **Node Editing**: Edit topic IDs, dynamic lines, responses, and speaker effects
- **Interactive Canvas**: Drag nodes, pan, zoom, and select nodes to edit
- **Validation**: Check for broken references, duplicate IDs, and other errors
- **Auto Layout**: Automatic node positioning using force-directed layout algorithm

## Requirements

- Python 3.7 or higher
- tkinter (usually included with Python)
  - Ubuntu/Debian: `sudo apt-get install python3-tk`
  - Fedora: `sudo dnf install python3-tkinter`
  - macOS/Windows: Usually pre-installed

## Installation

1. Clone or download this repository
2. Ensure Python 3.7+ is installed
3. Install tkinter if needed (see Requirements above)

## Usage

Run the editor:

```bash
python main.py
```

Or from the src directory:

```bash
python -m src.main
```

### Basic Workflow

1. **Import a dialogue file**: Click "Import" or use File → Import to load a JSON dialogue file
2. **View the graph**: Topics appear as nodes with connections showing dialogue flow
3. **Select a node**: Click on any node to view and edit its properties
4. **Edit properties**: Use the property editor panel to modify:
   - Dynamic lines (dialogue variations)
   - Responses (connections to other topics)
   - Speaker effects
5. **Add new topics**: Click "New Topic" to create a new dialogue topic
6. **Auto layout**: Click "Auto Layout" to automatically arrange nodes
7. **Validate**: Click "Validate" to check for errors
8. **Export**: Click "Export" or use File → Export to save your changes

### Node Interaction

- **Click**: Select a node
- **Drag**: Move a node around the canvas
- **Mouse Wheel**: Zoom in/out
- **Middle Mouse Button**: Pan the canvas

### Editing Nodes

When a node is selected, you can:
- Edit dynamic lines (add, remove, modify)
- Add/edit/remove responses that link to other topics
- Edit speaker effects (JSON format)
- Update the node to save changes

## Project Structure

```
bn_dialogue_editor/
├── dialogue/
│   └── example/          # Example dialogue files
├── src/
│   ├── models/           # Data models (DialogueTopic, DialogueGraph)
│   ├── parsers/          # JSON import/export and validation
│   ├── ui/               # UI components (canvas, editor, toolbar)
│   ├── graph/            # Graph management and layout
│   └── utils/            # Utility functions
├── main.py               # Entry point
├── requirements.txt      # Dependencies (none required)
└── README.md            # This file
```

## Dialogue Format

The editor works with Cataclysm: Bright Nights dialogue files, which are JSON arrays of talk_topic objects:

```json
[
  {
    "type": "talk_topic",
    "id": "TALK_EXAMPLE",
    "dynamic_line": ["Hello there!"],
    "responses": [
      { "text": "Hi", "topic": "TALK_OTHER" }
    ]
  }
]
```

## Future Enhancements

Planned features (see PROJECT_OUTLINE.md for details):
- Undo/redo system
- Copy/paste nodes
- Dialogue preview/simulation
- Multi-file project management
- Enhanced graphics and themes
- Search and replace
- Export graph as image

## License

This project is open source and available for modification and distribution.

## Contributing

Contributions are welcome! Please refer to PROJECT_OUTLINE.md for the project architecture and design considerations.




