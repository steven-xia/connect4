"""
file: setup.py

description: script to build the Cython components.
"""

if __name__ == "__main__":
    import setuptools

    import Cython.Build

    kwargs = {
        "extra_compile_args": ["/O2"],
    }

    directives = {

    }

    setuptools.setup(
        ext_modules=Cython.Build.cythonize(
            [setuptools.extension.Extension(
                name="board",
                sources=["board.pyx"],
                **kwargs
            ), setuptools.extension.Extension(
                name="evaluate",
                sources=["evaluate.pyx"],
                **kwargs
            )],
            nthreads=8,
            force=True,
            annotate=True,
            compiler_directives=directives
        )
    )
