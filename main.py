import os
import sys
import manager

running = True


def main():
    for arg in sys.argv:
        if arg.lower() == "--generate-default-templates":
            manager.generateDefaultTemplates()
            sys.exit(0)


if __name__ == "__main__":
    main()
