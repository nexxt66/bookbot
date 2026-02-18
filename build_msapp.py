"""
Generates BookRecommender.msapp from scratch.
The .msapp format is a ZIP archive used by Microsoft Power Apps.
Internal format matches what `pac canvas pack` produces.
"""
import json
import zipfile
import io

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def jstr(obj):
    return json.dumps(obj, indent=2)

# ---------------------------------------------------------------------------
# Root manifest files
# ---------------------------------------------------------------------------

CONTENT_TYPES_XML = """\
<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="json" ContentType="application/json" />
  <Default Extension="sarif" ContentType="application/json" />
  <Default Extension="yaml" ContentType="text/plain" />
</Types>"""

HEADER = {
    "DocVersion": "2.1",
    "FileFormat": "2.0"
}

PROPERTIES = {
    "Author":                        "BookBot User",
    "Name":                          "BookRecommender",
    "Id":                            "00000000-0000-0000-0000-000000000001",
    "FileID":                        "00000000-0000-0000-0000-000000000002",
    "LocalConnectionReferences":     "{}",
    "LocalDatabaseReferences":       "{}",
    "LibraryDependencies":           "{}",
    "DocumentLayoutWidth":           640,
    "DocumentLayoutHeight":          1136,
    "DocumentLayoutOrientation":     "portrait",
    "PublishVersion":                "1.0",
    "AppCreationSource":             "AppFromScratch",
    "AppCreationSourceVersion":      "3.22081.22",
    "OriginalDataSourceType":        "None",
    "BackgroundImage":               "",
    "MinimumRequiredApiVersion":     "2.2.0",
    "HasResources":                  False
}

THEMES = {
    "Themes":    [],
    "CustomThemes": []
}

DATA_SOURCES = {
    "DataSources": []
}

RESOURCES = {
    "Resources": []
}

COMPONENTS_METADATA = []

CONTROL_TEMPLATES = {
    "ComponentTemplates": []
}

# ---------------------------------------------------------------------------
# App-level code  (OnStart loads the books collection)
# ---------------------------------------------------------------------------

APP_JSON = {
    "OnStart": (
        "=ClearCollect("
        "BooksCollection,"
        "{Genre:\"Fiction\",Title:\"To Kill a Mockingbird\",Author:\"Harper Lee\",Description:\"A timeless story of racial injustice and moral growth.\"},"
        "{Genre:\"Fiction\",Title:\"1984\",Author:\"George Orwell\",Description:\"A chilling dystopian novel about totalitarianism.\"},"
        "{Genre:\"Fiction\",Title:\"The Great Gatsby\",Author:\"F. Scott Fitzgerald\",Description:\"A portrait of the Jazz Age and the American Dream.\"},"
        "{Genre:\"Mystery\",Title:\"Gone Girl\",Author:\"Gillian Flynn\",Description:\"A dark psychological thriller about a marriage gone wrong.\"},"
        "{Genre:\"Mystery\",Title:\"The Girl with the Dragon Tattoo\",Author:\"Stieg Larsson\",Description:\"A gripping mystery involving a decades-old disappearance.\"},"
        "{Genre:\"Mystery\",Title:\"Big Little Lies\",Author:\"Liane Moriarty\",Description:\"A murder mystery woven through the lives of three women.\"},"
        "{Genre:\"Sci-Fi\",Title:\"Dune\",Author:\"Frank Herbert\",Description:\"An epic saga of politics and ecology on a desert planet.\"},"
        "{Genre:\"Sci-Fi\",Title:\"The Martian\",Author:\"Andy Weir\",Description:\"An astronaut stranded on Mars must use science to survive.\"},"
        "{Genre:\"Sci-Fi\",Title:\"Ender's Game\",Author:\"Orson Scott Card\",Description:\"A gifted child is trained to lead humanity against aliens.\"},"
        "{Genre:\"Fantasy\",Title:\"The Hobbit\",Author:\"J.R.R. Tolkien\",Description:\"A hobbit embarks on an unexpected journey.\"},"
        "{Genre:\"Fantasy\",Title:\"Harry Potter and the Sorcerer's Stone\",Author:\"J.K. Rowling\",Description:\"A boy discovers he is a wizard.\"},"
        "{Genre:\"Fantasy\",Title:\"The Name of the Wind\",Author:\"Patrick Rothfuss\",Description:\"A legendary figure tells his own story.\"},"
        "{Genre:\"Biography\",Title:\"Steve Jobs\",Author:\"Walter Isaacson\",Description:\"The definitive biography of Apple's visionary co-founder.\"},"
        "{Genre:\"Biography\",Title:\"Educated\",Author:\"Tara Westover\",Description:\"A memoir about growing up and self-reinvention.\"},"
        "{Genre:\"Biography\",Title:\"Becoming\",Author:\"Michelle Obama\",Description:\"An intimate memoir by the former First Lady.\"}"
        ")"
    ),
    "BackEnabled": "=false"
}

