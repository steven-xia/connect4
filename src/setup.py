"""
file: setup.py

description: script to build the Cython components.
"""

if __name__ == "__main__":
    import setuptools

    import Cython.Build

    setuptools.setup(
        ext_modules=Cython.Build.cythonize(
            setuptools.extension.Extension(
                name="board",
                sources=["board.pyx"],
                extra_compile_args=["/O2"]
            ),
        )
    )
