"""
Entrypoint for pyinstaller executable.
"""
if __name__ == "__main__":
    import aws_clipper.cli

    aws_clipper.cli.main()