# ---------------------------------------------------------------------------
# Screen builders
# ---------------------------------------------------------------------------

def ctrl(name, template_id, props, children=None):
    """Build a ControlInfo dict."""
    node = {
        "Name":     name,
        "Type":     "ControlInfo",
        "Template": {"Id": template_id, "Version": "1.0", "Name": template_id},
        "Properties": props
    }
    if children:
        node["Children"] = children
    return node


def home_screen():
    return {
        "TopParent": ctrl("HomeScreen", "screen", {"Fill": "=RGBA(245, 245, 250, 1)"}, [
            ctrl("HeaderRect", "rectangle", {
                "X": "=0", "Y": "=0",
                "Width": "=Parent.Width", "Height": "=140",
                "Fill": "=RGBA(63, 81, 181, 1)"
            }),
            ctrl("AppIconLabel", "label", {
                "X": "=0", "Y": "=30",
                "Width": "=Parent.Width", "Height": "=50",
                "Text": "=\"\U0001F4DA\"",
                "Align": "=Align.Center",
                "Size": "=36",
                "Color": "=RGBA(255, 255, 255, 1)"
            }),
            ctrl("TitleLabel", "label", {
                "X": "=0", "Y": "=85",
                "Width": "=Parent.Width", "Height": "=40",
                "Text": "=\"Book Recommender\"",
                "Align": "=Align.Center",
                "Size": "=22",
                "Color": "=RGBA(255, 255, 255, 1)",
                "FontWeight": "=FontWeight.Bold"
            }),
            ctrl("SubtitleLabel", "label", {
                "X": "=20", "Y": "=165",
                "Width": "=Parent.Width-40", "Height": "=50",
                "Text": "=\"Select a genre to get personalised book recommendations.\"",
                "Align": "=Align.Center",
                "Size": "=14",
                "Color": "=RGBA(90, 90, 120, 1)"
            }),
            ctrl("GenreLabel", "label", {
                "X": "=20", "Y": "=235",
                "Width": "=Parent.Width-40", "Height": "=30",
                "Text": "=\"Choose a Genre\"",
                "Size": "=15",
                "FontWeight": "=FontWeight.Semibold",
                "Color": "=RGBA(50, 50, 80, 1)"
            }),
            ctrl("GenreDropdown", "dropdown", {
                "X": "=20", "Y": "=270",
                "Width": "=Parent.Width-40", "Height": "=55",
                "Items": "=[\"Fiction\",\"Mystery\",\"Sci-Fi\",\"Fantasy\",\"Biography\"]",
                "BorderColor": "=RGBA(63, 81, 181, 1)",
                "BorderThickness": "=2",
                "Color": "=RGBA(30, 30, 60, 1)",
                "Size": "=15"
            }),
            ctrl("RecommendBtn", "button", {
                "X": "=20", "Y": "=360",
                "Width": "=Parent.Width-40", "Height": "=60",
                "Text": "=\"Get Recommendations\"",
                "Fill": "=RGBA(63, 81, 181, 1)",
                "Color": "=RGBA(255, 255, 255, 1)",
                "Size": "=16",
                "FontWeight": "=FontWeight.Bold",
                "BorderRadius": "=8",
                "OnSelect": (
                    "=ClearCollect(FilteredBooks, Filter(BooksCollection, Genre = GenreDropdown.SelectedText));"
                    "Navigate(RecommendationsScreen, ScreenTransition.Fade)"
                )
            }),
            ctrl("FooterLabel", "label", {
                "X": "=0", "Y": "=Parent.Height-50",
                "Width": "=Parent.Width", "Height": "=40",
                "Text": "=\"BookBot \u2022 Powered by Power Apps\"",
                "Align": "=Align.Center",
                "Size": "=12",
                "Color": "=RGBA(160, 160, 180, 1)"
            })
        ])
    }


