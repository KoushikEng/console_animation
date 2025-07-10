# ⏳ console-animation

![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)

A lightweight and flexible Python decorator to show a console spinner (loading animation) while a function is running. Useful for long-running CLI tasks, data processing, I/O, or just making your tools feel more alive.

---

## 🔧 Features

- Add a console spinner with a single line
- Optional start, end, and error messages
- Customizable spinner style and speed
- Gracefully handles exceptions
- Works with or without decorator arguments
- Clean terminal output (hides cursor during spin)

---

## 📦 Installation

```bash
# pip install
pip install console_animation

# or

# Clone the repo
git clone https://github.com/KoushikEng/console-animation.git
cd console-animation

# Install locally
pip install .
````

> You can also install it in **editable mode** during development:
>
> ```bash
> pip install -e .
> ```

---

## 🚀 Usage

### ✅ Basic Spinner (no args)

```python
from console_spinner import loading_animation

@loading_animation
def task():
    import time
    time.sleep(3)
```

This will show a rotating spinner while `task()` runs.

---

### ⚙️ With Custom Messages

```python
@loading_animation(start="Processing...", loaded="✅ Task complete!", error="❌ Something broke.")
def do_work():
    time.sleep(5)
```

* `start` – message shown before spinner
* `loaded` or `end` – message shown after successful run
* `error` – message shown if exception occurs

---

### 🎯 Custom Spinner and Speed

```python
@loading_animation(spinner="⠋⠙⠚⠞⠖⠦⠴⠲⠳⠓", interval=0.05)
def fancy_task():
    time.sleep(3)
```

* `spinner`: any iterable of characters
* `interval`: time (in seconds) between frames

---

### ❗ Error Handling

If `error` is not provided:

* The spinner will stop
* Cursor will be restored
* The original exception is raised **as-is**

If `error` is set:

* It will be printed
* Full traceback is also printed for debugging

---

## 🧪 Example Script

```python
from console_spinner import loading_animation
import time

@loading_animation(start="Crunching numbers...", loaded="✅ Done!", error="🔥 Failed.")
def math_task():
    time.sleep(3)

@loading_animation
def quick_task():
    time.sleep(1)

@loading_animation(start="Breaking...", error="Oops.")
def will_fail():
    raise RuntimeError("Intentional failure.")

math_task()
quick_task()
will_fail()
```

---

## 🤝 Contributing

Contributions are **welcome and appreciated**!

If you want to:

* Add features (like async support, presets, color, etc.)
* Improve performance or compatibility
* Fix bugs
* Write tests or improve docs

Please feel free to:

1. Fork the repo
2. Create a new branch (`feature/your-feature`)
3. Commit your changes
4. Push and open a PR

> Issues and suggestions are also welcome in the [Issues](https://github.com/KoushikEng/console-animation/issues) tab.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](./LICENSE) file for details.

---

## 🙌 Credits

Built with frustration from boring terminal waits and love for clean CLI UX.

---

## 🛠️ To Do (Open for PRs)

* [ ] Async function support (`async def`)
* [ ] Color support (via `colorama`)
* [ ] Predefined spinner styles
* [ ] Timeout decorator option
* [ ] PyPI upload

---

Made by [Koushik](https://github.com/KoushikEng) 🔥