import os
import sys
import manager


running = True


def main():
    index = 0
    for arg in sys.argv:
        if arg.lower() == "--generate-default-templates":
            manager.generateDefaultTemplates()
            sys.exit(0)
        elif arg.lower() == "--apply-template":
            manager.applyTemplate(index + 1)
            break

        index += 1


if __name__ == "__main__":
    main()