def recommendations_screen():
    gallery_children = [
        ctrl("CardRect", "rectangle", {
            "X": "=10", "Y": "=0",
            "Width": "=Parent.TemplateWidth-20", "Height": "=120",
            "Fill": "=RGBA(255, 255, 255, 1)",
            "BorderColor": "=RGBA(220, 220, 235, 1)",
            "BorderThickness": "=1",
            "BorderRadius": "=10"
        }),
        ctrl("TitleLabel", "label", {
            "X": "=24", "Y": "=12",
            "Width": "=Parent.TemplateWidth-44", "Height": "=34",
            "Text": "=ThisItem.Title",
            "Size": "=15",
            "FontWeight": "=FontWeight.Bold",
            "Color": "=RGBA(30, 30, 60, 1)"
        }),
        ctrl("AuthorLabel", "label", {
            "X": "=24", "Y": "=46",
            "Width": "=Parent.TemplateWidth-44", "Height": "=24",
            "Text": "=\"by \" & ThisItem.Author",
            "Size": "=13",
            "Color": "=RGBA(63, 81, 181, 1)",
            "FontStyle": "=FontStyle.Italic"
        }),
        ctrl("DescriptionLabel", "label", {
            "X": "=24", "Y": "=72",
            "Width": "=Parent.TemplateWidth-44", "Height": "=40",
            "Text": "=ThisItem.Description",
            "Size": "=12",
            "Color": "=RGBA(100, 100, 130, 1)",
            "Overflow": "=Overflow.Hidden"
        })
    ]

    return {
        "TopParent": ctrl("RecommendationsScreen", "screen", {"Fill": "=RGBA(245, 245, 250, 1)"}, [
            ctrl("HeaderRect", "rectangle", {
                "X": "=0", "Y": "=0",
                "Width": "=Parent.Width", "Height": "=110",
                "Fill": "=RGBA(63, 81, 181, 1)"
            }),
            ctrl("BackButton", "button", {
                "X": "=10", "Y": "=40",
                "Width": "=80", "Height": "=40",
                "Text": "=\"\u2190 Back\"",
                "Fill": "=RGBA(0, 0, 0, 0)",
                "Color": "=RGBA(255, 255, 255, 1)",
                "Size": "=14",
                "BorderThickness": "=0",
                "OnSelect": "=Navigate(HomeScreen, ScreenTransition.Fade)"
            }),
            ctrl("ScreenTitleLabel", "label", {
                "X": "=90", "Y": "=35",
                "Width": "=Parent.Width-100", "Height": "=50",
                "Text": "=\"Recommendations\"",
                "Size": "=20",
                "FontWeight": "=FontWeight.Bold",
                "Color": "=RGBA(255, 255, 255, 1)"
            }),
            ctrl("GenreBadge", "label", {
                "X": "=20", "Y": "=120",
                "Width": "=Parent.Width-40", "Height": "=36",
                "Text": "=\"Genre: \" & GenreDropdown.SelectedText",
                "Size": "=14",
                "FontWeight": "=FontWeight.Semibold",
                "Color": "=RGBA(63, 81, 181, 1)"
            }),
            ctrl("SeparatorRect", "rectangle", {
                "X": "=20", "Y": "=158",
                "Width": "=Parent.Width-40", "Height": "=2",
                "Fill": "=RGBA(200, 200, 220, 1)"
            }),
            ctrl("BooksGallery", "gallery", {
                "X": "=0", "Y": "=165",
                "Width": "=Parent.Width",
                "Height": "=Parent.Height-220",
                "Items": "=FilteredBooks",
                "TemplatePadding": "=12",
                "TemplateSize": "=130"
            }, gallery_children),
            ctrl("NoResultsLabel", "label", {
                "X": "=20", "Y": "=300",
                "Width": "=Parent.Width-40", "Height": "=60",
                "Text": "=\"No books found for this genre.\"",
                "Align": "=Align.Center",
                "Size": "=15",
                "Color": "=RGBA(160, 160, 180, 1)",
                "Visible": "=CountRows(FilteredBooks) = 0"
            }),
            ctrl("FooterLabel", "label", {
                "X": "=0", "Y": "=Parent.Height-50",
                "Width": "=Parent.Width", "Height": "=40",
                "Text": "=\"BookBot \u2022 Powered by Power Apps\"",
                "Align": "=Align.Center",
                "Size": "=12",
                "Color": "=RGBA(160, 160, 180, 1)"
            })
        ])
    }


# ---------------------------------------------------------------------------
# Main builder
# ---------------------------------------------------------------------------

def build():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml",          CONTENT_TYPES_XML)
        zf.writestr("Header.json",                  jstr(HEADER))
        zf.writestr("Properties.json",              jstr(PROPERTIES))
        zf.writestr("Themes.json",                  jstr(THEMES))
        zf.writestr("DataSources.json",             jstr(DATA_SOURCES))
        zf.writestr("Resources.json",               jstr(RESOURCES))
        zf.writestr("ComponentsMetadata.json",      jstr(COMPONENTS_METADATA))
        zf.writestr("ControlTemplates.json",        jstr(CONTROL_TEMPLATES))
        zf.writestr("Src/App.json",                 jstr(APP_JSON))
        zf.writestr("Src/HomeScreen.json",          jstr(home_screen()))
        zf.writestr("Src/RecommendationsScreen.json", jstr(recommendations_screen()))

    out = "BookRecommender.msapp"
    with open(out, "wb") as f:
        f.write(buf.getvalue())

    import os
    size = os.path.getsize(out)
    print(f"Created {out}  ({size:,} bytes)")
    print("Files inside the archive:")
    with zipfile.ZipFile(out) as zf:
        for info in zf.infolist():
            print(f"  {info.filename}  ({info.file_size} bytes)")


if __name__ == "__main__":
    build()
