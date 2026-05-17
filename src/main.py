"""Entry point"""
#########################################################
# Builtin packages
#########################################################
# (None)

#########################################################
# 3rd party packages
#########################################################
# (None)

#########################################################
# Own packages
#########################################################
from common.log import initialize_logger
from controllers.instagram_controller import InstagramController


def main():
    """main"""
    initialize_logger()
    InstagramController().run()


if __name__ == "__main__":
    main()
