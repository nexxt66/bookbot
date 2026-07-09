# BookBot – Power Apps Canvas App

A simple Microsoft Power Apps canvas app that recommends books based on the user's chosen genre.

## Screens

| Screen | Description |
|---|---|
| **HomeScreen** | Welcome screen with a genre dropdown and a "Get Recommendations" button |
| **RecommendationsScreen** | Gallery of recommended books filtered by the selected genre |

## Genres & Books

The app includes 3 book recommendations per genre:

- **Fiction** – To Kill a Mockingbird, 1984, The Great Gatsby
- **Mystery** – Gone Girl, The Girl with the Dragon Tattoo, Big Little Lies
- **Sci-Fi** – Dune, The Martian, Ender's Game
- **Fantasy** – The Hobbit, Harry Potter and the Sorcerer's Stone, The Name of the Wind
- **Biography** – Steve Jobs, Educated, Becoming

## Project Structure

```
bookbot/
├── CanvasManifest.json          # App manifest (layout, orientation)
├── Properties.json              # App metadata
├── Src/
│   ├── App.fx.yaml              # App-level code (OnStart: loads book data)
│   ├── HomeScreen.fx.yaml       # Home screen with genre selector
│   ├── RecommendationsScreen.fx.yaml  # Results gallery screen
│   └── EditorState.json         # Studio editor state
└── pkgs/
    └── References/
        ├── DataSources.json     # External data sources (none – data is inline)
        └── Resources.json       # Media/resource references
```

## How to Import into Power Apps

1. Install the [Power Platform CLI](https://learn.microsoft.com/en-us/power-platform/developer/cli/introduction).
2. Pack the source files into a `.msapp` file:
   ```bash
   pac canvas pack --sources . --msapp BookRecommender.msapp
   ```
3. Go to [make.powerapps.com](https://make.powerapps.com) → **Apps** → **Import canvas app**.
4. Upload `BookRecommender.msapp` and publish.
