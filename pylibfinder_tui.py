#!/usr/bin/env python3
"""
Interactive TUI (Terminal User Interface) for pylibfinder
Real-time semantic function search with live results
"""

import pylibfinder
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import DataTable, Footer, Header, Input, Static


class TitleBar(Static):
    """Simple title bar with filter toggle"""

    show_all = reactive(False)

    def render(self) -> str:
        filter_status = "[red]✓ Callable Only[/red]" if not self.show_all else "[yellow]✗ All Objects[/yellow]"
        return f"[bold cyan]pylibfinder[/bold cyan] - Search Python Objects | {filter_status} (Press Tab to toggle)"


class SearchBox(Static):
    """Search input wrapper"""

    def compose(self) -> ComposeResult:
        yield Input(id="search-input", placeholder="Type to search...")


class ResultsTable(DataTable):
    """Table displaying search results"""

    def on_mount(self) -> None:
        self.add_columns("Object Name", "Module", "Type", "Score")


class SearchApp(App):
    """Interactive TUI application with live search"""

    BINDINGS = [
        ("ctrl+c", "quit", "Quit"),
        ("ctrl+l", "clear_search", "Clear"),
        ("tab", "toggle_filter", "Toggle Filter"),
    ]

    CSS = """
    Screen {
        layout: vertical;
        background: $surface;
    }

    TitleBar {
        dock: top;
        height: 2;
        background: $boost;
        color: $text;
        padding: 0 1;
        border: solid $accent;
    }

    SearchBox {
        dock: top;
        height: 3;
        border: solid $accent;
    }

    #search-input {
        width: 100%;
        height: 1;
        border: none;
        background: $boost;
        color: $text;
    }

    ResultsTable {
        border: solid $accent;
    }

    Footer {
        dock: bottom;
    }
    """

    TITLE = "pylibfinder"

    def __init__(self):
        super().__init__()
        self.callable_only = True

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        yield TitleBar()
        yield SearchBox()
        yield ResultsTable(id="results-table")
        yield Footer()

    def on_mount(self) -> None:
        """Initialize and focus search input"""
        input_widget = self.query_one("#search-input", Input)
        input_widget.focus()

    def watch_search_value(self) -> None:
        """Trigger search when input changes"""
        input_widget = self.query_one("#search-input", Input)
        query = input_widget.value.strip()

        if not query or len(query) < 1:
            self.query_one("#results-table", ResultsTable).clear()
            return

        try:
            results = pylibfinder.find_similar(query, threshold=0.3, callable_only=self.callable_only)
            self.display_results(results)
        except Exception:
            pass

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input changes for live search"""
        self.watch_search_value()

    def display_results(self, results: list[dict]) -> None:
        """Display results in the table"""
        table = self.query_one("#results-table", ResultsTable)
        table.clear()

        if not results:
            return

        sorted_results = sorted(results, key=lambda x: x.get("Score", 0), reverse=True)

        for result in sorted_results[:30]:
            obj_name = result["Object Name"]
            module_name = result["Module"]
            obj_type = result.get("Type", "Unknown")
            score = result.get("Score", 0)

            percentage = f"{score*100:.1f}%"

            if score >= 0.9:
                color = "bright_green"
            elif score >= 0.7:
                color = "bright_cyan"
            elif score >= 0.5:
                color = "bright_yellow"
            else:
                color = "bright_red"

            bar_width = 10
            filled = int(score * bar_width)
            bar = "[" + "=" * filled + "-" * (bar_width - filled) + "]"
            score_display = f"[{color}]{bar} {percentage}[/{color}]"

            table.add_row(obj_name, module_name, obj_type, score_display)

    def action_clear_search(self) -> None:
        """Clear search results"""
        input_widget = self.query_one("#search-input", Input)
        input_widget.value = ""
        table = self.query_one("#results-table", ResultsTable)
        table.clear()

    def action_toggle_filter(self) -> None:
        """Toggle callable_only filter"""
        self.callable_only = not self.callable_only
        title_bar = self.query_one("TitleBar")
        title_bar.show_all = not self.callable_only
        # Re-run search with new filter
        self.watch_search_value()


def main():
    """Run the interactive TUI"""
    app = SearchApp()
    app.run()


if __name__ == "__main__":
    main()
