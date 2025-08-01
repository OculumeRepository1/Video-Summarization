import toga
from toga.style import Pack


class HelloWorld(toga.App):
    def startup(self):
        layout = toga.Box()

        self.button = toga.Button(
            "Say Hello!",
            on_press=self.say_hello,
            style=Pack(margin=5),
        )
        layout.add(self.button)

        self.main_window = toga.MainWindow(title="Hello world!")
        self.main_window.content = layout
        self.main_window.show()

    def say_hello(self, source_widget):
        # Receives the button that was clicked.
        source_widget.text = "Hello, world!"


app = HelloWorld(formal_name="Hello, world!", app_id="hello.world")
app.main_loop()