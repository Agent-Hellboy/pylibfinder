#!/usr/bin/env python3
"""
Interactive TUI (Terminal User Interface) for pylibfinder
Beautiful terminal interface with keyboard navigation and interactive search
"""


import pylibfinder
from textual.app import App, ComposeResult, on
from textual.widgets import DataTable, Footer, Header, Input, Static


class SearchHeader(Static):
    """Header with title and instructions"""

    def render(self) -> str:
        return """[bold cyan]pylibfinder - Semantic Function Search[/bold cyan]
[dim]Search for similar functions in Python stdlib[/dim]"""


class ResultsTable(DataTable):
    """Table displaying search results"""

    def on_mount(self) -> None:
        self.add_columns("#", "Function", "Module", "Score", "Match %")


class SearchInput(Static):
    """Search input area"""

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Enter keyword (e.g., power, print, parseInt)", id="search-input")


class SearchApp(App):
    """Interactive TUI application"""

    BINDINGS = [
        ("ctrl+c", "quit", "Quit"),
        ("ctrl+l", "clear_search", "Clear"),
    ]

    CSS = """
    Screen {
        layout: vertical;
        background: $panel;
    }

    SearchHeader {
        dock: top;
        height: 3;
        background: $boost;
        color: $text;
        border: solid $accent;
        padding: 1;
    }

    SearchInput {
        dock: top;
        height: 3;
        border: solid $accent;
        padding: 1;
    }

    #search-input {
        border: solid $accent;
        margin: 1;
    }

    ResultsTable {
        border: solid $accent;
        margin: 1;
    }

    Footer {
        dock: bottom;
        color: $text;
    }

    Static {
        width: 1fr;
    }
    """

    TITLE = "pylibfinder - Function Search"

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        yield SearchHeader()
        yield SearchInput()
        yield ResultsTable(id="results-table")
        yield Footer()

    def on_mount(self) -> None:
        """Initialize the app"""
        self.query_one("#search-input", Input).focus()

    @on(Input.Submitted)
    def perform_search(self, event: Input.Submitted) -> None:
        """Perform search when user submits"""
        query = event.value.strip()
        if not query:
            return

        # Parse threshold if provided
        parts = query.rsplit(" ", 1)
        keyword = parts[0]
        threshold = 0.5

        try:
            if len(parts) == 2:
                threshold = float(parts[1])
                keyword = parts[0]
        except ValueError:
            pass

        # Perform search
        try:
            results = pylibfinder.find_similar(keyword, threshold)
            self.display_results(results, keyword, threshold)
        except Exception as e:
            self.display_error(str(e))

    def display_results(self, results: list[dict], query: str, threshold: float) -> None:
        """Display search results in the table"""
        table = self.query_one("#results-table", ResultsTable)
        table.clear()

        if not results:
            return

        # Sort by score descending
        sorted_results = sorted(results, key=lambda x: x["Score"], reverse=True)

        # Add rows to table
        for idx, result in enumerate(sorted_results, 1):
            func_name = result["Function"]
            module_name = result["Module"]
            score = result["Score"]
            percentage = f"{score*100:.1f}%"

            # Create progress bar
            bar_width = 10
            filled = int(score * bar_width)
            empty = bar_width - filled
            bar = "█" * filled + "░" * empty

            table.add_row(str(idx), func_name, module_name, bar, percentage, key=str(idx))

    def display_error(self, error: str) -> None:
        """Display error message"""
        table = self.query_one("#results-table", ResultsTable)
        table.clear()
        self.notify(f"Error: {error}", severity="error")

    def action_clear_search(self) -> None:
        """Clear search results"""
        table = self.query_one("#results-table", ResultsTable)
        table.clear()
        input_widget = self.query_one("#search-input", Input)
        input_widget.value = ""
        input_widget.focus()


def main():
    """Run the interactive TUI"""
    app = SearchApp()
    app.run()


if __name__ == "__main__":
    main()
