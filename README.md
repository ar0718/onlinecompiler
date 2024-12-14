
# Online Compiler Project
### Current status: Backend Under Developement

Welcome to the **Online Compiler** project! This is an ongoing development effort to build a robust backend for an online code compilation platform using Django. The backend will serve as the foundation for a future full-stack application, enabling users to write, compile, and execute code securely within a sandboxed environment.

---

## 🚧 Project Status: Under Development 🚧

The project is **not yet ready for production use**. Features and functionalities are being actively developed, tested, and improved.

---

## Vision

The goal of this project is to provide a scalable and secure backend for an online compiler that supports multiple programming languages. This platform will be designed for:
- Students and educators for learning and teaching programming.
- Developers testing code snippets without needing a local environment.
- Organizations conducting coding assessments or competitions.

Planned features include:
- Support for various programming languages (e.g., Python, Java, C++).
- Real-time compilation and execution with instant feedback.
- REST APIs to integrate with a future front-end application.
- A secure and isolated execution environment to handle user code.

---

## Installation Guide

To run the backend locally, follow the steps below:

### Steps

1. **Clone the Repository**
   ``` bash
   git clone https://github.com/premagarwals/onlinecompiler.git
   cd onlinecompiler
	```


2.  **Create a Virtual Environment**
    
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```
    
3.  **Install Dependencies** Install the required Python libraries by running:
    
    ```bash
    pip install -r requirements.txt
    ```
    
4.  **Run the Development Server** Start the Django development server:
    
    ```bash
    python manage.py runserver
    ```
    
    The server will be accessible at `http://127.0.0.1:8000/`.


## Future Roadmap

-   **Multi-language Support**: Add compiler support for Python, Java, C++, and more.
-   **RESTful APIs**: Provide APIs for front-end integration and external usage.
-   **Secure Execution**: Implement sandboxed environments for running untrusted user code.
-   **Error Handling**: Develop robust error reporting and debugging tools.
-   **Testing**: Add unit tests and integration tests for all APIs.

Stay tuned for updates!

----------

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

```
COPYRIGHT (C) [YEAR] [AUTHOR/ORGANIZATION]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

```
